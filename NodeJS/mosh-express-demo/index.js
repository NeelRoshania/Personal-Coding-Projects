// Express documentation: https://expressjs.com/en/4x/api.html


// Startup instructions
//      - nodemon index.js

// Notes
//      - vscode cannot switch between environment variables

// *********************************************
// functions
// *********************************************

// load dependencies

// debuggers subject to environment variable, DEBUG
//  - One namespace:                setx DEBUG app:startup OR export DEBUG=app:startup
//  - No namespaces:                setx DEBUG None OR export DEBUG=
//  - Multiple namespaces:          setx DEBUG app:startup,app:db OR export DEBUG=app:startup,app:db
//  - All namespaces:               setx DEBUG app:* OR export DEBUG=app:*
//  - Set env variables on start:   ...cannot be done on windoes :( OR $DEBUG=app:db nodemone index.js 

// best practice: minimize number of debugger objects
const startupDebugger = require('debug')('app:startup'); // define namespace for reference to env var DEBUG
const dbDebugger = require('debug')('app:db'); // define namespace for reference to env var DEBUG

// core app dependecies
const config = require('config');
const express = require('express');
const helmet = require('helmet');
const morgan = require('morgan');
app = express();

// external routers to handle classifications of routes
const courses = require('./routes/courses');
const home = require('./routes/home');
const posts = require('./routes/posts');
const logger = require('./logger');

// loading HTML templating engine
//  - views/.pug

app.set('view engine', 'pug'); // set view engine for application
// app.set('views', './views') // optional - place all templates in folder views

// Install middeleware functions

// Specify environment variables - This seems redundent, refer to notes on vscode
// require('dotenv').config(); // Specify env variable in .env file

// App configuration settings
//  - config module documentation: https://docs.npmjs.com/cli/config
//  - The config module references json files from config folder based on the specified environment
//  - For windows, 'set' creates and stores variables temporarily and will be forgotted when the terminal is closed
//  - Use setx app_password 1234, then restart the terminal new env variables to take effect
startupDebugger('Application Name: ' + config.get('name'));
startupDebugger('Mail Server: ' + config.get('mail.host'));
startupDebugger("app.get('env'): ", app.get('env'));
startupDebugger("Mail password: ", config.get('mail.password')); // custome-environmen-variables.json reads custom environment variables 
startupDebugger("NODE_ENV: ",   process.env.NODE_ENV);

dbDebugger('Connected to the database....'); // example dbDebugger
// Environment types
//  - Development, testing, staging, production 

// Development only
// if (process.env.NODE_ENV === 'development') { // access specific environment variable
if (app.get('env') === 'development') {

    // get the current environment that returns development by default
    //      - Access environment variables process.env.NODE_ENV
    
    app.use(morgan('tiny')); // log http requests in the console by default. Specify format of logging, in this case, tiny.
    startupDebugger("Morgan enabled...");

}

// Development and production environments 


// Middleware integration

// built in middleware
app.use(express.json()); // parse body of request object to json if detected
app.use(express.urlencoded({ extended: true })); // parses url key-value payloads into JSON in the body of the request   
app.use(express.static('static_assets')); // serve static resources to client when url requests for it
app.use(logger); // execute custom middleware function

// middleware for similar route endpoints - refer to routes folder
app.use('/', home);
app.use('/api/courses', courses);
app.use('/api/posts', posts);

// Express thirdparty middleware
//  - requires npm module installation
//  - documentation: https://expressjs.com/en/resources/middleware.html
app.use(helmet()); // helps secure apps by setting various HTTP headers

// Instantiations

// *********************************************
// route handlers
// *********************************************

// - all routers are custom middleware callback functions
//      - Nevertheless they have been strucutred according to their endpoints in the routes folder

// Setup port listeners
PORT = process.env.PORT || 3000;
app.listen(3000, () => startupDebugger(`Listening to port ${PORT}`));
