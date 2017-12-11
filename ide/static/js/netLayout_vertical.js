// Assumption: test differs from train in the source of input and
// some additions of accuracy layer

// designed to work with  alexNet, vgg, googleNet and resNet.
// will work with all prototxts which follows our assumption
// but the UI may not be clean.

export default function(net){
let map = {};
let position = {};
let processed = {};

Object.keys(net).forEach(layerId => {
  processed[layerId] = false;
});

function isProcessPossible(layerId){
  let inputs = net[layerId].connection.input;
  let i = 0;
  for (i = 0; i < inputs.length; i++){
    if (processed[inputs[i]] === false) {
      return false;
    }
  }
  return true;
}

/* allocatePosition finds the closest position available to preferred position,
the algorithm checks if the location at that depth is occupied by any other node
along the X direction, if yes, the closest available right or left position is
assigned */
function allocatePosition(layerId, preferredPosition){
  if (!map.hasOwnProperty(preferredPosition[1])) {
    map[preferredPosition[1]] = [];
  }
  
  map[0]=[];
    
  let positionsY = map[preferredPosition[1]];
  if (positionsY.indexOf(preferredPosition[0]) != -1) { // If X position is taken
    let temp = preferredPosition[0], i = 2;
    while (1) { // eslint-disable-line
      if(positionsY.indexOf(temp+i) === -1){
        // may be avoid overlapping edges
        if (map[preferredPosition[1] - 1].indexOf(temp + i) === -1) {
          position[layerId] = [temp + i, preferredPosition[1]];
          map[preferredPosition[1]].push(position[layerId][0]);
          return;
        }
      }
      if(positionsY.indexOf(temp-i) === -1){
        // may be avoid overlapping edges
        if (map[preferredPosition[1] - 1].indexOf(temp - i) === -1) {
          position[layerId] = [temp - i, preferredPosition[1]];
          map[preferredPosition[1]].push(position[layerId][0]);
          return;
        }
      }
      i = i + 2;
    }

  } else {
    position[layerId] = preferredPosition;
    map[preferredPosition[1]].push(position[layerId][0]);
    return;
  }
}

let stack = [];
let parentMap = {};
let i = null, layerId = null, parentId =  null, inputLength = null, outputLength = null;
const dataLayers = ['ImageData', 'Data', 'HDF5Data', 'Input', 'WindowData', 'MemoryData', 'DummyData'];
// finding the input layers to start DFS
Object.keys(net).forEach(layerId => {
  if (net[layerId].info.type == 'Python'){
    // This is to check if the Python layer is a data layer
    if (net[layerId].params.endPoint[0] == "1, 0"){
      stack.push(layerId);
      parentMap[layerId] = null;
    }
  }
  if (dataLayers.includes(net[layerId].info.type)) {
    stack.push(layerId);
    parentMap[layerId] = null;
  }
});

/* custom DFS, traverse the nodes and allocate position to elements
based on the input and output connections */
while (stack.length) {
  i = stack.length - 1;
  while (isProcessPossible(stack[i]) === false) { // To check if all preceeding nodes have been processed
    i = i - 1;
  }
  layerId = stack[i];
  stack.splice(i, 1); // Removes layerID from stack
  parentId = parentMap[layerId];
  inputLength = net[layerId].connection.input.length; // No. of parents
  if (parentId != null){
    outputLength = net[parentId].connection.output.length;
  }
  if (parentId === null) { // First node
    position[layerId] = [0,0];
  } else if(inputLength === 1 && outputLength === 1){ // Simple sequential NN structure
    allocatePosition(layerId, [position[parentId][0], position[parentId][1]+1]);
  } else if (inputLength > 1){ // e.g. Concat layer in GoogLeNet
    let sum = 0, mean = 0, max = 0;
    net[layerId].connection.input.forEach(inputId => {
      sum = sum + position[inputId][0]; // To center node among the preceeding nodes
      if (position[inputId][1] > max) { // To find deepest node in branch
        max = position[inputId][1];
      }
    });
    mean = Math.floor(sum / inputLength);
    allocatePosition(layerId, [mean, max + 1]);
  } else if (inputLength === 1 && outputLength != 1) { // e.g. inception block
    let index = net[parentId].connection.output.indexOf(layerId);
    allocatePosition(layerId, [position[parentId][0] + (outputLength - 1) - 2 * index, position[parentId][1] + 1]);
  }

  net[layerId].connection.output.forEach(outputId => {
    if (stack.indexOf(outputId) === -1) {
      stack.push(outputId);
      parentMap[outputId] = layerId;
    }
  });

  processed[layerId] = true;

}
return position;
}
