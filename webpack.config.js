var webpack=require('webpack');

module.exports = {
     entry: './ide/static/js/index.js',
     output: {
         path: './ide/static/bundle/',
         filename: 'bundle.js',
     },
     module: {
         loaders: [{
             test: /\.js$/,
             exclude: /node_modules/,
             loader: 'babel-loader',
         },
         { test: /\.css$/, loaders: ["style", "css"] },
         {test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: 'file'},
        {test: /\.(woff|woff2)$/, loader: 'url?prefix=font/&limit=5000'},
        {test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=application/octet-stream'},
        {test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=image/svg+xml'}
         ]
     }
 }
