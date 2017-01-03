/**
 * Created by Ralph Wen<ralph.wen@gmail.com> on 1/1/17.
 */

let path = require('path');
let webpack = require('webpack');
let ExtractTextPlugin = require('extract-text-webpack-plugin');
let AssetsPlugin = require('assets-webpack-plugin');
let _ = require('lodash');

// PostCSS plugins
const cssnext = require('postcss-cssnext');
const postcssFocus = require('postcss-focus');
const postcssReporter = require('postcss-reporter');

module.exports = {
    entry: {
        main: [
            './src/index.js'
        ]
    },
    output: {
        path: path.join(__dirname, '../static/build'),
        publicPath: '/static/build/',
        filename: '[name].[hash].js',
        chunkFilename: '[id].[hash].js'
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
                loader: ExtractTextPlugin.extract('style-loader', 'css!postcss!sass')
            }, {
                test: /\.css$/i,
                loader: ExtractTextPlugin.extract('style-loader', 'css-loader?importLoaders=1!postcss-loader')
            }, {
                test: /\.(jpe?g|png|gif|svg([\?]?.*))$/i,
                loaders: [
                    'file?context=./&name=[path][name].[hash].[ext]',
                    'image?bypassOnDebug&optimizationLevel=7&interlaced=false'
                ]
            }
        ],
        noParse: /\.min\.js/
    },
    plugins: [
        new webpack.DefinePlugin({
            "process.env": {
                NODE_ENV: JSON.stringify("production")
            }
        }),
        new webpack.optimize.OccurrenceOrderPlugin(),
        new webpack.optimize.AggressiveMergingPlugin(),
        new webpack.optimize.DedupePlugin(),
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false
            }
        }),
        new webpack.NoErrorsPlugin(),
        new ExtractTextPlugin('[name].[hash].css'),
        new AssetsPlugin({
            filename: 'manifest.json',
            path: '../static/build/',
            processOutput: function (assets) {
                return '{"assets":{' + _.map(assets,
                        function (v, k) {
                            var splitPath = v['js'].split('/');
                            var fileName = splitPath[splitPath.length - 1];
                            return '"' + k + '.js":"' + fileName + '","'
                                + k + '.css":"' + fileName.replace('.js', '.css"');
                        }
                    ) + '},"publicPath": "/static/build/"}';
            }
        })
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