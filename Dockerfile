FROM ubuntu:22.04

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 必要そうなものをinstall
RUN apt-get update && apt-get install -y --no-install-recommends wget build-essential libreadline-dev \ 
libncursesw5-dev libssl-dev libsqlite3-dev libgdbm-dev libbz2-dev liblzma-dev zlib1g-dev uuid-dev libffi-dev libdb-dev

RUN apt -y install build-essential libbz2-dev libdb-dev \
  libreadline-dev libffi-dev libgdbm-dev liblzma-dev \
  libncursesw5-dev libsqlite3-dev libssl-dev \
  zlib1g-dev uuid-dev tk-dev libc6-dev

#任意バージョンのpython install
# RUN wget --no-check-certificate https://www.python.org/ftp/python/3.9.5/Python-3.9.5.tgz \
# && tar -xf Python-3.9.5.tgz \
# && cd Python-3.9.5 \
# && ./configure --enable-optimizations\
# && make \
# && make install

RUN apt-get install -y python3 python3-pip

#サイズ削減のため不要なものは削除
RUN apt-get autoremove -y

#必要なpythonパッケージをpipでインストール
#RUN pip3 install --upgrade pip && pip3 install --no-cache-dir jupyterlab

#追加
RUN apt -y install  default-jre
RUN apt-get -y install libopenmpi-dev

#requirements.txtなら以下のように
ADD requirements.txt /root
RUN apt-get update && apt-get install -y ffmpeg


WORKDIR /root

RUN pip3 install -r requirements.txt
# RUN pip3.6 install --upgrade pip
# RUN pip3.6 install -r requirements.txt
# RUN apt-get -y install yum-utils
# RUN apt-get -y install epel-release
# RUN rpm -Va --nofiles --nodigest
#RUN apt-get -y install -skip-broken  https://download1.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm
# RUN apt-get -y install https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm
# #RUN rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm
# RUN apt-get -y update
# RUN apt-get -y install ffmpeg ffmpeg-devel
RUN apt-get -y install zip
RUN wget  https://www.parallelpython.com/downloads/pp/pp-1.6.4.4.zip
# RUN ls -la
RUN unzip pp-1.6.4.4.zip

# RUN cd pp-1.6.4.4
# RUN python3 setup.py install
# RUN apt-get update && apt-get install -y ffmpeg
