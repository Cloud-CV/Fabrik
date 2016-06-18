export default function () {
  const instance = window.jsp = jsPlumb.getInstance({
    DragOptions: { cursor: 'pointer', zIndex: 2000 },
    ConnectionOverlays: [
      ['Arrow',
        {
          location: 1,
          visible: true,
          id: 'ARROW',
          width: 20,
          length: 20,
        },
      ],
    ],
    Container: 'canvas',
  });

  const connectorPaintStyle = {
    lineWidth: 5,
    strokeStyle: 'rgba(0, 122, 204,0.7)',
  };

  const sourceEndpoint = {
    endpoint: 'Dot',
    paintStyle: {
      fillStyle: '#c5c5bf',
      radius: 5,
    },
    isSource: true,
    connector: [
      'Flowchart',
      {
        stub: [5, 10],
        gap: 5,
        cornerRadius: 10,
        alwaysRespectStubs: true,
      },
    ],
    connectorStyle: connectorPaintStyle,
    maxConnections: -1,
    dragOptions: {},
  };

  const targetEndpoint = {
    endpoint: 'Dot',
    paintStyle: {
      fillStyle: '#c5c5bf',
      radius: 5,
    },
    maxConnections: 1,
    isTarget: true,
  };


  function addLayerEndpoints(toId, sourceAnchors, targetAnchors) {
    let i;
    let sourceUUID;
    let targetUUID;
    for (i = 0; i < sourceAnchors.length; i++) {
      sourceUUID = `${toId}-s${i}`;
      instance.addEndpoint(toId, sourceEndpoint, { anchor: sourceAnchors[i], uuid: sourceUUID });
    }
    for (i = 0; i < targetAnchors.length; i++) {
      targetUUID = `${toId}-t${i}`;
      instance.addEndpoint(toId, targetEndpoint, { anchor: targetAnchors[i], uuid: targetUUID });
    }
  }

  return { instance, addLayerEndpoints };
}
