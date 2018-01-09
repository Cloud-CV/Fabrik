## Use exported model in Caffe

### To export the model for Caffe in Fabrik

- Click on the export button in the Actions section of the sidebar.

<img src="https://raw.githubusercontent.com/Cloud-CV/Fabrik/master/tutorials/exportbutton.png">

- Select Caffe option from the dropdown list.
    - A JSON file will be downloaded to your computer. It may take a while though.

<img src="https://raw.githubusercontent.com/Cloud-CV/Fabrik/master/tutorials/exportcaffe.png">

- Rename the file to ```caffeModel.prototxt```.

### Load the exported model in python and show it's parameters and output sizes.

- Open a terminal and cd into the directory where the ```caffeModel.prototxt``` is saved.
- Do ```touch caffeLoader.py```.
- Open the ```caffeLoader.py``` in any text editor.
- Type the following code into the editor.
```
import caffe
import numpy as np
from numpy import prod, sum
from pprint import pprint

caffe.set_mode_cpu()                 # Change the mode cpu/gpu according to your caffe installation

def model_details (model):
    net = caffe.Net(model, caffe.TEST)
    print "########################### Caffe Model Loaded ###########################"
    print "\nLayer-wise parameters: \n"
    pprint([(k, v[0].data.shape) for k, v in net.params.items()])
    print "\nTotal number of parameters: " + str(sum([prod(v[0].data.shape) for k, v in net.params.items()]))
    
model = "model.prototxt"            # Change name and path of the model as and if required 

model_details(model)

```

- Save the file at the same location where the ```model.prototxt``` file is saved and close the text editor.
- Switch to the terminal we were using earlier.
- Type ```python caffeLoader.py```.
- Congrats! You should see the model's parameters and output sizes.
- You can further use the model for training/testing purpose. Read about it more [here](caffe_prototxt_usage_1.md).