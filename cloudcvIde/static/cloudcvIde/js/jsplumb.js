export default function(){
    var instance = window.jsp = jsPlumb.getInstance({
        DragOptions: { cursor: 'pointer', zIndex: 2000 },
        ConnectionOverlays: [
            [ "Arrow", {
                location: 1,
                visible:true,
                id:"ARROW",
                width:20,
                length:20,
                events:{
                    click:function() { alert("you clicked on the arrow overlay")}
                }
            } ],
            [ "Label", {
                location: 0.1,
                id: "label",
                cssClass: "",
                events:{
                    tap:function() { alert("hey"); }
                }
            }]
        ],
        Container: "canvas"
        });
    
    var connectorPaintStyle = {
            lineWidth: 5,
            strokeStyle: "rgba(0, 122, 204,0.7)"
        },
        sourceEndpoint = {
            endpoint: "Dot",
            paintStyle: {
                fillStyle: "#c5c5bf",
                radius: 5
            },
            isSource: true,
            connector: [ "Straight", { curviness: 40 }  ],
            connectorStyle: connectorPaintStyle,
            maxConnections: -1,
            dragOptions: {}
        },
        targetEndpoint = {
            endpoint: "Dot",
            paintStyle: {
                fillStyle: "#c5c5bf",
                radius: 5
            },
            maxConnections: 1,
            isTarget: true
        }


    var _addLayerEndpoints = function (toId, sourceAnchors, targetAnchors) {
        for (var i = 0; i < sourceAnchors.length; i++) {
            var sourceUUID = toId + "-s"+i.toString();
            instance.addEndpoint(toId, sourceEndpoint, {
                anchor: sourceAnchors[i], uuid: sourceUUID
            });
        }
        for (var j = 0; j < targetAnchors.length; j++) {
            var targetUUID = toId + "-t"+j.toString();
            instance.addEndpoint(toId, targetEndpoint, { anchor:targetAnchors[j], uuid: targetUUID });
        }
    };

    return {instance:instance,_addLayerEndpoints:_addLayerEndpoints}
}