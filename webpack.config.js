const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const CopyPlugin = require('copy-webpack-plugin');
const path = require('path');

let ThemeWatcher;
try {
    ThemeWatcher = require('@salla.sa/twilight/watcher.js');
} catch (e) {
    // Fallback: twilight watcher not available, skip live reload
    ThemeWatcher = null;
}

const asset = file => path.resolve('src/assets', file || '');
const output = file => path.resolve("public", file || '');

const plugins = [
    new MiniCssExtractPlugin({ filename: '[name].css' }),
    new CopyPlugin({
        patterns: [
            { from: asset('images'), to: output('images'), noErrorOnMissing: true },
        ],
    }),
];

if (ThemeWatcher) {
    plugins.push(new ThemeWatcher());
}

module.exports = {
    entry: {
        app: [asset('styles/app.scss'), asset('js/app.js')],
        home: asset('js/home.js'),
    },
    output: {
        path: output(),
        filename: '[name].js',
        clean: false,
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env'],
                    },
                },
            },
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'postcss-loader',
                    { loader: 'sass-loader', options: { api: 'modern-compiler' } },
                ],
            },
        ],
    },
    optimization: {
        minimizer: ['...', new CssMinimizerPlugin()],
    },
    plugins,
};
