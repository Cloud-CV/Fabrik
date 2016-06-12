var webpack=require('webpack');

module.exports = {
     entry: './cloudcvIde/static/cloudcvIde/js/index.js',
     output: {
         path: './cloudcvIde/static/cloudcvIde/bundle/',
         filename: 'bundle.js',
     },
     plugins: [
        new webpack.ProvidePlugin({ 
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery' 
        })
    ],
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