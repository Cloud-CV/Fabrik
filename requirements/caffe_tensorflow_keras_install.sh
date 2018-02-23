# Generic dependencies
echo "Installing generic dependencies"
sudo apt-get install git libatlas-base-dev python-protobuf python-numpy python-scipy python-h5py unzip make libblas-dev liblapack-dev libatlas-base-dev gfortran python-pip python-dev
pip install numpy scipy scikit-image

#Caffe specific dependencies
echo "Installing caffe specific dependencies"
sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev libgflags-dev libgoogle-glog-dev liblmdb-dev protobuf-compiler cmake
sudo apt-get install --no-install-recommends libboost-all-dev

if [ ! -d $HOME/caffe/caffe ]; then
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
		mkdir build
		cd build
		cmake -DCPU_ONLY=1 -DBUILD_python_layer=1 ..
		make -j"$(nproc)"
		
		echo "export PYTHONPATH=$PYTHONPATH:$HOME/caffe/caffe/python" >> ~/.bash_profile
fi
echo "#################### Caffe Install Complete! ####################"

echo "Installing Tensorflow dependencies"
sudo apt-get install python-pip python-dev google-perftools
export LD_PRELOAD="/usr/lib/libtcmalloc.so.4" 

echo "Installing Tensorflow"
pip install tensorflow==1.4.1

echo "#################### Tensorflow Install Complete! ####################"

echo "Installing Keras"
pip install keras==2.0.8

echo "#################### Keras Install Complete! ####################"
