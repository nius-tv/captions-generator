FROM ubuntu:18.04

RUN apt-get update -y

RUN apt-get install -y locales # required by mocha
RUN apt-get install -y python3.5
RUN apt-get install -y python3-pip

RUN pip3 install google-cloud-error-reporting==0.33.0
RUN pip3 install pytest==3.2.1
RUN pip3 install pytest-mocha==0.1.0
RUN pip3 install PyYAML==5.2
RUN pip3 install watchdog==0.8.3

# Setup unicode support (required by mocha)
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install gcsfuse
RUN apt-get install -y curl
RUN apt-get install -y gnupg2
RUN apt-get install -y lsb-release

RUN export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s` && \
	echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | \
	tee /etc/apt/sources.list.d/gcsfuse.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

RUN apt-get update -y
RUN apt-get install -y gcsfuse

# Install gcloud
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | \
	tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

RUN apt-get install -y apt-transport-https
RUN apt-get install -y ca-certificates

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
	apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

RUN apt-get update -y
RUN apt-get install -y google-cloud-sdk

ADD . /app
