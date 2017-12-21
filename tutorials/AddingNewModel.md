<h1>Adding New Model - Caffe</h1>

1. For Setup instructions, look at the [README](https://github.com/Cloud-CV/Fabrik/blob/master/README.md).
2. Add the new model as a .prototxt file to the <b>[Example/Caffe](https://github.com/Cloud-CV/Fabrik/tree/master/example/caffe)</b> folder.
3. Then add your entry to the front-end by refering to the following example in <b>[modelZoo.js](https://github.com/Cloud-CV/Fabrik/blob/master/ide/static/js/modelZoo.js)</b>, in this the ```id``` should be the name of your prototxt without the extension.
```
<li><ModelElement importNet={this.props.importNet} framework="caffe" id="sample">Sample</ModelElement></li>

```
4. After making these changes, test if loading the model and exporting it to both or at least one framework is working fine and document it accordingly in your pull request.
5. Create a pull request for the same and get reviewed by the mentors.
Cheers!

<h1>Adding New Model - Keras </h1>

1. For Setup instructions, look at the [README](https://github.com/Cloud-CV/Fabrik/blob/master/README.md).
2. Add the new model as a .json file to the <b>[Example/Keras](https://github.com/Cloud-CV/Fabrik/tree/master/example/keras)</b> folder.
3. Then add your entry to the front-end by refering to the following example in <b>[modelZoo.js](https://github.com/Cloud-CV/Fabrik/blob/master/ide/static/js/modelZoo.js)</b>, in this the ```id``` should be the name of your json without the extension.
```
<li><ModelElement importNet={this.props.importNet} framework="keras" id="Sample">sample</ModelElement></li> 
```
4. After making these changes, test if loading the model and exporting it to both or at least one framework is working fine and document it accordingly in your pull request.
5. Create a pull request for the same and get reviewed by the mentors.
Cheers!
