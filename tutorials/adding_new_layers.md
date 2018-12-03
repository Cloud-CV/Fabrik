# Adding New Layers

- For setup instructions, check [README](https://github.com/Cloud-CV/Fabrik/blob/master/README.md).
- Add your new layer(s) to the [data.js](https://github.com/Cloud-CV/Fabrik/blob/master/ide/static/js/data.js) file.


## Basics for adding a new layer

- Open the ```data.js``` file in any text other.

```
export default {
  /* ********** Data Layers ********** */
  ImageData: { // Only Caffe
    name: 'image data',
    color: '#673ab7',
    endpoint: {
      src: ['Bottom'],
      trg: []
    },
```

- You should see the line ```/* ********** Data Layers ********** */```, it is the category of the layer. There are many categories in the file as mentioned below:
    - Data Layers
    - Vision Layers
    - Recurrent Layers
    - Activation/Neuron Layers
    - Normalization Layers
    - Noise Layers
    - Common Layers
    - Loss Layers
    - Utility Layers
    - Python Layers

- Create a new json element for your layer below the category it belongs to.

- Add the suitable comment for the new layer or leave it if there is no such need.


## Adding a Dropout Layer - A Walkthrough

```
  Dropout: {
    name: 'dropout',
    color: '#ff9800',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      },
      rate: {
        name: 'Dropout Ratio',
        value: 0.5,
        type: 'float',
        required: false
      },
      seed: {
        name: 'Seed',
        value: 42,
        type: 'number',
        required: false
      },
      trainable: {
        name: 'Trainable',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
```

- Suppose we wanted to add a Dropout layer into Fabrik. Keep it under ```/* ********** Common Layers ********** */``` in `data.js`.

- Add suitable comment for your layer. For example, mention if the layer is specific to a single framework.

- Keywords explanation:
    - name: Name of the layer.
    - color: Color of the layer to be shown in frontend.
    - endpoint: Endpoints of the layer.
        - src: Source endpoint of the layer.
        - trg: Target endpoint of the layer.
    - params: Parameters for the layer.
        - inplace: Checkbox input for the layer.
        - caffe: Availibility of Caffe (Checkbox input).
        - rate: The rate at which to randomly drop neurons out.
        - seed: Number to seed the random selection of neurons to drop out.
        - trainable: Whether the layer is trainable or not.
    - props: It defines the properties of the layer.
    - learn: This declares if the layer can be used for learning.

- Define as many parameters as you need for the layer.


## Making the layer visible in Fabrik

- Open [ide/static/js/pane.js](https://github.com/Cloud-CV/Fabrik/blob/master/ide/static/js/pane.js).

- Now, add a new line for the layer you just added in ```data.js``` in the  `Common` section, because this layer belongs to this category.

```html
<div className="panel panel-default">
    <div className="panel-heading" role="tab" data-toggle="collapse"                
        href="#common" aria-expanded="false"
        aria-controls="common" onClick={() => this.toggleClass('common')}>
        <a data-parent="#menu">
            <span className="badge sidebar-badge" id="commonLayers"> </span>
            Common <!-- Add your layer under the appropriate section -->
            <span className={this.state.common ? 'glyphicon sidebar-dropdown glyphicon-menu-down':
            'glyphicon sidebar-dropdown glyphicon-menu-right'} ></span>
        </a>
    </div>
    <div id="common" className="panel-collapse collapse" role="tabpanel">
        <div className="panel-body">
            <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                handleClick={this.props.handleClick}
                id="InnerProduct_Button">Inner Product</PaneElement>
            <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                handleClick={this.props.handleClick}
                id="Dropout_Button">Dropout</PaneElement> <!-- Add your layer -->
            <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                handleClick={this.props.handleClick}
                id="Embed_Button">Embed</PaneElement>
        </div>
    </div>
</div>
```

- ```<PaneElement handleClick={this.props.handleClick} id="your_layer_id">your_layer_name</PaneElement>``` this line will make your layer visible in Fabrik.

- Open [ide/static/js/filterbar.js](https://github.com/Cloud-CV/Fabrik/blob/master/ide/static/js/filterbar.js) in a text editor, add ```"your_layer_id"``` to 1(or more) of 3 framework filter array ```var KerasLayers = [...]```, ```var TensorFlowLayers = [...]``` or ```var CaffeLayers = [...]```. This should be like this ```var KerasLayers = ["RNN_Button", "GRU_Button", "your_layer_id"]```. This arrays are placed inside ```changeEvent() {}``` function.


## Adding layer handling to the backend

See the guides below to see how to add layer handling to the backend:

- [Caffe](adding_new_layers_caffe.md)
- [Keras](adding_new_layers_keras.md)
- [Tensorflow](adding_new_layers_tensorflow.md)


## Testing and pushing the new layer.

- Run the fabrik application on you local machine by following the instructions in [README](https://github.com/Cloud-CV/Fabrik/blob/master/README.md) file.

<img src="https://raw.githubusercontent.com/Cloud-CV/Fabrik/master/tutorials/layer_testing_dropout.png" />

- Check the new layer inside the category you added it. See if all the parameters are properly displayed and usable as you wanted.
- If everything is working fine commit your changes and push it to your fork then make a Pull Request.
- Congratulations! Happy contributing :-)
