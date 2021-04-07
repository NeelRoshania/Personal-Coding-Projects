// custom middleware function to logg information
function log(req, res, next) {

    // prove access
    console.log('Logging...');
    
    // pass control to the next middleware function
    next();
}

// export functions
module.exports = log;
