// Assumption: test differs from train in the source of input and
// some additions of accuracy layer

// designed to work with  alexNet, vgg, googleNet and resNet.
// will work with all prototxts which follows our assumption
// but the UI may not be clean.

export default function(net) {
  let map = {};
  let position = {};
  let processed = {};
  let layer_indegree = {};

  // maintaining height & width in integers for use of map in order to
  // reduce the search space for overlapping layers & plotting.
  const height = Math.round(0.05*window.innerHeight, 0);
  const width = Math.round(0.35*window.innerWidth, 0);

  Object.keys(net).forEach(layerId => {
    processed[layerId] = false;
    /* maintaining indegeree for every layer node
    to avoid extra iteration and using topological sort instead of DFS */
    layer_indegree[layerId] = net[layerId].connection.input.length;
  });

  /* allocatePosition finds the closest position available to preferred position,
  the algorithm checks if the location at that depth is occupied by any other node
  along the X direction, if yes, the closest available right or left position is
  assigned */
  function allocatePosition(layerId, preferredPosition) {
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

    }
    else {
      position[layerId] = preferredPosition;
      map[preferredPosition[1]].push(position[layerId][0]);
      return;
    }
  }

  let stack = [];
  let parentMap = {};
  let i = null, layerId = null, parentId =  null, inputLength = null, outputLength = null;
  const dataLayers = ['ImageData', 'Data', 'HDF5Data', 'Input', 'WindowData', 'MemoryData', 'DummyData'];

  // finding the input layers to start Topological Sort
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

  /* Custom Topolical Sort, traverse the nodes and allocate position to
  elements based on the input and output connections */
  let mapp = {};
  // Layers which are not used alone
  let combined_layers = ['ReLU', 'PReLU', 'LRN', 'TanH', 'BatchNorm', 'Dropout', 'Scale'];

  while (stack.length) {
    i = stack.pop();
    layerId = i;

    parentId = parentMap[layerId];
    inputLength = net[layerId].connection.input.length; // No. of parents
    if (parentId != null) {
      outputLength = net[parentId].connection.output.length;
    }
    if (parentId === null) { // First node
      position[layerId] = [0,0];
    }
    else if(inputLength === 1 && outputLength === 1) { // Simple sequential NN structure
      allocatePosition(layerId, [position[parentId][0], position[parentId][1]+1]);
    }
    else if (inputLength > 1) { // e.g. Concat layer in GoogLeNet
      let sum = 0, mean = 0, max = 0;
      net[layerId].connection.input.forEach(inputId => {
        sum = sum + position[inputId][0]; // To center node among the preceeding nodes
        if (position[inputId][1] > max) { // To find deepest node in branch
          max = position[inputId][1];
        }
      });
      mean = Math.floor(sum / inputLength);
      allocatePosition(layerId, [mean, max + 1]);
    }
    else if (inputLength === 1 && outputLength != 1) { // e.g. inception block
      let index = net[parentId].connection.output.indexOf(layerId);
      allocatePosition(layerId, [position[parentId][0] + (outputLength - 1) - 2 * index, position[parentId][1] + 1]);
    }

    net[layerId].connection.output.forEach(outputId => {
      if ((layer_indegree[outputId] - 1) == 0) {
        stack.push(outputId);
        parentMap[outputId] = layerId;
      }
      layer_indegree[outputId] = layer_indegree[outputId] - 1;
    });

    processed[layerId] = true;

    const layer = net[layerId];
    // Checking if the layer is one of the combined ones
    // and deciding vertical spacing accordingly
    let parentX = position[layer.connection.input[0]];
    let currentX = position[layerId][0];
    let y_space = 40;
    let prev_top = 0;

    if (parentX){
      parentX = parentX[0];
    }
    if ($.inArray(layer.info.type, combined_layers) != -1 && parentX==currentX){
      y_space = 0;
    }

    // Finding the position of the last(deepest) connected layer
    if (net[layer.connection.input[0]] != undefined) {
      prev_top = 0;
      for (let j=0; j<layer.connection.input.length; j++){
        // safety check for corner cases
        if('state' in net[layer.connection.input[j]]){
          let temp = net[layer.connection.input[j]].state.top;
          temp = parseInt(temp.substring(0,temp.length-2));
          if (temp > prev_top){
            prev_top = temp;
          }
        }
      }
    }
    // Graph does not centre properly on higher resolution screens
    let top = height + prev_top + y_space + Math.ceil(41-height);
    let left = width + 100 * position[layerId][0];
    let layerOverlaps = true;

    // Checking for Overlapping layers based on their X-Coordinates
    // if any layer overlaps then adjust the position else keep
    // the preferred positions.
    if (y_space > 0) {
      while (layerOverlaps) {
        let overlapFlag = false;
        // checking for overlapping layer div's by use of there height & width.
        for(let topC = Math.max(0,top - 40);topC<(top+40);topC++) {
          if(mapp.hasOwnProperty(topC)) {
            let xPositions = mapp[topC].slice();
            for(let j=0;j<xPositions.length;j++) {
              if(xPositions[j]>=(left-130) && xPositions[j]<=(left+135)) {
                overlapFlag = true;
                break;
              }
            }
          }
        }
        if(!overlapFlag) {
          layerOverlaps = false;
          break;
        }
        top += y_space;
      }
    }

    layer.state = {
        top: `${top}px`,
        left: `${left}px`,
        class: ''
    };

    // keeping a map of layer's top,left coordinates.
    if(!map.hasOwnProperty(top)) {
      mapp[top]=[];
    }
    mapp[top].push(left);
  }
}
