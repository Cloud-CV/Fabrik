FROM node:6

RUN mkdir -p /code
WORKDIR /code
ENV PYTHONUNBUFFERED 1

COPY package.json /code
RUN npm install
RUN npm install -g webpack

# Install Python.
RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        unzip \	
        wget \
	supervisor \
	nginx \
        libatlas-base-dev \
        libboost-all-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libopencv-dev \
        libprotobuf-dev \
        libsnappy-dev \
        protobuf-compiler \
        python-dev \
        python-numpy \
        python-pip \
        python-setuptools \
        python-scipy && \
    rm -rf /var/lib/apt/lists/*

# Install Caffe
RUN cd /root &&\
	wget https://github.com/BVLC/caffe/archive/25391bf9e0552740af8253c6d6fd484297889a49.zip &&\
	unzip -o 25391bf9e0552740af8253c6d6fd484297889a49.zip &&\
	rm 25391bf9e0552740af8253c6d6fd484297889a49.zip && \
	mv caffe-25391bf9e0552740af8253c6d6fd484297889a49 caffe &&\
	cd caffe &&\
	pip install scikit-image &&\
    mkdir build && cd build && \
    cmake -DCPU_ONLY=1 -DWITH_PYTHON_LAYER=1 .. && \
    make -j"$(nproc)"

# Set up Caffe environment variables
ENV CAFFE_ROOT=/root/caffe
ENV PYCAFFE_ROOT=$CAFFE_ROOT/python
ENV PYTHONPATH=$PYCAFFE_ROOT:$PYTHONPATH \
	PATH=$CAFFE_ROOT/build/tools:$PYCAFFE_ROOT:$PATH

RUN echo "$CAFFE_ROOT/build/lib" >> /etc/ld.so.conf.d/caffe.conf && ldconfig

# Install Tensorflow
RUN pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.12.1-cp27-none-linux_x86_64.whl

# Install Keras
RUN pip install git+https://github.com/fchollet/keras.git

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY docker/prod/nginx.conf /etc/nginx/sites_available/default
COPY docker/prod/supervisor.conf /etc/supervisor/conf.d/

# Install Fabrik dependencies
COPY /requirements /code/requirements
RUN pip install -r requirements/prod.txt

COPY . /code

EXPOSE 8000
CMD ["/bin/bash", "/code/docker/prod/container-start.sh"]
