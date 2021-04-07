// load requred modules
const express = require('express');
const router = express.Router(); // router instead of app


// return a single course by defining a parameter on the api endpoint
router.get('/:year/:month', (req, res) => {

    // read the request api route params object as defined above 
    res.send(req.params);

});

module.exports = router; // export router