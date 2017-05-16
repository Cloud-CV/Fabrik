# Generic dependencies
echo "Installing generic dependencies"
sudo apt-get install git libatlas-base-dev python-protobuf python-numpy python-scipy python-h5py unzip make libblas-dev liblapack-dev libatlas-base-dev gfortran python-pip python-dev
pip install numpy scipy scikit-image

#Caffe specific dependencies
echo "Installing caffe specific dependencies"
sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev libgflags-dev libgoogle-glog-dev liblmdb-dev protobuf-compiler
sudo apt-get install --no-install-recommends libboost-all-dev

#Download caffe
echo "Downloading caffe"
cd
mkdir caffe
cd caffe
wget https://github.com/BVLC/caffe/archive/25391bf9e0552740af8253c6d6fd484297889a49.zip
unzip -o 25391bf9e0552740af8253c6d6fd484297889a49.zip
rm 25391bf9e0552740af8253c6d6fd484297889a49.zip
mv caffe-25391bf9e0552740af8253c6d6fd484297889a49 caffe
cd caffe

#Install caffe
echo "Installing caffe"
cp Makefile.config.example Makefile.config
CPU_ONLY=1 USE_OPENCV=0 make all -j4

#Install pycaffe
echo "Install PyCaffe"
CPU_ONLY=1 USE_OPENCV=0 make pycaffe -j2

echo "export PYTHONPATH=$(pwd)/python:$PYTHONPATH" > ~/.bash_profile
source ~/.bash_profile

echo "#################### Caffe Install Complete! ####################"

echo "Installing Tensorflow dependencies"
sudo apt-get install python-pip python-dev

echo "Installing Tensorflow"
pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.12.1-cp27-none-linux_x86_64.whl

echo "#################### Tensorflow Install Complete! ####################"
