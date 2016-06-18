import React from 'react';
import PaneElement from './paneElement';

function Pane() {
  return (
    <div className="col-md-2 pane">
      <PaneElement id="input">Input</PaneElement>
      <PaneElement id="conv">Convolution</PaneElement>
      <PaneElement id="pool">Pool</PaneElement>
      <PaneElement id="relu">ReLU</PaneElement>
      <PaneElement id="fc">FC</PaneElement>
      <PaneElement id="loss">Loss</PaneElement>
    </div>
  );
}

export default Pane;
