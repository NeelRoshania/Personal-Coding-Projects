// Single responsibility principle - customer.js has all the code for defining and validating a customer object

// create a mongoose schema and map to a MongoDB schema - optional volidation logic
// - mongoose validation: https://mongoosejs.com/docs/validation.html
// - mongoose SchemaType Options: https://mongoosejs.com/docs/schematypes.html#schematype-options
// - mongoose Getter/Setters: https://mongoosejs.com/docs/tutorials/getters-setters.html
// - load customers: mongoimport --db mongo-exercises --collection courses --drop --file load-genres.json --jsonArray

// module dependencies
const mongoose = require('mongoose');   // mongoose API
const Joi = require('@hapi/joi');

// ...................................................................................................................................
// functions
// ...................................................................................................................................

function joi_validate_customer(request_object) {

    // perform validation logic for the request_object object

    // Define Joi schema object
    const schema = Joi.object({
        isGold: Joi.boolean(),
        name:   Joi.string().min(3).max(50).required(),
        phone:  Joi.string().min(3).max(50).required()
    });

    // return validation results object
    return schema.validate(request_object);

}

// ...................................................................................................................................
// Model definition
// ...................................................................................................................................

const customer_schema = new mongoose.Schema({
    isGold: { 
        type: Boolean, 
        required: true
        // match: /pattern/ // match string on regex
    }, // these are known as SchemaType Options
    name: {
        type: String,
        required: true,
        minlength: 3,
        maxlength: 50
    },
    phone: {
        type: String,
        required: true,
        minlength: 12,
        maxlength: 12
    },
    date: { type: Date, default: Date.now }
});

// export models and functions
exports.customer_schema = customer_schema;
exports.joi_validate_customer = joi_validate_customer;
