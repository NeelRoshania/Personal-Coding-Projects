// Single responsibility principle - customer.js has all the code for defining and validating a customer object

// create a mongoose schema and map to a MongoDB schema - optional volidation logic
// - mongoose validation: https://mongoosejs.com/docs/validation.html
// - mongoose SchemaType Options: https://mongoosejs.com/docs/schematypes.html#schematype-options
// - mongoose Getter/Setters: https://mongoosejs.com/docs/tutorials/getters-setters.html
// - load genres: mongoimport --db mongo-exercises --collection courses --drop --file load-genres.json --jsonArray


// module dependencies
const mongoose = require('mongoose');   // mongoose API
const Joi = require('@hapi/joi');

// ...................................................................................................................................
// functions
// ...................................................................................................................................

function joi_validate_genre(request_object) {

    // perform validation logic for the request_object object

    // Define Joi schema object
    const schema = Joi.object({
        name:   Joi.string().min(3).required()
    });

    // return validation results object
    return schema.validate(request_object);

}

// ...................................................................................................................................
// Model definition
// ...................................................................................................................................

const genre_schema = new mongoose.Schema({
    name: { 
        type: String, 
        required: true,
        minlength: 5,
        maxlength: 20,
        // match: /pattern/ // match string on regex
    }, // these are known as SchemaType Options
    date: { type: Date, default: Date.now }
});

// export models and functions
exports.genre_schema = genre_schema;
exports.joi_validate_genre = joi_validate_genre;