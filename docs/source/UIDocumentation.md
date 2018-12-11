Frontend Design
========
## Architecture
(All javascript files described here can be found in the /ide/static/js/ directory of Fabrik)

#### ```addCommentModal.js```
(The bullets contain methods specific to the file along with their explanations.)

```addCommentModal.js``` is responsible for adding comments into the interface. It has the following methods:
* ```handleClick``` - invoked on click on modal
* ```addComment``` - adds comment modal to RTC

***

#### ```app.js```
```app.js``` hosts the main app, but contains nothing else than a call for ```content.js```.
***

#### ```canvas.js```
```content.js``` invokes an instance of ```canvas.js``` that contains the following methods:
* ```clickLayerEvent``` - invoked on a click of a layer or on drag of that layer
* ```hoverLayerEvent``` - invoked on a hover
* ```scrollCanvas``` - scrolls canvas
* ```clickCanvas``` - invoked on click
* ```updateLayerPosition``` - changes layer positon based on event
* ```mouseUpEvent``` - invoked when mouse key is up
* ```connectionEvent``` - invoked on connection; checks for cycles and modifies layers
* ```detachConnectionEvent``` - modifies layers
* ```drop``` - invoked on layer drop onto canvas; checks for errors

```canvas.js``` also contains the code that decides whether a node's line needs to be rerouted if it is cutting through another node.

#### ```canvas.js```'s visualisation algorithm
The method it uses is the following:
```checkIfCuttingLine``` takes in 2 variables: net and pos, where net has an array of all the nodes, and pos is an array of x and y coordinates checked by this method to see whether a line will cut through.
To put it more specifically, ```checkIfCuttingLine``` checks if the line formed with the coordinates in the positional block will cut through any other nodes between them.

```checkIfCuttingLine``` creates an equation from the x and y points by calculating the slope and using point slope form.

After this, it calls ```getBetween``` to get the nodes between the x and y coordinates of the created line.

The ```getBetween``` also serves the purpose of returning which direction the majority of the blocks between are. This implementation is purely for performance, otherwise it would be seperated into a seperate function.

After ```getBetween``` returns the IDs of the nodes between the x and y coordinate pair, it is checked if the cutting line loops through them (to see whether or not the resulting line will cut through the in between node).

If it does cut through, ```getBetween``` will return the direction the line needs to be shifted to the parent function, ```checkCutting```, to iterate once again 80 pixels to either the left or right (depending on the return.)

*This algorithmic design creates the possibility of an infinite loop if the canvas has been completely occupied  and there is no more space remaining.*

***

#### ```commentSidebar.js```
Is responsible for creating the comment sidebar. Consists of:
* ```close``` - closes sidebar
* ```addComment``` - adds comment

***

#### ```commentTooltip.js```
Is responsible for creating the comment dialog box. Consists of:
* ```handleClick``` - handles user click event
* ```addComment``` - adds comment to RTC

***

#### ```content.js```
```content.js``` is the most important file, as it loads the main app. Here are some of its important methods:
* ```openModal``` - opens modals (such as "Help" or "About Us")
* ```closeModal``` - closes previously opened modals
* ```infoModal``` - sets info about infoModal state, and then opens that modal
* ```faqModal``` - sets info about faqModal state, and then opens that modal
* ```zooModal``` - imports and opens zooModal
* ```addNewLayer``` - invoked by ```handleClick``` and passed in a JS object with layer information - adds a layer
* ```changeSelectedLayer``` - changes which layer has the selected class on it, which outlines layer to emphasize a "selection"
* ```changeHoveredLayer``` - changes which layer has the hover class on it, which outlines layer to emphasize a "hover"
* ```addHighlightOnLayer``` - highlights layer by ```layerId```
* ```modifyLayer``` - modifies layer, passed in layer is the new layer, and layer id is the id it needs to be replaced at.
* ```deleteLayer``` - deletes layers and removes inputs and outputs for it.
* ```getLayerParameters``` - sums total amount of parameters and updates layer's parameters
* ```calculateParameters``` - loops through net and invokes ```getLayerParameters```
* ```adjustParameters``` - used to adjust layer parameters based on layer, change is passed in.
* ```modifyLayerParams``` - modifies layer params based on layer and layerId, invoked by SetParams
* ```loadLayerShapes``` - AJAXs to backend to model parameters
* ```exportNet``` - AJAXs to backend and then passes back error/success
* ```exportPrep``` - invoked by ```exportNet```; preprocessed model object for export
* ```importNet``` - AJAXs to backend and then passes back error/success
* ```initialiseImportedNet``` - starts prepping layer to be displayed by Fabrik, positions layers
* ```changeNetName``` - invoked after user starts typing in name box (placed above the model in the UI); changes the name of the net
* ```changeNetStatus``` - takes in a boolean and changes its value (the boolean is responsible for the ```rebuildNet``` element)
* ```changeNetPhase``` - changes the phase of the net (Train/Test)
* ```copyTrain``` - copies the nets train phase for the test phase
* ```copyTrain``` - copies the nets train option for the test option
* ```trainOnly``` - mehod responsible for Train-only models
* ```saveDb``` - creates RTC hyperlink
* ```loadDb``` - loads model for RTC by ```id```
* ```performSharedUpdate``` - updates RTC shared model using sockets
* ```performSharedAdd``` - adds shared layer in RTC
* ```performSharedDelete``` - deletes shared layer in RTC
* ```addSharedComment``` - adds comment shared in RTC
* ```toggleSidebar``` - toggles the visibilty of the sidebar
* ```handleClick``` - handles a click based on an event: handles connections and adding layers.

***

#### ```data.js```
```data.js``` contains various different variables filled with data used throughout the application, it stores the layers

***
#### ```error.js```
```error.js``` contains Error React Component with two methods:
* ```dismissError``` - dismisses opened error
The error is passed in through props and then displayed to the user.

***

#### ```field.js```
```field.js``` contains the various fields used by the layer editor.
* ```change``` - used to change the state of checkboxes; it is passed in event e.

***

#### ```filterBar.js```
This file filters layers based on framework. It uses two methods:
* ```changeEvent``` - filters the layers

***

#### ```importTextbox.js```
Renders the 'Load Model From Text Input' textbox (available in the top of the main sidebar).

***

#### ```jsplumb.js```
The ```jsplumb.js``` file contains code that handles the arrangement and the dragging/connecting of layers. The file hosts a function, which created the arrow connector(```ArrowConnector```). Later, there is a function (```this._compute```), which draws the elements. It is responsible for creating the connectors and simultaneously checks if there isn't any cutting and if extending the connector isn't neccessary. It then creates the connectors segments and styles it appropriately. Then, in ```instance.addLayerEndpoints``` the anchors of the connector are defined.

Please refer to the jsplumb documentation here to learn more about this API set: https://jsplumbtoolkit.com/docs.html

***

#### ```layer.js```
```layer.js``` is invoked by ```canvas.js``` and it displays the actual layering on the jsplumb container. The position of each layer is set in the state of the layer. Its methods are:
* ```onCloseCommentModal``` - closes comment modal
* ```onAddComment``` - opens comment tooltip
* ```doSharedUpdate``` - shares comment in RTC

***

#### ```login.js```
```login.js``` is responsible for the login dialog in Fabrik. First it uses AJAX to process it and later renders the login dialog.

***

#### ```modelElement.js```
```modelElement.js``` contains the component that renders out each model in the model zoo. It includes logic that onClick will trigger an importNet, as defined in ```content.js```.
***
#### ```modelZoo.js```
```modelZoo.js``` contains the rendering of the modelZoo, it invokes modelElement to render the actual listing of the model. Methods:

***

#### ```netLayout_vertical.js``` and ```netLayout.js```
Both of these files contain code that determines positioning and layout of net. It is invoked by ```content.js```

#### ```netLayout_vertical.js```
Defines the vertical alignment of network elements. ```netLayout_vertical.js``` uses a function, called ```allocatePosition``` to give the layers their position on the canvas. It finds the closest position available to the preferred position, and checks if a node is already on that position on the X axis (if one is, a position left or right is assigned). The file also uses a custom Topolical Sort to give the nodes their position (it is based on the inputs and outputs of nodes). Later it is checked if any nodes overlap and in case they do, they are moved.

#### ```netLayout.js```
```netLayout.js``` is used to check the Y attribute of nodes. The function ```allocatePosition``` finds the closest available position to the preffered one and allocates the module. Later the nodes are checked with a DFS algorithm (depth-first search algorithm).

***

#### ```pane.js```
```pane.js``` handles the layer panel and contains these methods:
* ```toggleClass``` - toggles classes for the dropdown on the sidebar for layer selection

```pane.js``` invokes ```paneElement.js``` to render out each element.

***

#### ```paneElement.js```
```paneElement.js``` renders out each element of the pane, it is invoked by ```pane.js```. It includes:
* ```drag``` - allows dragging of layers

```pane.js``` renders out all of the layers for selection by the user.
***
#### ```panZoom.js```
```panZoom.js``` includes the functions that zoom the canvas in and out, based on various invocations.

***

#### ```setParams.js```
Contains the following methods for the layer edition sidebar:
* ```changeProps``` - changes layer properties
* ```changeParams``` - changes layer parameters
* ```trainOnly``` - turns model into a train-only
* ```handleKeyPress``` - handles layer delete after the 'delete' key is pressed

```setParams.js``` allows users to change layer parameters and reads parameters through ```data.js```

***
#### ```tabs.js```
```tabs.js``` is used to switch between the Train and Test model buttons and to render.
***
#### ```tooltip.js``` and ```tooltipData.js```
Both of these files contains code for tooltips and the ```tooltipData.js``` contains the actual tooltips that are rendered.

note: tooltips are "hover" messages, they tell more information about something when a user hovers over an object.
***

#### ```topbar.js```
```topbar.js```  shows the top section of the sidebar. It has two methods:
* ```checkURL``` - checks model import URL
