FROM debian:jessie

MAINTAINER Joachim Breitner <breitner@kit.edu>

RUN echo "deb http://http.debian.net/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list
RUN apt-get --yes update
RUN apt-get install --yes -t jessie-backports openjdk-8-jdk
RUN apt-get install --yes junit junit4 dejagnu gcj-jdk && apt-get clean
RUN update-java-alternatives -s java-1.8.0-openjdk

# Python-Stuff
RUN apt-get update -y
RUN apt-get install --yes python3            python               && apt-get clean
RUN apt-get install --yes ipython3           ipython              && apt-get clean
RUN apt-get install --yes python3-requests                        && apt-get clean
RUN apt-get install --yes python3-pip                             && apt-get clean
RUN apt-get install --yes python3-six        python-six           && apt-get clean
RUN apt-get install --yes python3-numpy                           && apt-get clean
RUN apt-get install --yes python3-scipy                           && apt-get clean
RUN apt-get install --yes python3-pandas                          && apt-get clean

RUN apt-get install --yes python3-matplotlib                      && apt-get clean
RUN sed -i -e 's/^backend      : TkAgg$/backend      : Agg/g' /etc/matplotlibrc

RUN apt-get install --yes python3-responses                       && apt-get clean
RUN apt-get install --yes python3-xlrd                            && apt-get clean

# Requirements for statsmodels
RUN apt-get install --yes python3-patsy                           && apt-get clean

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install statsmodels
RUN pip3 install scikit-learn

# more recent versions of numdifftools pull a whole lot of newer versions of other packages than those already installed from the debian packages (numpy, scipy), we don't want that
RUN pip3 install numdifftools==0.7.7

RUN echo "praktomat:x:1001:1001:,,,:/home/praktomat:/bin/bash" >> /etc/passwd
RUN echo "praktomat:x:1001:tester" >> /etc/group

COPY checkstyle-6.19-all.jar /srv/praktomat/contrib/checkstyle-6.19-all.jar
COPY jplag-2.11.8-SNAPSHOT-jar-with-dependencies.jar /srv/praktomat/contrib/jplag-2.11.8-SNAPSHOT-jar-with-dependencies.jar

# We use a fresh tmpfs with /home in each container
RUN chmod 1777 /home
