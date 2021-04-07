// load requred modules
const { genre_schema, joi_validate_genre } = require('../models/genre'); // object destructuring to capture export properties
const express = require('express');
const router = express.Router();        // define router object for each route
const mongoose = require('mongoose');   // mongoose API

// ...................................................................................................................................
// functions
// ...................................................................................................................................

// get all genres
async function get_genres(req, res) {
    
    try {

        const all_genres = await Genre.find().sort('name');
        res.send({
            status: 'Successfully retrieved all genres',
            genres: all_genres
        })
        
    } catch (err) {

        console.log(Error("Error retrieving all genres"));
        console.log(err);
        res.status(400).send({
            status: 'Could not retrieve genres'
        })

    }

}

// create new genre
async function create_genre(req, res) {

    // create new document
    const new_genre = new Genre({
        name: req.body.name
    });

    // attempt to save or catch
    try {

        const result = await new_genre.save();
        res.send({
            status: "New genre created successfully!",
            result: result,
        });

    } catch (err) {

        console.log(new Error("Could not create or save new genre."));
        console.log(err);
        res.status(400).send({status: "Error creating or saving a new genre..."});
        
    }

}

// get a specific genre
async function get_genre(req, res) {

    try {

        // findByID and handle none
        const genre = await Genre.findById(req.params.id);

        // Handle not found
        if (!genre) res.status(400).send({
            status: 'Genre not found..'
        });

        // ..else send genre
        res.send({
            status: 'Genre: ' + req.params.id + ' retrieved.',
            genre: genre,
        });

        
    } catch (err) {

        // log error
        console.log(new Error('Error retrieving genre: ' + req.params.id ));
        console.log(err);
        res.status(400).send({
            status: 'Error retrieving genre: ' + req.params.id 
        });
    }

}

// update a specific genre
async function update_genre(req, res) {

    try {
        
        // To return the updated document, use the findByIdAndUpdate
        const update_genre = await Genre.findByIdAndUpdate(req.params.id, {
            $set: {
                name: req.body.name,
            }
        }, { new: true }); // updated course document is returned; ; { isPiblished: true } can return many results
      
        // Handle not found
        if (!update_genre) res.status(400).send({
            status: 'Genre not found..'
        });

        // ..else send updated genre
        res.send({
            status: 'Updated genre!',
            updated_genre: update_genre
        });

    } catch (err) {
        
        console.log(new Error('Error updating genre:' + req.params.id));
        console.log(err);
        res.status(400).send({ status: 'Error updating genre:' + req.params.id });

    }

}

// delete a single genre
async function delete_genre(req, res) {

    try {

        // delete a single genre
        const genre_delete = await Genre.findByIdAndRemove(req.params.id);

        // Handle not found
        if (!genre_delete) res.status(400).send({
            status: 'Genre not found..'
        });

        // ..else send updated genre
        res.send({
            status: 'Deleted genre!',
            result: genre_delete 
        });
        
    } catch (err) {

        console.log(new Error('Error deleting genre: ' + req.params.id));
        console.log(err);
        res.status(400).send({
            status: 'Could not delete genre: ' + req.params.id
        });
    }

}

// ...................................................................................................................................
// Initializations
// ...................................................................................................................................

// Create a new instance of Schema that's mapped to a model object
const Genre = mongoose.model('Genre', genre_schema); // schema class that automatically generates a plural collection
console.log(Genre);

// ...................................................................................................................................
// External routes handlers
// ...................................................................................................................................

// get all genres
router.get('/all', async (req, res) => {

    // respond to client
    get_genres(req, res)
        .then( () => console.log('Request to get all genres'));

});

// create a new genre
router.post('/', async (req, res) => {

    // Joi validate client body request and return 404 Bad request if not valid
    const { error } = joi_validate_genre(req.body);
    if (error) return res.status(404).send({
        validation: error.details[0].message
    });

    // get current list of genres and create new genre
    create_genre(req, res)
        .then( () => console.log('Request to create new genre'));

});

// get a specific genre
router.get('/:id', async (req, res) => {

    // get genre from request params
    get_genre(req, res)
        .then( () => console.log("Request to retrieve genre"));

});

// update an existing genre
router.put('/:id', async (req, res) => {

    // Joi validate client body request and return 404 Bad request if not valid
    const { error } = joi_validate_genre(req.body);
    if (error) return res.status(404).send({
        validation: error.details[0].message
    });

    // update existing genre
    update_genre(req, res)
        .then( () => console.log("Request to update genre"));

});

// delete a genre
router.delete('/:id', async (req, res) => {

    // delete genre of specified id
    delete_genre(req, res)
        .then( () => console.log('Request to delete genre') );

});

// ...................................................................................................................................
// Export routers
// ...................................................................................................................................
module.exports = router;