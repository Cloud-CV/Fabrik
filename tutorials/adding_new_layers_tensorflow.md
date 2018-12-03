## Exporting and Importing layer - Tensorflow

Follow the guide [here](adding_new_layers.md) to add your new layer to Fabrik's frontend. Then follow through this guide to add support for importing and exporting your layer for Tensorflow.


#### Importing a layer

- Open [import_graphdef.py](https://github.com/Cloud-CV/Fabrik/blob/master/tensorflow_app/views/import_graphdef.py)

    - Add your layer to one of these four dictionaries that map Tensorflow ops to Caffe layers:
        - `op_layer_map` : if the op has can be mapped to a Caffe layer directly
        - `activation_map` : if the op is a simple activation
        - `name_map` : if the op type can be inferred from the name of the op
        - `initializer_map` : if the op is an initializer

        ```diff
        name_map = {'flatten': 'Flatten',
                    'lrn': 'LRN', 
                    ...
        +           'dropout': 'Dropout' 
        }
        ```

    - Inside the loop `for node in graph.get_operations()`, write code to get any layer parameters needed and build the layer.

    ```
    elif layer['type'][0] == 'Dropout':
        if ('rate' in node.node_def.attr):
            layer['params']['rate'] = node.get_attr('rate')
        if ('seed' in node.node_def.attr):
            layer['params']['seed'] = node.get_attr('seed')
        if ('training' in node.node_def.attr):
            layer['params']['trainable'] = node.get_attr('training')
    ```

#### Exporting a layer

Fabrik exports Tensorflow models using Keras. [See this guide](adding_new_layers_keras.md) for exporting a layer for Keras.
