## Exporting and Importing layer - Caffe

Follow the guide [here](adding_new_layers.md) to add your new layer to Fabrik's frontend. Then follow through this guide to add support for importing and exporting your layer for Caffe.


#### Importing a layer

- Open [caffe_app/views/import_prototxt.py](https://github.com/Cloud-CV/Fabrik/blob/master/caffe_app/views/import_prototxt.py).

- Add a function for the new layer below the category of this layer.

- Load the parameters, do the calculations for your layer in python and return the value of ```params``` (parameters).
    ```
    # ********** Common Layers **********
    def Dropout(layer):
        params = {}
        if(layer.top == layer.bottom):
            params['inplace'] = True
        return params
    ```
- Add your defined layer in the ```layer_dict``` array, as shown above.

    ```diff
    layer_dict = {'Accuracy': Accuracy,
        'WindowData': WindowData,
        ...
    +   'Dropout': Dropout
    }
    ```


#### Exporting a layer

- Open [ide/utils/jsonToPrototxt.py](https://github.com/Cloud-CV/Fabrik/blob/master/ide/utils/jsonToPrototxt.py).

- Add an export function for training and testing of the new layer.

- There you need to load parameters, then train & test values and at last return the trained and tested data.

    ```
    def export_Dropout(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
        inplace = layerParams['inplace']
        for ns in (ns_train, ns_test):
            caffeLayer = get_iterable(L.Dropout(
                *[ns[x] for x in blobNames[layerId]['bottom']],
                in_place=inplace))
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns[key] = value
        return ns_train, ns_test
    ```

- Add the export function in the ```layer_map``` array.

    ```diff
    layer_map = {
        'ImageData': export_ImageData,
        'Data': export_Data,
        ...
    +   'Dropout': export_Dropout,
    }
    ```
