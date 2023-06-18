from flask import Flask,request
import pyspark
import pyspark.ml.feature
import pyspark.mllib.linalg
import pyspark.ml.param
import pyspark.sql.functions
from pyspark.sql import functions as F
from pyspark.sql.types import FloatType
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import udf
from scipy.spatial import distance
#only version 2.1 upwards
#from pyspark.ml.feature import BucketedRandomProjectionLSH
from pyspark.mllib.linalg import Vectors
from pyspark.ml.param.shared import *
from pyspark.mllib.linalg import Vectors, VectorUDT
from pyspark.ml.feature import VectorAssembler
import numpy as np
#import org.apache.spark.sql.functions.typedLit
from pyspark.sql.functions import lit
from pyspark.sql.functions import levenshtein  
from pyspark.sql.functions import col
from pyspark.sql.functions import desc
from pyspark.sql.functions import asc
import scipy as sp
from scipy.signal import butter, lfilter, freqz, correlate2d, sosfilt
import time
import sys
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row
import spark_ara_df

import mpi4py_ara_features as features
import mpi4py_ara_files as files
import glob
import os
from pyspark.sql.functions import to_json
import pathlib
import pandas as pd
import openpyxl
import json

similer = Flask(__name__)

# confCluster = SparkConf().setAppName("MusicSimilarity Cluster")
# confCluster.set("spark.driver.memory", "8g")
# confCluster.set("spark.executor.memory", "8g")
# confCluster.set("spark.driver.memoryOverhead", "6g")
# confCluster.set("spark.executor.memoryOverhead", "6g")
# #Be sure that the sum of the driver or executor memory plus the driver or executor memory overhead is always less than the value of yarn.nodemanager.resource.memory-mb
# #confCluster.set("yarn.nodemanager.resource.memory-mb", "196608")
# #spark.driver/executor.memory + spark.driver/executor.memoryOverhead < yarn.nodemanager.resource.memory-mb
# confCluster.set("spark.yarn.executor.memoryOverhead", "4096")
# #set cores of each executor and the driver -> less than avail -> more executors spawn
# confCluster.set("spark.driver.cores", "12")
# confCluster.set("spark.executor.cores", "12")
# confCluster.set("spark.dynamicAllocation.enabled", "True")
# confCluster.set("spark.dynamicAllocation.minExecutors", "15")
# confCluster.set("spark.dynamicAllocation.maxExecutors", "15")
# confCluster.set("yarn.nodemanager.vmem-check-enabled", "false")
# repartition_count = 32


confCluster = SparkConf().setAppName("MusicSimilarity Cluster")
confCluster.set("spark.driver.memory", "4g")
confCluster.set("spark.executor.memory", "4g")
confCluster.set("spark.driver.memoryOverhead", "2g")
confCluster.set("spark.executor.memoryOverhead", "2g")
#Be sure that the sum of the driver or executor memory plus the driver or executor memory overhead is always less than the value of yarn.nodemanager.resource.memory-mb
#confCluster.set("yarn.nodemanager.resource.memory-mb", "196608")
#spark.driver/executor.memory + spark.driver/executor.memoryOverhead < yarn.nodemanager.resource.memory-mb
confCluster.set("spark.yarn.executor.memoryOverhead", "4096")
#set cores of each executor and the driver -> less than avail -> more executors spawn
confCluster.set("spark.driver.cores", "16")
confCluster.set("spark.executor.cores", "16")
confCluster.set("spark.dynamicAllocation.enabled", "True")
confCluster.set("spark.dynamicAllocation.minExecutors", "15")
confCluster.set("spark.dynamicAllocation.maxExecutors", "15")
confCluster.set("yarn.nodemanager.vmem-check-enabled", "false")
repartition_count = 32

sc = SparkContext(conf=confCluster)
sqlContext = SQLContext(sc)

sc.setLogLevel("ERROR")

# spark_ara_df.search_similer_music(sc,song)

repartition_count = 32

debug_dict = {}
negjs = sc.accumulator(0)
nanjs = sc.accumulator(0)
nonpdjs = sc.accumulator(0)
negskl = sc.accumulator(0)
nanskl = sc.accumulator(0)
noninskl = sc.accumulator(0)
tic1 = int(round(time.time() * 1000))
list_to_vector_udf = udf(lambda l: Vectors.dense(l), VectorUDT())

#########################################################
#   Pre- Process RH and RP for Euclidean
#

rh = sc.textFile("features[0-9]*/out[0-9]*.rh", minPartitions=repartition_count)
rh = rh.map(lambda x: x.split(","))
kv_rhFirst = rh.map(lambda x: (x[0].replace(";","").replace(".","").replace(",","").replace(" ",""), list(x[1:]))).persist()

rp = sc.textFile("features[0-9]*/out[0-9]*.rp", minPartitions=repartition_count)
rp = rp.map(lambda x: x.split(","))
kv_rpFirst = rp.map(lambda x: (x[0].replace(";","").replace(".","").replace(",","").replace(" ",""), list(x[1:]))).persist()

#########################################################
#   Pre- Process BH for Euclidean
#

bh = sc.textFile("features[0-9]*/out[0-9]*.bh", minPartitions=repartition_count)
bh = bh.map(lambda x: x.split(";"))
kv_bhFirst = bh.map(lambda x: (x[0].replace(";","").replace(".","").replace(",","").replace(" ",""), x[1], Vectors.dense(x[2].replace(' ', '').replace('[', '').replace(']', '').split(',')))).persist()
#########################################################
#   Pre- Process Notes for Levenshtein
#

notes = sc.textFile("features[0-9]*/out[0-9]*.notes", minPartitions=repartition_count)
notes = notes.map(lambda x: x.split(';'))
notes = notes.map(lambda x: (x[0].replace(";","").replace(".","").replace(",","").replace(" ",""), x[1], x[2], x[3].replace("10",'K').replace("11",'L').replace("0",'A').replace("1",'B').replace("2",'C').replace("3",'D').replace("4",'E').replace("5",'F').replace("6",'G').replace("7",'H').replace("8",'I').replace("9",'J')))
notesFirst = notes.map(lambda x: (x[0], x[1], x[2], x[3].replace(',','').replace(' ',''))).persist()


#########################################################
#   Pre- Process Chroma for cross-correlation
#

chroma = sc.textFile("features[0-9]*/out[0-9]*.chroma", minPartitions=repartition_count)
chroma = chroma.map(lambda x: x.replace(' ', '').replace(';', ','))
chroma = chroma.map(lambda x: x.replace('.mp3,', '.mp3;').replace('.wav,', '.wav;').replace('.m4a,', '.m4a;').replace('.aiff,', '.aiff;').replace('.aif,', '.aif;').replace('.au,', '.au;').replace('.flac,', '.flac;').replace('.ogg,', '.ogg;'))
chroma = chroma.map(lambda x: x.split(';'))
#try to filter out empty elements
chroma = chroma.filter(lambda x: (not x[1] == '[]') and (x[1].startswith("[[0.") or x[1].startswith("[[1.")))
chromaRdd = chroma.map(lambda x: (x[0].replace(";","").replace(".","").replace(",","").replace(" ",""),(x[1].replace(' ', '').replace('[', '').replace(']', '').split(','))))
chromaVec = chromaRdd.map(lambda x: (x[0], Vectors.dense(x[1])))
chromaDfFirst = sqlContext.createDataFrame(chromaVec, ["id", "chroma"]).persist()

#########################################################
#   Pre- Process MFCC for SKL and JS and Euc
#

mfcc = sc.textFile("features[0-9]*/out[0-9]*.mfcckl", minPartitions=repartition_count)            
mfcc = mfcc.map(lambda x: x.replace(' ', '').replace(';', ','))
mfcc = mfcc.map(lambda x: x.replace('.mp3,', '.mp3;').replace('.wav,', '.wav;').replace('.m4a,', '.m4a;').replace('.aiff,', '.aiff;').replace('.aif,', '.aif;').replace('.au,', '.au;').replace('.flac,', '.flac;').replace('.ogg,', '.ogg;'))
mfcc = mfcc.map(lambda x: x.split(';'))
mfcc = mfcc.map(lambda x: (x[0].replace(";","").replace(".","").replace(",","").replace(" ",""), x[1].replace('[', '').replace(']', '').split(',')))
mfccVec = mfcc.map(lambda x: (x[0], Vectors.dense(x[1])))
mfccDfMergedFirst = sqlContext.createDataFrame(mfccVec, ["id", "features"]).persist()

#Force Transformation
#kv_rp.count()
#kv_rh.count()
#kv_bh.count()
#notes.count()
#mfccDfMerged.count()
#chromaDf.count()

# song = "/root/sim/music/Aerosmith/O, Yeah! Ultimate Aerosmith Hits [Disc 2]/09 I Don't Want To Miss A Thing.mp3"
song = "/root/sim/music/Oasis/Time Flies 1994-2009 [Disc 2]/2-11 Whatever.mp3"

def anaryze(song,file):   
    file = "featuresout/out" + file
    print("python3 mpi4py_ara_rhythm.py -rp -rh \"" + song +  "\" " + file)
    os.system("python3 mpi4py_ara_rhythm.py -rp -rh \"" + song +  "\" " + file)
    files.file(song,file)
    features.feathers(song,file)
    # for file in files:
    #     print(file)


#excel to sprak dataframe
def excel_to_dataframe():
    pd.set_option('display.max_rows', 5000)
    pd.set_option('display.max_columns', 5000)
    pandasdf = []
    excelFilePath = glob.glob('/root/sim/music/*')
    for path in excelFilePath:
        path = path + "/list.xlsx"
        if os.path.exists(path):
            print("ok")
            # if path == "/root/sim/music/901~1000/list.xlsx" or path == "/root/sim/music/801~900/list.xlsx" or path == "/root/sim/music/701~800/list.xlsx" or path == "/root/sim/music/601~700/list.xlsx" or path == "/root/sim/music/501~600/list.xlsx" or path == "/root/sim/music/301~400/list.xlsx" or path == "/root/sim/music/201~300/list.xlsx" or path == "/root/sim/music/101~200/list.xlsx" or path == "/root/sim/music/1~100/list.xlsx": 
            pandasdf.append(pd.read_excel(path,dtype=str))
    pandas = pd.concat(pandasdf)
    sparkdf = sqlContext.createDataFrame(pandas,['number','title','artist','url'])
    sparkdf.show(3000,truncate=False)
    return sparkdf

excelDataframe = excel_to_dataframe()

@similer.route('/',methods=['GET','POST'])
def search():
    time1 = int(round(time.time() * 1000))
    if request.method !=  'GET':
        return "plese input data"

    song = request.args.get('id','')  
    print("song name") 
    print(song) 

    outfile = glob.glob('featuresout/*')
    if not outfile :
        print('touch')
        p = pathlib.Path('./featuresout/0.rp')
        p.touch()
        print("touch end")
    max = 0
    for file in outfile:
        file = file.split("featuresout/out")
        print(int(file[1].split(".")[0]))
        if max < int(file[1].split(".")[0]):
            max = int(file[1].split(".")[0])
        # print(int(file.split(".")[0]))
    # line_count = int(subprocess.check_output(['wc', '-l', glob]).decode().split(' ')[0])
    if not os.path.isfile("./featuresout/out" + str(max) + ".rp"):
        p = pathlib.Path('./featuresout/out' + str(max) + '.rp')
        p.touch()

    if not os.path.isfile("./featuresout/out" + str(max) + ".rh"):
        p = pathlib.Path('./featuresout/out' + str(max) + '.rh')
        p.touch()


    print('featuresout/out' + str(max) +".rp")
    print(sum([1 for _ in open('featuresout/out' + str(max) +".rp")]))
    if 25 <= sum([1 for _ in open('featuresout/out' + str(max) +".rp")]):
        max += 1
    max = str(max)
    print(song.split("/root/sim/")[1])
    print('max')
    print(max)
    song = song.replace(" ","_")
    anaryze(song,max)
    if  os.path.isfile("./featuresout/out" + max + ".rp"):
        p = pathlib.Path('./featuresout/out' + max + '.rp')

    # rh = sc.textFile("featuresout/out"+ max + ".rh", minPartitions=repartition_count)
    rh = sc.textFile("featuresout/out[0-9]*.rh", minPartitions=repartition_count)
    rh = rh.map(lambda x: x.split(","))
    kv_rh= rh.map(lambda x: (x[0].replace(";","").replace(".","").replace(",","").replace(" ",""), list(x[1:]))).persist()
    kv_rh = kv_rh.union(kv_rhFirst).persist()
    if  os.path.isfile("./featuresout/out" + max + ".rh"):
        p = pathlib.Path('./featuresout/out' + max + '.rh')

    # rp = sc.textFile("featuresout/out"+ max + ".rp", minPartitions=repartition_count)
    rp = sc.textFile("featuresout/out[0-9]*.rp", minPartitions=repartition_count)
    rp = rp.map(lambda x: x.split(","))
    kv_rp= rp.map(lambda x: (x[0].replace(";","").replace(".","").replace(",","").replace(" ",""), list(x[1:]))).persist()
    kv_rp = kv_rp.union(kv_rpFirst).persist()

    #########################################################
    #   Pre- Process BH for Euclidean
    #
    if  not os.path.isfile("./featuresout/out" + max + ".bh"):
        p = pathlib.Path('./featuresout/out' + max + '.bh')

    # bh = sc.textFile("featuresout/out"+ max + ".bh", minPartitions=repartition_count)
    bh = sc.textFile("featuresout/out[0-9]*.bh", minPartitions=repartition_count)

    bh = bh.map(lambda x: x.split(";"))
    kv_bh = bh.map(lambda x: (x[0].replace(";","").replace(".","").replace(",","").replace(" ",""), x[1], Vectors.dense(x[2].replace(' ', '').replace('[', '').replace(']', '').split(',')))).persist()
    kv_bh = kv_bh.union(kv_bhFirst).persist()
    #   Pre- Process Notes for Levenshtein
    #
    if not os.path.isfile("./featuresout/out" + max + ".notes"):
        p = pathlib.Path('./featuresout/out' + max + '.notes')

    # notes = sc.textFile("featuresout/out"+ max + ".notes", minPartitions=repartition_count)
    notes = sc.textFile("featuresout/out[0-9]*.notes", minPartitions=repartition_count)

    notes = notes.map(lambda x: x.split(';'))
    notes = notes.map(lambda x: (x[0].replace(";","").replace(".","").replace(",","").replace(" ",""), x[1], x[2], x[3].replace("10",'K').replace("11",'L').replace("0",'A').replace("1",'B').replace("2",'C').replace("3",'D').replace("4",'E').replace("5",'F').replace("6",'G').replace("7",'H').replace("8",'I').replace("9",'J')))
    notes = notes.map(lambda x: (x[0], x[1], x[2], x[3].replace(',','').replace(' ',''))).persist()
    notes = notes.union(notesFirst).persist()



    #########################################################
    #   Pre- Process Chroma for cross-correlation
    #
    if not os.path.isfile("./featuresout/out" + max + ".chroma"):
        p = pathlib.Path('./featuresout/out' + max + '.chroma')

    # chroma = sc.textFile("featuresout/out"+ max + ".chroma", minPartitions=repartition_count)
    chroma = sc.textFile("featuresout/out[0-9]*.chroma", minPartitions=repartition_count)

    chroma = chroma.map(lambda x: x.replace(' ', '').replace(';', ','))
    chroma = chroma.map(lambda x: x.replace('.mp3,', '.mp3;').replace('.wav,', '.wav;').replace('.m4a,', '.m4a;').replace('.aiff,', '.aiff;').replace('.aif,', '.aif;').replace('.au,', '.au;').replace('.flac,', '.flac;').replace('.ogg,', '.ogg;'))
    chroma = chroma.map(lambda x: x.split(';'))
    #try to filter out empty elements
    chroma = chroma.filter(lambda x: (not x[1] == '[]') and (x[1].startswith("[[0.") or x[1].startswith("[[1.")))
    chromaRdd = chroma.map(lambda x: (x[0].replace(";","").replace(".","").replace(",","").replace(" ",""),(x[1].replace(' ', '').replace('[', '').replace(']', '').split(','))))
    chromaVec = chromaRdd.map(lambda x: (x[0], Vectors.dense(x[1])))
    chromaDf = sqlContext.createDataFrame(chromaVec, ["id", "chroma"])
    chromaDf = chromaDf.unionAll(chromaDfFirst).persist()

    #########################################################
    #   Pre- Process MFCC for SKL and JS and Euc
    #

    if not os.path.isfile("./featuresout/out" + max + ".mfcckl"):
        p = pathlib.Path('./featuresout/out' + max + '.mfcckl')
    # mfcc = sc.textFile("featuresout/out"+ max + ".mfcckl", minPartitions=repartition_count)       
    mfcc = sc.textFile("featuresout/out[0-9]*.mfcckl", minPartitions=repartition_count)            
     
    mfcc = mfcc.map(lambda x: x.replace(' ', '').replace(';', ','))
    mfcc = mfcc.map(lambda x: x.replace('.mp3,', '.mp3;').replace('.wav,', '.wav;').replace('.m4a,', '.m4a;').replace('.aiff,', '.aiff;').replace('.aif,', '.aif;').replace('.au,', '.au;').replace('.flac,', '.flac;').replace('.ogg,', '.ogg;'))
    mfcc = mfcc.map(lambda x: x.split(';'))
    mfcc = mfcc.map(lambda x: (x[0].replace(";","").replace(".","").replace(",","").replace(" ",""), x[1].replace('[', '').replace(']', '').split(',')))
    mfccVec = mfcc.map(lambda x: (x[0], Vectors.dense(x[1])))
    mfccDfMerged = sqlContext.createDataFrame(mfccVec, ["id", "features"])
    mfccDfMerged = mfccDfMerged.unionAll(mfccDfMergedFirst).distinct().persist()

    res = spark_ara_df.search_similer_music(sc,sqlContext,song,kv_rp,kv_rh,kv_bh,notes,mfccDfMerged,chromaDf,list_to_vector_udf,negjs,nanjs,nonpdjs,negskl,nanskl,noninskl)
    # res = res._jdf.schema().treeString()
    # res.write.json("result.json")
    res = res.join(excelDataframe, res.id.contains( F.concat(excelDataframe.number,lit("_"),F.regexp_replace(excelDataframe.title," ","_"))), how='left_outer').drop_duplicates(["id"]).persist()
    res = res.orderBy('aggregated', ascending=True)
    res.show(3000,truncate=False)
    kv_rp.unpersist()
    kv_rh.unpersist()
    kv_bh.unpersist()
    notes.unpersist()
    mfccDfMerged.unpersist()
    chromaDf.unpersist()
    res.unpersist()
    time2 = int(round(time.time() * 1000))
    print(time2 -time1)
    j = res.toJSON().map(lambda str:json.loads(str)).collect()
    js = json.dumps(j)
    with open("sample.json","w",) as f:
        json.dump(js,f)

    return js
if __name__ == "__main__":
    similer.run(host="0.0.0.0",port="11000",use_reloader=False)
   
    
    





