/**
 * Created by Ralph Wen<ralph.wen@gmail.com> on 1/1/17.
 */

let path = require('path');
let webpack = require('webpack');

// PostCSS plugins
const cssnext = require('postcss-cssnext');
const postcssFocus = require('postcss-focus');
const postcssReporter = require('postcss-reporter');

module.exports = {
    devServer: {
        hot: true,
        inline: true,
        host: 'localhost',
        port: 3456
    },
    devtool: 'cheap-module-source-map',
    entry: {
        'debug-bundle': [
            './src/index.js'
        ]
    },
    output: {
        path: path.join(__dirname, '../static/build'),
        publicPath: 'http://localhost:3456/assets/',
        filename: '[name].js'
    },
    resolve: {
        extensions: ['', '.js', '.css']
    },
    module: {
        loaders: [
            {
                test: /\.js$/i,
                loaders: ['babel-loader'],
                include: [path.resolve(__dirname, './src')]
            }, {
                test: /\.scss$/i,
                loader: 'style!css!postcss!sass-loader!postcss-loader'
            }, {
                test: /\.css$/i,
                loader: 'style-loader!css-loader?importLoaders=1&sourceMap'
            }, {
                test: /\.(jpe?g|png|gif|svg([\?]?.*))$/i,
                loaders: [
                    'file-loader',
                    'image-webpack-loader?{progressive:true, optimizationLevel: 7, interlaced: false, pngquant:{quality: "65-90", speed: 4}}'
                ]
            }
        ],
        noParse: /\.min\.js/
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin()
    ],
    // Process the CSS with PostCSS
    postcssPlugins: [
        postcssFocus(), // Add a :focus to every :hover
        cssnext({ // Allow future CSS features to be used, also auto-prefixes the CSS...
            browsers: ['last 2 versions', '> 1%'] // ...based on this browser list
        }),
        postcssReporter({ // Posts messages from plugins to the terminal
            clearMessages: true
        })
    ]
};