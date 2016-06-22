import React from 'react';
import PaneElement from './paneElement';

function Pane() {
  return (
    <div className="col-md-2 pane">
      <PaneElement id="Data">Input</PaneElement>
      <PaneElement id="Convolution">Convolution</PaneElement>
      <PaneElement id="Pooling">Pool</PaneElement>
      <PaneElement id="ReLU">ReLU</PaneElement>
      <PaneElement id="InnerProduct">FC</PaneElement>
      <PaneElement id="SoftmaxWithLoss">Loss</PaneElement>
    </div>
  );
}

export default Pane;
