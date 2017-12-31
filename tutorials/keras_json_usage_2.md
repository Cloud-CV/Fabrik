### Use exported model in Keras

#### To export the model for Keras in Fabrik

- Click on the export button in the Actions section of the sidebar.
<img src="exportbutton.png">

- Select Keras option from the dropdown list.
    - A JSON file will be downloaded to your computer. It may take a while though.
<img src="exportdropdown.png">

- Rename the file to ```kerasModel.json```.

#### Load the exported model in python and show it's summary.

- Open a terminal and cd into the directory where the ```kerasModel.json``` is saved.
- Do ```touch kerasModelLoader.py```.
- Open the ```kerasModelLoader.py``` in any text editor.
- Type the following code into the editor.
```
#import keras' json model loader.
from keras.models import model_from_json

#Open the json file.
model = open('kerasModel.json', 'r')

#Read and close the json file.
loadedModel = model.read()
model.close()

#Load model from json file content.
loadedModel = model_from_json(loadedModel)

#Print the summary 
print (loadedModel.summary())
```

- Save the file at the same location where the kerasModel.json is saved and close the text editor.
- Switch to the terminal we were using earlier.
- Type ```python kerasModelLoader.py```.
- Congrats! You should see a summary of the exported model.
- You can further use the model for training/testing purpose. Read about it more [here](keras_json_usage_1.md).
