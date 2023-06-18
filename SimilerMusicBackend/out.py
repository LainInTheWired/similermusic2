# import api
import mpi4py_ara_features as features
from pathlib import Path, PurePath
import os
import mpi4py_ara_files as files


i = 0
j = 0
def anaryze(song,file):   
    file = "featuresout/out" + file
    print("python3 mpi4py_ara_rhythm.py -rp -rh" + song +  " " + file)
    os.system("python3 mpi4py_ara_rhythm.py -rp -rh '" + song +  "' " + file)
    files.file(song,file)
    features.feathers(song,file)
    # for file in files:
    #     print(file)

for song in Path('/root/sim/music/out').glob('**/*.mp3'):
    print(song)
    file = "featuresout/out" + str(j)
    os.system("python3 mpi4py_ara_rhythm.py -rp -rh '" + str(song) +  "' " + file)
    files.file(song,file)

    features.feathers(song,file)


    i += 1
    if i > 20 :
        j +=1
        i = 0