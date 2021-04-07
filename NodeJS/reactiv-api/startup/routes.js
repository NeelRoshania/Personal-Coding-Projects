const express = require('express');
const associates = require('../routes/associates');      // external routers to handle classifications of routes
// const logger = require('./logger');             // custome middleware
// const mongoose = require('mongoose');  

// schemas
module.exports = function(app) {
    app.use(express.json());
    app.use('/associates', associates);
    // app.use(error);
  }