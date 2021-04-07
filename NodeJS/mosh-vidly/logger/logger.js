// custom middleware function to logg information
function log(req, res, next) {

    // prove access
    console.log('Logger middleware hello...');
    
    next(); // pass control to the next middleware function
}

// export functions
module.exports = log;
