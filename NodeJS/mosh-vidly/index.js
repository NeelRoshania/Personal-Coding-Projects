// ...................................................................................................................................
// Vidly
//     - Vidly is a video streaming platform competes with Netflix by providing niche fantasy series and movies

// Services    
//     - A back-end service to handle data pertaining to various genres 

// Known Bugs
//     - Delete route deletes more than one genre object
//          - Fixed by specifiying variable type and unique name

// Notes
//     - logger.js log middlware function only accessed when a REST Call is made

// ...................................................................................................................................


// ...................................................................................................................................
// functions
// ...................................................................................................................................


// ...................................................................................................................................
// dependencies
// ...................................................................................................................................
const Express = require('express');
const rt_genres = require('./routes/genres');      // external routers to handle classifications of routes
const rt_customers = require('./routes/customers');      // external routers to handle classifications of routes
const logger = require('./logger');             // custome middleware
const mongoose = require('mongoose');           // mongoose API

// ...................................................................................................................................
// instantiations
// ...................................................................................................................................
app = Express();

// ...................................................................................................................................
// Install and use middleware functions
// ...................................................................................................................................

// - These functions intercept the request response cycle
// - app.use to integrate existing functions or create custom ones
// - ***They're called in sequence of being defined when a REST call is made

// ...................................................................................................................................

// built-in express middleware including custom user defined functions
app.use(Express.json()); // parse body of request object to json if detected

// custom middleware functions
app.use(logger);

// routers handlers by external reference
app.use('/api/genres', rt_genres);
app.use('/api/customers', rt_customers);

// ...................................................................................................................................
// Connect to MongoDB
// ...................................................................................................................................

// mongodb connection path
const mongodb_str = "mongodb://localhost:27017/mosh-vidly";

// .connect returns a promise
mongoose.connect(mongodb_str)
    .then( () => console.log('Connected to MongoDB...'))
    .catch( err => console.log('Could not connect to MongoDB', err));

// ...................................................................................................................................
// Setup port listener
// ...................................................................................................................................
const PORT = process.env.PORT || 3000;
app.listen(3000, () => console.log(`Listening on port ${PORT}`));