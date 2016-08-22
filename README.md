# IDE
This is a user interface to draw and configure deep neural networks and supports import/export of model configuration 
file from/to caffe/tensorflow deep learning frameworks

### Requirements
1. install [caffe](http://installing-caffe-the-right-way.wikidot.com/start)
2. install [tensorflow](https://www.tensorflow.org/versions/r0.10/get_started/os_setup.html#pip-installation)

### Build instructions
1. `git clone https://github.com/Cloud-CV/IDE.git`
2. `git submodule init`
3. `git submodule update`
4. `pip install -r requirements.txt`
5. `npm install`

### Usage
`python manage.py runserver`

### Example
* Use `example/GoogleNet.pbtxt` for tensorflow import
* Use `example/GoogleNet.prototxt` for caffe import
