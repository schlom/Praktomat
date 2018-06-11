FROM debian:jessie

MAINTAINER Martin Hecker <martin.hecker@kit.edu>

RUN echo "deb http://http.debian.net/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list
RUN apt-get --yes update
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install --yes -t jessie-backports ca-certificates-java
# Install Oracle Java 8
RUN echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | tee /etc/apt/sources.list.d/webupd8team-java.list
RUN echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | tee -a /etc/apt/sources.list.d/webupd8team-java.list
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886
RUN apt-get update
RUN echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
RUN echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --force-yes oracle-java8-installer
RUN apt-get install -y oracle-java8-set-default
#RUN apt-get install --yes -t jessie-backports openjdk-8-jdk
RUN apt-get install --yes junit junit4 dejagnu gcj-jdk && apt-get clean
#RUN update-java-alternatives -s java-1.8.0-openjdk

# Python-Stuff
RUN apt-get update -y
RUN apt-get install --yes python3            python               && apt-get clean
RUN apt-get install --yes                    ipython              && apt-get clean
RUN apt-get install --yes python3-requests                        && apt-get clean
RUN apt-get install --yes python3-pip                             && apt-get clean
RUN apt-get install --yes python3-six        python-six           && apt-get clean
RUN apt-get install --yes python3-responses                       && apt-get clean
RUN apt-get install --yes python3-xlrd                            && apt-get clean
RUN apt-get install --yes python3-simplejson python-simplejson    && apt-get clean
RUN apt-get install --yes -t jessie-backports python3-numpy python-numpy    && apt-get clean

RUN python3 -m pip install --upgrade pip
#RUN pip3 install numpy
RUN pip3 install scipy
RUN pip3 install matplotlib
RUN pip3 install ipython
RUN apt-get install --yes -t jessie-backports python3-pandas python-pandas    && apt-get clean
#RUN pip3 install pandas
RUN sed -i -e 's/^backend      : \(\(TkAgg\)\|\(tkagg\)\)$/backend      : Agg/g' /usr/local/lib/python3.4/dist-packages/matplotlib/mpl-data/matplotlibrc

# set up some font cache once and for all
RUN python3 -c "from matplotlib.font_manager import FontManager"

# Requirements for statsmodels
RUN pip3 install statsmodels
RUN pip3 install scikit-learn
RUN pip3 install numdifftools
RUN pip3 install Cython
RUN pip3 install h5py
RUN pip3 install arch==3.1

RUN echo "praktomat:x:1001:1001:,,,:/home/praktomat:/bin/bash" >> /etc/passwd
RUN echo "praktomat:x:1001:tester" >> /etc/group

COPY checkstyle-6.19-all.jar /srv/praktomat/contrib/checkstyle-6.19-all.jar
COPY jplag-2.11.8-SNAPSHOT-jar-with-dependencies.jar /srv/praktomat/contrib/jplag-2.11.8-SNAPSHOT-jar-with-dependencies.jar

# We use a fresh tmpfs with /home in each container
RUN chmod 1777 /home

ENV JAVA_HOME /usr/lib/jvm/java-8-oracle
