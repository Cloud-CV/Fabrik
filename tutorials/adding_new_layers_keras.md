## Exporting and Importing layer - Keras

Follow the guide [here](adding_new_layers.md)  to add your new layer to Fabrik's frontend. Then follow through this guide to add support for importing and exporting your layer for Keras.


#### Importing a layer

- Open [keras_app/views/layers_import.py](https://github.com/Cloud-CV/Fabrik/blob/master/keras_app/views/layers_import.py).
    - Add a function to process the new layer.
        - The function should take a Keras `Layer` object, called `layer`.
        - Get the layer parameters from `layer`, and create a json layer with the function  jsonLayer.
        - Return the json layer you just created.

        ```
        def Dropout(layer):
            params = {}
            if (layer.rate is not None):
                params['rate'] = layer.rate
            if (layer.seed is not None):
                params['seed'] = layer.seed
            if (layer.trainable is not None):
                params['trainable'] = layer.trainable
            return jsonLayer('Dropout', params, layer)
        ```

- Open [keras_app/views/import_json.py](https://github.com/Cloud-CV/Fabrik/blob/master/keras_app/views/import_json.py).
    
    - From `layers_import`, import the function you just defined.

        ```
        from layers_import import Dropout
        ```

    - Map your layer name to your function in `layer_map`.

        ```diff
        layer_map = {
            'InputLayer': Input,
            'Dense': Dense,
            ...
        +   'Dropout': Dropout,
        }
        ```


#### Exporting a layer

- Open [keras_app/views/layers_export.py](https://github.com/Cloud-CV/Fabrik/blob/master/keras_app/views/layers_export.py).
    - Add a function to process your layer that takes in the following arguments:
        - `layer` : a json string, same as the one created in layers_import.py
        - `layer_in`: a Tensor, output of the previous layer
        - `layerId`: a string id of layer
        - `tensor`: a bool

    - Inside the function, get layer parameters from `layer` and build a Keras layer using them.

    - If `tensor==True`, call the Keras layer on `layer` and return the output tensor. Else, return the `layer` itself.

    ```
    def dropout(layer, layer_in, layerId, tensor=True):
        out = {layerId: Dropout(0.5)}
        if tensor:
            out[layerId] = out[layerId](*layer_in)
        return out
    ```

- Open [ide/tasks.py](https://github.com/Cloud-CV/Fabrik/blob/master/ide/tasks.py).

    - From `layers_export`, import the function you just defined.

    ```
    from keras_app.views.layers_export import dropout
    ```

    - Add your function to `layer_map` inside `export_keras_json`.

    ```diff
    layer_map = {
        'InputLayer': Input,
        'Dense': Dense,
            ...
    +   'Dropout': dropout,
    }
    ```

- Open [keras_app/views/export_json.py](https://github.com/Cloud-CV/Fabrik/blob/master/keras_app/views/export_json.py)

    - From `layers_export`, import the function you just defined.

    ```
    from layers_export import dropout
    ```

    - Add your function to `layer_map`.

    ```diff
    layer_map = {
        'InputLayer': Input,
        'Dense': Dense,
        ...
    +  'Dropout': dropout
    }
    ```

    Note : Fabrik exports models using the celery task [export_keras_json](https://github.com/Cloud-CV/Fabrik/blob/master/ide/tasks.py#L60), but we keep `export_json.py` updated to test the export code.
