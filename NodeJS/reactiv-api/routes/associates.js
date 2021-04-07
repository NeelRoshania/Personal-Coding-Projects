// Single responsibility principle - customers.js has all the code for handling Express routing requests for the Customer model


// load requred modules
const express = require('express');
const mysql = require('mysql');
const router = express.Router();        // define router object for each route

// ...................................................................................................................................
// Functions
// ...................................................................................................................................

// ...................................................................................................................................
// Initializations
// ...................................................................................................................................


// ...................................................................................................................................
// External routes handlers
// ...................................................................................................................................

// handle home page requests
router.get('/', async (req, res) => {

    // get associates
    res.json({ connectionStatus: "200"})

});

// get all associates
router.get('/all', async (req, res) => {

    // get associates
    const query = "SELECT * FROM associate"
    pool.query(query, (err, results) => {
        
        // handle error state
        if (err) {res.json({ status: "Error querying table" });}
        
        // handle results
        if (!results[0]) {
            res.json({ status: "No results found" });
        } else {
            res.json(results);
        }

    });

});

// create connection to database
const pool  = mysql.createPool({
    host            : process.env.DB_HOST,
    user            : process.env.DB_USER,
    password        : process.env.DB_PASS,
    database        : process.env.DB_NAME,
    socketPath      : `/cloudsql/${process.env.INSTANCE_CONNECTION_NAME}`,
  });

// create new associate
router.post('/newassociate', async (req, res) => {
    
    // define response data schema
    const data = {
        firstName  : req.body.firstName,
        lastName   : req.body.lastName,
        department : req.body.department
    }

    // define and produce query 
    const query = "INSERT INTO associate (firstName, lastName, department) VALUES (?, ?, ?)";
    pool.query(query, Object.values(data), (error) => {
        if (error) {
        res.json({ status: "failure", reason: error.code  });
        } else {
        res.json({ status: "Successfully inserted new associate", data: data});
        }
    });
});

// ...................................................................................................................................
// Export routers
// ...................................................................................................................................
module.exports = router;