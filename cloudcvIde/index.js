var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
console.log(__dirname)

var child;

io.on('connection', function(socket){
  socket.on('startTraining', function(id){
    console.log("start training");

    child = require('child_process').spawn(
     'python',
     [__dirname+'/trainLenet.py'
     ,id]
     );


    child.stdout.on('data', function(data) {
        console.log('STDOUT!!!!!');

    });
    child.stderr.on('data', function(data) {
        console.log(data.toString());
        socket.emit('result',data.toString());

    });
    child.on('close', function(code) {
        console.log('closing code: ' + code);
        //Here you can get the exit code of the script
    });
  });
  socket.on('disconnect', function(){
    console.log('user disconnected');
  });
  console.log("a user connected");
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});
