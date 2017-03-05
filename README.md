# IDE

[![Join the chat at https://gitter.im/Cloud-CV/IDE](https://badges.gitter.im/Cloud-CV/IDE.svg)](https://gitter.im/Cloud-CV/IDE?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This is a React+Django webapp with a simple drag and drop interface to build and configure deep neural networks with support for export of model configuration files to caffe and tensorflow. It also supports import from these frameworks to visualize different model architectures. Our motivation is to build an online IDE where researchers can share models and collaborate without having to deal with deep learning code.

![alt text](https://github.com/Cloud-CV/IDE/blob/master/example/snapshot.png "IDE Snapshot")

This app is presently under active development and we welcome contributions. Please check out our [issues thread](https://github.com/Cloud-CV/IDE/issues) to find things to work on, or ping us on [Gitter](https://gitter.im/batra-mlp-lab/CloudCV). 

### Requirements
1. install [caffe](http://caffe.berkeleyvision.org/installation.html)
2. install [tensorflow](https://www.tensorflow.org/versions/r0.10/get_started/os_setup.html#pip-installation)

### Build instructions
1. `git clone https://github.com/Cloud-CV/IDE.git`
2. `git submodule init`
3. `git submodule update`
4. `pip install -r requirements.txt`
5. `npm install`

### Usage
`python manage.py runserver`

### Note
* While installing tensorflow through conda use tensorflow version >= 0.12.0 in requirements.txt

### Example
* Use `example/GoogleNet.pbtxt` for tensorflow import
* Use `example/GoogleNet.prototxt` for caffe import

### License

This software is licensed under GNU GPLv3. Please see the included License file. All external libraries, if modified, will be mentioned below explicitly.
