## Tensorflow upgrade

Current Version: 1.4.1

Versions Tested:
 - **1.5.0**
 - **1.6.0**
 - **1.7.0**
 - **1.8.0** 
    - **Remarks:** Upgrading to version 1.5.0-1.8.0 breaks no functionality and produces no error when running with Travis CI. Importing data models also do not seem to produce any problems.
 - **1.9.0** & **1.10.1** 
    - **Errors encountered:** An `ImportError: dlopen: cannot load any more object with static TLS_` was thrown when trying to run the project.
    - **Cause of error:** This error seems to be thrown due to a wrong order of import statements, which is thought to be a bug as none of the breaking changes from v1.8.0 to 1.9.0 apply ([source](https://github.com/tensorflow/tensorflow/blob/master/RELEASE.md#breaking-changes-2)). On upgrading to 1.12.0, this issue no longer persists. 
    - **Travis CI log:** [1.9.0](https://travis-ci.com/c0derlint/Fabrik/builds/90459224), [1.10.1](https://travis-ci.com/c0derlint/Fabrik/builds/90600645)
 - **1.12.0** (latest version) 
    - **Remarks:** Travis CI built successfully on this version of tensorflow. No functionality seems to be lost.
    - **Tests performed:**
        - Importing models from model zoo.
        - Importing a custom model downloaded from internet.
        - Exporting a model locally and then importing it again.
        - Making a simple model.
        - Importing / Exporting models of caffe and keras

 ![Tensorflow 1.12.0 import](https://i.imgur.com/8CZpF5q.png)
