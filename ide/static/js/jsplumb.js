export default function () {
  let ArrowConnector = function(params) {
  params = params || { dx: 120, dy: 120 };
  let _super =  jsPlumb.Connectors.AbstractConnector.apply(this, arguments);
  this.type = "ArrowConnector";
  let dx = params.x || 50,
    dy = params.y || 50;

  this._compute = function(paintInfo, paintParams) {
    let w = paintInfo.w,
      h = paintInfo.h;

    if(paintParams.targetEndpoint.isTarget && paintParams.targetEndpoint.element.attributes['data-type'].nodeValue === 'Concat'){
      _super.addSegment(this, "Straight", {
        x1:paintInfo.sx,
        y1:paintInfo.sy,
        x2:paintInfo.tx - dx,
        y2:paintInfo.sy
      });
      _super.addSegment(this, "Straight", {
        x1:paintInfo.tx - dx,
        y1:paintInfo.sy,
        x2:paintInfo.tx,
        y2:paintInfo.ty
      });
    } else {
      _super.addSegment(this, "Straight", {
        x1:paintInfo.sx,
        y1:paintInfo.sy,
        x2:paintInfo.sx + dx,
        y2:paintInfo.ty
      });
      _super.addSegment(this, "Straight", {
        x1:paintInfo.sx + dx,
        y1:paintInfo.ty,
        x2:paintInfo.tx,
        y2:paintInfo.ty
      });
    }
  };
};
jsPlumbUtil.extend(ArrowConnector, jsPlumb.Connectors.AbstractConnector);
jsPlumb.registerConnectorType(ArrowConnector, "ArrowConnector");
  const instance = window.jsp = jsPlumb.getInstance({
    DragOptions: { cursor: 'pointer', zIndex: 2000 },
    ConnectionOverlays: [
      ['Arrow',
        {
          location: 1,
          visible: true,
          id: 'ARROW',
          width: 10,
          length: 10,
        },
      ],
    ],
    Container: 'canvas',
  });

  const connectorPaintStyle = {
    lineWidth: 2,
    strokeStyle: 'black',
  };

  const sourceEndpoint = {
    endpoint: 'Dot',
    paintStyle: {
      fillStyle: '#c5c5bf',
      radius: 5,
    },
    isSource: true,
    connector: [
      'ArrowConnector'
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
    maxConnections: -1,
    isTarget: true,
  };


  instance.addLayerEndpoints = function addLayerEndpoints(toId, sourceAnchors, targetAnchors) {
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

  return instance;
}


