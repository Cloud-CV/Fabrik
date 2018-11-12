## Using an Exported Tensorflow Model

In order to export a Tensorflow model from Fabrik:

1. First, select the 2nd button from the left in the Actions section of the sidebar.
<img src="https://raw.githubusercontent.com/Cloud-CV/Fabrik/master/tutorials/exportbutton.png">

2. A drop-down list should appear. Select Tensorflow.
    * This should download a pbtxt file to your computer.  
    <img src="https://raw.githubusercontent.com/Cloud-CV/Fabrik/master/tutorials/export_tensorflow.png">

3. Rename the file to ```model.pbtxt```.

4. Load the model from the ProtoBuf file using the following code:

    ```
    import tensorflow as tf
    from google.protobuf import text_format

    # read the graphdef from the model file
    with open('model.pbtxt', 'r') as model_file:
	    model_protobuf = text_format(model_file.read(),
		    	                 tf.Graphdef())
    
    # import the graphdef into the default graph
    tf.import_graph_def(model_protobuf)
    ```

### Code template

[The code template](../example/tensorflow/code_template/tensorflow_sample.py) loads the model from a pbtxt file into the default graph. Additional operations like layers and optimizers can be then built onto the graph as required.

To run the code, run:

```
python tensorflow_sample.py model.pbtxt
```

Replace ```model.pbtxt``` with the model file that you want to use.
