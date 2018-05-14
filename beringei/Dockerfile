FROM ubuntu:16.04

RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN apt update && \
	apt -y install build-essential libgflags-dev libgtest-dev vim && \
	apt clean && \
	apt -y autoremove && \
	rm -rf /var/lib/apt/lists/*

WORKDIR /projects
COPY setup_ubuntu.sh /projects/
RUN /projects/setup_ubuntu.sh

