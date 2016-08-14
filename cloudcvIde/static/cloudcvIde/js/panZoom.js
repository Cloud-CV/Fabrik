export default function() {
  "use strict";

  var panZoom = document.getElementById('panZoomContainer'),
    canvas = document.getElementById('jsplumbContainer');

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


  function updateTextPosition(e) {
    e.style.left = ($(e).data("x")) / current.zoom + 'px';
    e.style.top = ($(e).data("y")) / current.zoom  + 'px';
  }


  function newText(x, y, size, text) {
    var tb = document.createElement('div');
    tb.className = "text";
    tb.contentEditable = true;
    tb.innerHTML = text;
    $(tb).data("x", x).data("y", y).data("size", size);
    updateTextPosition(tb);
    canvas.appendChild(tb);
    return tb;
  }

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
  //panZoom.onmouseup = function() {
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
      //instance.repaintEverything();
    }
  };

  panZoom.ondblclick = function(e) {
    e.preventDefault();
    onZoom((e.ctrlKey || e.metaKey) ? current.zoom * 1.7 * 1.7 : current.zoom / 1.7 / 1.7, e.clientX - panZoom.offsetLeft, e.clientY - panZoom.offsetTop);
  };

  function onZoom(zoom, cx, cy) {
    var dx = cx - canvas.x;
    var dy = cy - canvas.y;
    var newdx = (dx*current.zoom)/zoom;
    var newdy = (dy*current.zoom)/zoom;
    canvas.x = cx - newdx;
    canvas.y = cy - newdy;
    canvas.scale = 1 / zoom;
    canvas.style.transitionDuration = "0s";
    canvas.updateContainerPosition();
    canvas.updateContainerScale();
    current.zoom = zoom;
    instance.setZoom(canvas.scale);
    //instance.repaintEverything();
  }

  var mousewheel, lastMouseWheelEventTime = Date.now();

  mousewheel = function(e) {
    e.preventDefault();
    var delta = e.wheelDeltaY;

    //onZoom((delta > 0) ? current.zoom / 1.7 : current.zoom * 1.7, e.clientX - panZoom.offsetLeft, e.clientY - panZoom.offsetTop);
    onZoom((delta > 0) ? current.zoom / 1.1 : ((delta < 0) ? current.zoom * 1.1 : current.zoom), e.clientX - panZoom.getBoundingClientRect().left, e.clientY - panZoom.getBoundingClientRect().top);
  };

  if ("onmousewheel" in document) { panZoom.onmousewheel = mousewheel; }
  else { panZoom.addEventListener('wheel', mousewheel, false); }

  function getQueryVariable(id) { var params = window.location.search.substring(1).split("&");  for (var i = 0; i < params.length; i++) { var p = params[i].split("="); if (p[0] == id) { return p[1]; } } return(false); }

  return state;

};
