<img width="25%" src="/ide/static/img/logo.png" />

[![Join the chat at https://gitter.im/Cloud-CV/IDE](https://badges.gitter.im/Cloud-CV/IDE.svg)](https://gitter.im/Cloud-CV/IDE?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/Cloud-CV/Fabrik.svg?branch=master)](https://travis-ci.org/Cloud-CV/Fabrik)
[![Coverage Status](https://coveralls.io/repos/github/Cloud-CV/Fabrik/badge.svg?branch=master)](https://coveralls.io/github/Cloud-CV/Fabrik?branch=master)

Fabrik is an online collaborative platform to build, visualize and train deep learning models via a simple drag-and-drop interface. It allows researchers to collaboratively develop and debug models using a web GUI that supports importing, editing and exporting networks written in widely popular frameworks like Caffe, Keras, and TensorFlow.

### Interface
<img src="/example/fabrik_demo.gif?raw=true">

This app is presently under active development and we welcome contributions. Please check out our [issues thread](https://github.com/Cloud-CV/IDE/issues) to find things to work on, or ping us on [Gitter](https://gitter.im/Cloud-CV/IDE). 

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
    
3. If you have Caffe, Keras and Tensorflow already installed on your computer, skip this step
    * For Linux users
        ```
        cd Fabrik/requirements
        yes Y | sh caffe_tensorflow_keras_install.sh
        ```
        Open your ~/.bashrc file and append this line at the end
        ```        
        export PYTHONPATH=~/caffe/caffe/python:$PYTHONPATH
        ```
        Save, exit and then run
        ```
        source ~/.bash_profile
        cd .. 
        ```
    * For Mac users
        * [Install Caffe](http://caffe.berkeleyvision.org/install_osx.html)
        * [Install Tensorflow](https://www.tensorflow.org/versions/r0.12/get_started/os_setup#virtualenv_installation)
        * [Install Keras](https://keras.io/#installation)
4. Install dependencies
* For developers:
    ```
    pip install -r requirements/dev.txt
    ```
* Others:
    ```
    pip install -r requirements/common.txt
    ```
5. [Install postgres >= 9.5](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04)
* Setup postgres database
    * Start postgresql by typing ```sudo service postgresql start```
    * Now login as user postgres by running ```sudo -u postgres psql``` and type the commands below
    
    ```
      CREATE DATABASE fabrik;
      CREATE USER admin WITH PASSWORD 'fabrik';
      ALTER ROLE admin SET client_encoding TO 'utf8';
      ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
      ALTER ROLE admin SET timezone TO 'UTC';
      ALTER USER admin CREATEDB;
    ```
    * Exit psql by typing in \q and hitting enter. 
* Migrate
    ```
    
    python manage.py makemigrations caffe_app
    python manage.py migrate
    ```
6. Install node modules
```
npm install
sudo npm install -g webpack
webpack --progress --watch --colors
```

### Usage
```
KERAS_BACKEND=theano python manage.py runserver
```

### Example
* Use `example/tensorflow/GoogleNet.pbtxt` for tensorflow import
* Use `example/caffe/GoogleNet.prototxt` for caffe import
* Use `example/keras/vgg16.json` for keras import

### Documentation
* [Using a Keras model exported from Fabrik](https://github.com/Cloud-CV/Fabrik/blob/master/tutorials/keras_json_usage.md)
* [List of models tested with Fabrik](https://github.com/Cloud-CV/Fabrik/blob/master/tutorials/tested_models.md)
* [Adding model to the Fabrik model zoo](https://github.com/Cloud-CV/Fabrik/blob/master/tutorials/AddingNewModel.md)
* [Linux installation walk-through](https://www.youtube.com/watch?v=zPgoben9D1w)

### License

This software is licensed under GNU GPLv3. Please see the included License file. All external libraries, if modified, will be mentioned below explicitly.
