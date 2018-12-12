## Exporting and Importing layer - Tensorflow

Follow the guide [here](adding_new_layers.md) to add your new layer to Fabrik's frontend. Then follow through this guide to add support for importing and exporting your layer for Tensorflow.


#### Importing a layer

- Open [layers_import.py](https://github.com/Cloud-CV/Fabrik/blob/master/tensorflow_app/views/layers_import.py).

    - Add a function to import your layer.
        - Create a function name import_<layer_name> that takes one parameter, layer_ops, that is a list of all ops in the layer being imported.
        - Get layer parameters from the operations in layer_ops and build a dictionary mapping parameter names to values.
        - Get a list of input layers to the layer being processed using `get_input_layers(layer_ops)`.
        - Create and return a json layer for new layer, calling `jsonLayer` with the new layer_type, parameters, input layers and output_layers(optional).

        ```
        def import_dropout(layer_ops):
            layer_params = {}
            for node in layer_ops:
            if ('rate' in node.node_def.attr):
                layer_params['rate'] = node.get_attr('rate')
            if ('seed' in node.node_def.attr):
                layer_params['seed'] = node.get_attr('seed')
            if ('training' in node.node_def.attr):
                layer_params['trainable'] = node.get_attr('training')
            return jsonLayer('Dropout', layer_params, get_input_layers(layer_ops), [])
        ```

- Open [import_graphdef.py](https://github.com/Cloud-CV/Fabrik/blob/master/tensorflow_app/views/import_graphdef.py)

    - From `layers_import`, import the layer import function you just defined.

        `from layers_import import_dropout`

    - Add your layer import function to either `layer_map` or `name_map`:
        - `layer_map` if the layer type can be determined directly by the type of nodes in the layer's ops.
        ` 'name_map` if the laye type can only be determined from the name of the layer.
        
        ```diff
        name_map = {
            'flatten': import_flatten,
            'lrn': import_lrn,
            ...
        +   'dropout': import_dropout,
            ...
            'concatenate': import_concat
        }
        ```

#### Exporting a layer

Fabrik exports Tensorflow models using Keras. [See this guide](adding_new_layers_keras.md) for exporting a layer for Keras.
