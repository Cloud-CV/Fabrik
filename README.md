# Fabrik

[![Join the chat at https://gitter.im/Cloud-CV/IDE](https://badges.gitter.im/Cloud-CV/IDE.svg)](https://gitter.im/Cloud-CV/IDE?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/Cloud-CV/Fabrik.svg?branch=master)](https://travis-ci.org/Cloud-CV/Fabrik)

This is a React+Django webapp with a simple drag and drop interface to build and configure deep neural networks with support for export of model configuration files to caffe and tensorflow. It also supports import from these frameworks to visualize different model architectures. Our motivation is to build an online IDE where researchers can share models and collaborate without having to deal with deep learning code.

### Interface
GoogLeNet             |  ResNet 
:-------------------------:|:-------------------------:
![](https://github.com/Cloud-CV/Fabrik/blob/master/example/screenshot_1.png)  |  ![](https://github.com/Cloud-CV/Fabrik/blob/master/example/screenshot_2.png)

Tooltips             |  Edit layer parameters and Layers Dropdown 
:-------------------------:|:-------------------------:
![](https://github.com/Cloud-CV/Fabrik/blob/master/example/screenshot_3.png)  |  ![](https://github.com/Cloud-CV/Fabrik/blob/master/example/screenshot_4.png)


This app is presently under active development and we welcome contributions. Please check out our [issues thread](https://github.com/Cloud-CV/IDE/issues) to find things to work on, or ping us on [Gitter](https://gitter.im/batra-mlp-lab/CloudCV). 

### How to setup
1. First set up a virtualenv
    ```
    sudo apt-get install python-pip python-dev python-virtualenv 
    virtualenv --system-site-packages ~/Fabrik
    source ~/Fabrik/bin/activate
    ```
    
2. Clone the repository
    ```
    git clone --recursive https://github.com/Cloud-CV/Fabrik.git
    ```
    
3. If you have Caffe and Tensorflow already installed on your computer, skip this step
    ```
    cd Fabrik/requirements
    sh caffe_tensoflow_install.sh
    ```
4. Install dependencies
* For developers:
    ```
    pip install -r requirements/dev.txt
    ```
* Others:
    ```
    pip install -r requirements/common.txt
    ```
```
npm install
```

### Usage
```
python manage.py runserver
```

### Example
* Use `example/GoogleNet.pbtxt` for tensorflow import
* Use `example/GoogleNet.prototxt` for caffe import

### License

This software is licensed under GNU GPLv3. Please see the included License file. All external libraries, if modified, will be mentioned below explicitly.
