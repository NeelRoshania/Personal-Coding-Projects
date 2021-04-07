// script to establish connection to the database

// dependencies
const express = require("express");
const mysql = require('mysql');
// const config = require("config");
// const app = express();

// create connection to database
const pool  = mysql.createPool({
    host            : process.env.DB_HOST,
    user            : process.env.DB_USER,
    password        : process.env.DB_PASS,
    database        : process.env.DB_NAME,
    socketPath      : `/cloudsql/${process.env.INSTANCE_CONNECTION_NAME}`,
  });
  
// check status
pool.getConnection(function(err, connection) {
      if (err) throw err; // failed to connect
      console.log('Connection established.');
  });

// ...................................................................................................................................
// Export routers
// ...................................................................................................................................
module.exports = pool;

