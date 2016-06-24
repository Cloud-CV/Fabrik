var socket = io.connect('http://gsoc.cloudcv.org:3000');

$('#train').click(function(){
    socket.emit("startTraining",prototxtId);
    $('html, body').animate(
        { scrollTop: $('#terminal').offset().top },
          'slow'
    );
});

socket.on('result',function(data){
    $('#terminal').append(data);
    $('#terminal').animate({"scrollTop": $('#terminal')[0].scrollHeight}, "fast");
});
