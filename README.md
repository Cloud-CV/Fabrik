<img width="25%" src="/ide/static/img/logo.png" />

[![Join the chat at https://gitter.im/Cloud-CV/Fabrik](https://badges.gitter.im/Cloud-CV/Fabrik.svg)](https://gitter.im/Cloud-CV/Fabrik?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/Cloud-CV/Fabrik.svg?branch=master)](https://travis-ci.org/Cloud-CV/Fabrik)
[![Coverage Status](https://coveralls.io/repos/github/Cloud-CV/Fabrik/badge.svg?branch=master)](https://coveralls.io/github/Cloud-CV/Fabrik?branch=master)
[![Documentation Status](https://readthedocs.org/projects/markdown-guide/badge/?version=latest)](http://fabrik.readthedocs.io/en/latest/)

Fabrik is an online collaborative platform to build, visualize and train deep learning models via a simple drag-and-drop interface. It allows researchers to collectively develop and debug models using a web GUI that supports importing, editing and exporting networks to popular frameworks like Caffe, Keras, and TensorFlow.

<img src="/example/fabrik_demo.gif?raw=true">

This app is presently under active development and we welcome contributions. Please check out our [issues thread](https://github.com/Cloud-CV/IDE/issues) to find things to work on, or ping us on [Gitter](https://gitter.im/Cloud-CV/IDE).


## Installation Instructions

Setting up Fabrik on your local machine is very easy. You can setup Fabrik using two methods:

### Using Docker

#### Docker Installation
If you haven't installed Docker already: </br>

To install Docker for Windows [click here](https://docs.docker.com/docker-for-windows/install/).

To install Docker for Mac [click here](https://docs.docker.com/docker-for-mac/install/).

#### Fabrik Installation
1. Get the source code on to your machine via git.

    ```
    git clone https://github.com/Cloud-CV/Fabrik.git && cd Fabrik
    ```

2. Rename `settings/dev.sample.py` as `dev.py`.

    ```
    cp settings/dev.sample.py settings/dev.py
    ```

3. Build and run the Docker containers. This might take a while. You should now be able to access Fabrik at <http://0.0.0.0:8000>.

    ```
    docker-compose up --build
    ```

### Setup Authentication for Docker Environment
1. Go to Github Developer Applications and create a new application. [here](https://github.com/settings/developers)

2. For local deployments,the following should be used in the options:
    * Application name: Fabrik
    * Homepage URL: http://0.0.0.0:8000
    * Application description: Fabrik
    * Authorization callback URL: http://0.0.0.0:8000/accounts/github/login/callback/

3. Github will provide you with a Client ID and a Secret Key. Save these.

4. Create a superuser in django service of docker container

    ```
    docker-compose run django python manage.py createsuperuser
    ```

    Note: Before creating the superuser, make sure that django service of docker image is running. This can be done by executing ``` docker-compose up ``` followed by ``` Ctrl + C ``` to save docker configuration.

5. Open http://0.0.0.0:8000/admin and login with the credentials from step 4.

6. Setting up Social Accounts in django admin

    * Under ``` Social Accounts ```, open ``` Social applications ``` and click on ``` Add Social Application ```.

    * Choose  the ``` Provider ``` of social application as ``` Github ``` and  name it ``` Github ```.

    * Add the sites available to the right side, so github is allowed for the current site.

    * Copy and paste your ``` Client ID ``` and ``` Secret Key ``` into the apppropriate fields and Save.

7. Go to ``` Sites ``` tab and update the ``` Domain name ``` to ``` 0.0.0.0:8000 ```.


### Using Virtual Environment
1. First set up a virtualenv. Fabrik runs on Python2.7.

    ```
    sudo apt-get install python-pip python-dev python-virtualenv
    virtualenv --system-site-packages ~/Fabrik --python=python2.7
    source ~/Fabrik/bin/activate
    ```

2. Clone the repository via git

    ```
    git clone --recursive https://github.com/Cloud-CV/Fabrik.git && cd Fabrik
    ```

3. Rename settings/dev.sample.py as settings/dev.py and change credentials in settings/dev.py

    ```
    cp settings/dev.sample.py settings/dev.py
    ```

    * Change the hostname to ``` localhost ``` in settings/dev.py line 15. It should now look like this:  

    ```
    'HOST': os.environ.get("POSTGRES_HOST", 'localhost'), 
    ```

4. Install redis server  

    ```
    sudo apt-get install redis-server
    ```

    * Change the hostname to ``` localhost ``` in settings/common.py line 115.

        ```
        "CONFIG": {
            # replace redis hostname to localhost if running on local system
            "hosts": [("localhost", 6379)],
            "prefix": u'fabrik:',
            },
        ```

    * Replace celery result backend in settings/common.py line 122 with localhost.

        ```
        CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
        ```

    * Change celery broker URL and result backend hostname to ``` localhost ``` in ide/celery_app.py, line 8.

        ```
        app = Celery('app', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0', include=['ide.tasks'])
        ```

5. If you already have Caffe, Keras and TensorFlow installed on your computer, skip this step.
* For Linux users
    * Install Caffe, Keras and Tensorflow

        ```
        cd Fabrik/requirements
        yes Y | sh caffe_tensorflow_keras_install.sh
        ```

    * Open your ~/.bashrc file and append this line to the end

        ```      
        export PYTHONPATH=~/caffe/caffe/python:$PYTHONPATH
        ```

    * Save, exit and then run

        ```
        source ~/.bash_profile
        cd ..
        ```

* For Mac users
    * [Install Caffe](http://caffe.berkeleyvision.org/install_osx.html)
    * [Install Tensorflow](https://www.tensorflow.org/install/install_mac)
    * [Install Keras](https://keras.io/#installation)

6. Install dependencies
* For developers:

    ```
    pip install -r requirements/dev.txt
    ```

* For others:

    ```
    pip install -r requirements/common.txt
    ```

7. [Install postgres >= 9.5](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04)
* Setup postgres database
    * Start postgresql by typing ```sudo service postgresql start```
    * Now login as user postgres by running ```sudo -u postgres psql``` and type the commands below:

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

8. Install node modules

    ```
    npm install
    npm install --save-dev json-loader
    sudo npm install -g webpack@1.15.0
    ```

    * Run the command below in a separate terminal for hot-reloading, i.e. see the changes made to the UI in real time. 

    ```
    webpack --progress --watch --colors
    ```

9. Start celery worker

    ```
    celery -A ide worker --app=ide.celery_app  --loglevel=info
    ```

    The celery worker needs to be run in parallel to the django server in a separate terminal.

10. Start django application

    ```
    python manage.py runserver
    ```

    You should now be able to access Fabrik at <http://localhost:8000>.

### Setup Authentication for Virtual Environment
1. Go to Github Developer Applications and create a new application. [here](https://github.com/settings/developers)

2. For local deployments, the following should be used in the options:
    * Application name: Fabrik
    * Homepage URL: http://localhost:8000
    * Application description: Fabrik
    * Authorization callback URL: http://localhost:8000/accounts/github/login/callback/

3. Github will provide you with a client ID and secret Key, save these.

4. Create a superuser in django

    ```
    python manage.py createsuperuser
    ```

5. Start the application

    ```
    python manage.py runserver
    ```

6. Open http://localhost:8000/admin

7. Login with the credentials from step 4.

8. Setting up Social Accounts in django admin :

    * Under ```Social Accounts``` open ``` Social applications ```, click on ``` Add Social Application ```.

    * Choose  the ``` Provider ``` of social application as ``` Github ``` &  name it ``` Github ```.

    * Add the sites available to the right side, so github is allowed for the current site. This should be `localhost:8000` for local deployment.

    * Copy and paste your ``` Client ID ``` and ``` Secret Key ``` into the appropriate fields and Save.

9. From the django admin home page, go to `Sites` under the `Sites` category and update ``` Domain name ``` to ``` localhost:8000 ```.

Note: For testing, you will only need one authentication backend. However, if you want to try out Google's authentication,
then, you will need to follow the same steps as above, but switch out the Github for Google.


### Usage

```
python manage.py runserver
```

### Example
* Use `example/tensorflow/GoogleNet.pbtxt` for TensorFlow import
* Use `example/caffe/GoogleNet.prototxt` for Caffe import
* Use `example/keras/vgg16.json` for Keras import

### Tested models

The model conversion between currently supported frameworks is tested on some models.

Models                                                                      | Caffe | Keras | Tensorflow |
:--------------------------------------------------------------------------:|:-----:|:-----:|:----------:|
[Inception V3](http://arxiv.org/abs/1512.00567)                             |   √   |   √   |     √      |
[Inception V4](http://arxiv.org/abs/1512.00567)                             |   √   |   √   |     √      |
[ResNet 101](https://arxiv.org/abs/1512.03385)                              |   √   |   √   |     √      |
[VGG 16](http://arxiv.org/abs/1409.1556.pdf)                                |   √   |   √   |     √      |
[GoogLeNet](https://arxiv.org/pdf/1610.02357.pdf)                           |   √   |   ×   |     ×      |
[SqueezeNet](https://arxiv.org/pdf/1602.07360)                              |   √   |   ×   |     ×      |
[DenseNet](https://arxiv.org/abs/1608.06993)                                |   √   |   ×   |     ×      |
[AllCNN](https://arxiv.org/abs/1412.6806)                                   |   √   |   ×   |     ×      |
[AlexNet](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks)                                 |   √   |   √   |     √      |
[FCN32 Pascal](https://www.cv-foundation.org/openaccess/content_cvpr_2015/html/Long_Fully_Convolutional_Networks_2015_CVPR_paper.html) |   √   |   ×   |     ×      |
[YoloNet](https://arxiv.org/abs/1506.02640)                                 |   √   |   √   |     √      |
[Pix2Pix](https://github.com/phillipi/pix2pix)                              |   √   |   ×   |     ×      |
[VQA](https://github.com/iamaaditya/VQA_Demo)                               |   √   |   √   |     √      |
[Denoising Auto-Encoder](https://blog.keras.io/building-autoencoders-in-keras.html)                               |   ×   |   √   |     √      |

Note: For models that use a custom LRN layer (Alexnet), Keras expects the custom layer to be passed when it is loaded from json. LRN.py is located in keras_app/custom_layers. [Alexnet import for Keras](https://github.com/Cloud-CV/Fabrik/blob/master/tutorials/keras_custom_layer_usage.md)

### Documentation
* [Using a Keras model exported from Fabrik](https://github.com/Cloud-CV/Fabrik/blob/master/tutorials/keras_json_usage_1.md)
* [Loading a Keras model exported from Fabrik and printing its summary](https://github.com/Cloud-CV/Fabrik/blob/master/tutorials/keras_json_usage_2.md)
* [Using an Exported Caffe Model](https://github.com/Cloud-CV/Fabrik/blob/master/tutorials/caffe_prototxt_usage_1.md)
* [Loading a Caffe model in python and printing its parameters and output size](https://github.com/Cloud-CV/Fabrik/blob/master/tutorials/caffe_prototxt_usage_2.md)
* [List of models tested with Fabrik](https://github.com/Cloud-CV/Fabrik/blob/master/tutorials/tested_models.md)
* [Adding model to the Fabrik model zoo](https://github.com/Cloud-CV/Fabrik/blob/master/tutorials/adding_new_model.md)
* [Adding new layers](https://github.com/Cloud-CV/Fabrik/blob/master/tutorials/adding_new_layers.md)
* [Using custom layers with Keras](https://github.com/Cloud-CV/Fabrik/blob/master/tutorials/keras_custom_layer_usage.md)
* [Linux installation walk-through](https://www.youtube.com/watch?v=zPgoben9D1w)

### License

This software is licensed under GNU GPLv3. Please see the included License file. All external libraries, if modified, will be mentioned below explicitly.
