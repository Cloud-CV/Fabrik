## Using custom layers with Keras
  - Keras doesn't support the LRN layer used in Alexnet & many other models out of the box. 
  - To use custom layers, a reference to the custom layer is to be added when importing it.
  - The custom layer for LRN is located in keras_app/custom_layers
  
  ### Alexnet import for Keras
  ```
  from keras.models import model_from_json
  from keras_app.custom_layers.lrn import LRN

  model = open('alexnet.json', 'r')
  loadedModel = model.read()
  model.close()

  loadedModel = model_from_json(loadedModel, {'LRN': LRN})
  print (loadedModel.summary())
  ```
For more info, refer [this](https://github.com/keras-team/keras/issues/8612)
