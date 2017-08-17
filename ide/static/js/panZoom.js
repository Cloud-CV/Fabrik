export default function() {
  "use strict";

  var panZoom = document.getElementById('panZoomContainer'),
  canvas = document.getElementById('jsplumbContainer'),
  zoomIn = document.getElementById('icon-plus'),
  zoomOut = document.getElementById('icon-minus');

  if (!canvas) { return; }

  var params = { x: getQueryVariable('x'), y: getQueryVariable('y'), zoom: getQueryVariable('zoom') };

  var current = {};
  current.x = params.x ? parseFloat(params.x) : $(canvas).data('x');
  current.y = params.y ? parseFloat(params.y) : $(canvas).data('y');
  current.zoom = params.zoom ? parseFloat(params.zoom) : $(canvas).data('zoom');

  canvas.x = 0; canvas.y = 0;canvas.scale = 1;
  canvas.updateContainerPosition = function() { canvas.style.left = canvas.x + 'px'; canvas.style.top = canvas.y + 'px'; };
  canvas.updateContainerScale = function() { canvas.style.transform = 'scale('+canvas.scale+')'};

  canvas.updateContainerPosition();
  canvas.updateContainerScale();

  panZoom.addEventListener('gestureend', function(e) {
      if (e.scale < 1.0) {
          onZoom(current.zoom * 1.2);
      } else if (e.scale > 1.0) {
          onZoom(current.zoom / 1.2);
      }
  }, false);

  var  dragging = false,
    state = { click: false, pan: false },
    previousMousePosition;

  panZoom.onmousedown = function(e) {
    e.preventDefault();
    dragging = true;
    state.click = true;
    previousMousePosition = { x: e.pageX, y: e.pageY };
  };

  window.onmouseup = function() {
    dragging = false;
  };


  panZoom.ondragstart = function(e) {
    e.preventDefault();
  };

  panZoom.onmousemove = function(e) {
    if(state.click){
      state.pan = true;
    }
    if (dragging && !e.shiftKey) {
      canvas.style.transitionDuration = "0s";
      canvas.x += e.pageX - previousMousePosition.x;
      canvas.y += e.pageY - previousMousePosition.y;
      canvas.updateContainerPosition();
      previousMousePosition = { x: e.pageX, y: e.pageY };
    }
  };

  panZoom.ondblclick = function(e) {
    e.preventDefault();
    onZoom((e.ctrlKey || e.metaKey) ? current.zoom * 1.2 : current.zoom / 1.2);
  };

  window.onkeypress = function(e) {   
   onZoom((e.key == '[') ? current.zoom * 1.2 : current.zoom);    
   onZoom((e.key == ']') ? current.zoom / 1.2 : current.zoom) ;    
  }

  zoomOut.onclick = function(){
    onZoom(current.zoom * 1.2);
  };

  zoomIn.onclick = function(){
    onZoom(current.zoom / 1.2);
  };

  function onZoom(zoom) {
    canvas.scale = 1 / zoom;
    canvas.x = 0 - 105*(canvas.scale*canvas.scale);
    canvas.y = 0 - 15*(canvas.scale*canvas.scale);
    canvas.style.transitionDuration = "0.1s";
    canvas.updateContainerPosition();
    canvas.updateContainerScale();
    current.zoom = zoom;
    instance.setZoom(canvas.scale);
  }

  function getQueryVariable(id) { 
    var params = window.location.search.substring(1).split("&");  
    for (var i = 0; i < params.length; i++) {
      var p = params[i].split("="); 
      if (p[0] == id) { 
        return p[1]; 
      } 
    } 
    return(false); 
  }
  
  return state;
}

