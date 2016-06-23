# CloudCV-IDE
###Build Instructions
1. pip install -r requirements.txt
2. npm install
3. Prepare mnsit dataset using this link https://github.com/BVLC/caffe/tree/master/examples/mnist
4. Copy the two datasets into `cloudcvIde/media/dataset/mnsit/` directory.  
   The directory structure should look like:  
   cloudcvIde/media/dataset/mnsit/  
                    mnist_train_lmdb  
                    mnist_test_lmdb
5. node ./cloudcvIde/index.js
6. python manage.py runserver
