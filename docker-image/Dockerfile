FROM debian:jessie

MAINTAINER Martin Hecker <martin.hecker@kit.edu>

RUN echo "deb http://http.debian.net/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list
RUN apt-get --yes update
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install --yes -t jessie-backports ca-certificates-java
RUN apt-get install --yes -t jessie-backports openjdk-8-jdk
RUN apt-get install --yes junit junit4 dejagnu gcj-jdk && apt-get clean
RUN update-java-alternatives -s java-1.8.0-openjdk

# Python-Stuff
RUN apt-get update -y
RUN apt-get install --yes python3            python               && apt-get clean
RUN apt-get install --yes python3-requests                        && apt-get clean
RUN apt-get install --yes python3-pip                             && apt-get clean
RUN apt-get install --yes python3-six        python-six           && apt-get clean

RUN apt-get install --yes python3-responses                       && apt-get clean
RUN apt-get install --yes python3-xlrd                            && apt-get clean
RUN apt-get install --yes python3-simplejson python-simplejson    && apt-get clean

RUN python3 -m pip install --upgrade pip
RUN pip3 install numpy scipy matplotlib ipython pandas
RUN sed -i -e 's/^backend      : \(\(TkAgg\)\|\(tkagg\)\)$/backend      : Agg/g' /usr/local/lib/python3.4/dist-packages/matplotlib/mpl-data/matplotlibrc

# set up some font cache once and for all
RUN python3 -c "from matplotlib.font_manager import FontManager"

# Requirements for statsmodels
RUN apt-get install --yes python3-patsy                           && apt-get clean

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install statsmodels
RUN pip3 install scikit-learn
RUN pip3 install numdifftools
RUN pip3 install arch

# more recent versions of numdifftools pull a whole lot of newer versions of other packages than those already installed from the debian packages (numpy, scipy), we don't want that
RUN pip3 install numdifftools==0.7.7

RUN echo "praktomat:x:1001:1001:,,,:/home/praktomat:/bin/bash" >> /etc/passwd
RUN echo "praktomat:x:1001:tester" >> /etc/group

COPY checkstyle-6.19-all.jar /srv/praktomat/contrib/checkstyle-6.19-all.jar
COPY jplag-2.11.8-SNAPSHOT-jar-with-dependencies.jar /srv/praktomat/contrib/jplag-2.11.8-SNAPSHOT-jar-with-dependencies.jar

# We use a fresh tmpfs with /home in each container
RUN chmod 1777 /home
