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
