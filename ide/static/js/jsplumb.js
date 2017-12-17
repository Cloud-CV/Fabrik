export default function () {
  let ArrowConnector = function(params) {
  params = params || { dx: 20, dy: 20 };
  let _super =  jsPlumb.Connectors.AbstractConnector.apply(this, arguments);
  this.type = "ArrowConnector";
  let dy = params.y || 20;

  this._compute = function(paintInfo, paintParams) {

    if(paintParams.targetEndpoint.isTarget && 
      ((paintParams.targetEndpoint.element.attributes['data-type'].nodeValue === 'Concat') ||
       (paintParams.targetEndpoint.element.attributes['data-type'].nodeValue === 'Eltwise'))){
      _super.addSegment(this, "Straight", {
        x1:paintInfo.sx,
        y1:paintInfo.sy,
        x2:paintInfo.sx,
        y2:paintInfo.ty - dy
      });
      _super.addSegment(this, "Straight", {
        x1:paintInfo.sx,
        y1:paintInfo.ty - dy,
        x2:paintInfo.tx,
        y2:paintInfo.ty
      })
    } else {
      if (paintInfo.ty-paintInfo.sy > 40) {
        var extend = Math.sqrt(paintInfo.ty-paintInfo.sy / 80) + 70;
      _super.addSegment(this, "Straight", {
        x1:paintInfo.sx,
        y1:paintInfo.sy,
        x2:paintInfo.sx - extend,
        y2:paintInfo.sy +40
      });
      _super.addSegment(this, "Straight", {
        x1:paintInfo.sx - extend,
        y1:paintInfo.sy +40,
        x2:paintInfo.sx - extend,
        y2:paintInfo.ty -40
      });
      _super.addSegment(this, "Straight", {
        x1:paintInfo.sx - extend,
        y1:paintInfo.ty-40,
        x2:paintInfo.tx,
        y2:paintInfo.ty
      });
    }
    else {
      _super.addSegment(this, "Straight", {
        x1:paintInfo.sx,
        y1:paintInfo.sy,
        x2:paintInfo.tx,
        y2:paintInfo.ty
      });
    }
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
          length: 10
        }
      ]
    ],
    Container: 'canvas'
  });

  const connectorPaintStyle = {
    lineWidth: 2,
    strokeStyle: 'black'
  };

  const sourceEndpointDot = {
    endpoint: 'Dot',
    paintStyle: {
      fillStyle: '#c5c5bf',
      radius: 5
    },
    isSource: true,
    connector: [
      'ArrowConnector'
    ],
    connectorStyle: connectorPaintStyle,
    maxConnections: -1,
    dragOptions: {}
  };

  const targetEndpointDot = {
    endpoint: 'Dot',
    paintStyle: {
      fillStyle: '#c5c5bf',
      radius: 5
    },
    maxConnections: -1,
    isTarget: true
  };

  instance.addLayerEndpoints = function addLayerEndpoints(toId, sourceAnchors, targetAnchors) {
    let i;
    let sourceUUID;
    let targetUUID;
    for (i = 0; i < sourceAnchors.length; i++) {
      sourceUUID = `${toId}-s${i}`;

      instance.addEndpoint(toId, sourceEndpointDot, { anchor: sourceAnchors[i], uuid: sourceUUID });
    }
    for (i = 0; i < targetAnchors.length; i++) {
      targetUUID = `${toId}-t${i}`;
      instance.addEndpoint(toId, targetEndpointDot, { anchor: targetAnchors[i], uuid: targetUUID });
    }
  }

  return instance;
}

