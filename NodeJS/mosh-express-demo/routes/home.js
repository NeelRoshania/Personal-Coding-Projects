// load requred modules
const express = require('express');
const router = express.Router(); // router instead of app

// Define routes with a callback function/route handler
router.get('/', (req, res) => {
    
    // res.send('Hello world!'); // replace with html markup
    
    // using pug template to generate html markup and pass variables to template
    res.render('index.pug', {title: 'My Express App', message: 'Hello'}); // template_location, object variables

});

module.exports = router; // export router