// Single responsibility principle - customers.js has all the code for handling Express routing requests for the Customer model


// load requred modules
const { customer_schema, joi_validate_customer } = require('../models/customer'); // object destructuring to capture export properties
const express = require('express');
const router = express.Router();        // define router object for each route
const mongoose = require('mongoose');   // mongoose API

// ...................................................................................................................................
// functions
// ...................................................................................................................................

// get all customers
async function get_customers(req, res) {
    
    try {

        const all_customers = await Customer.find().sort('name');
        res.send({
            status: 'Successfully retrieved all customers',
            customers: all_customers
        })
        
    } catch (err) {

        console.log(Error("Error retrieving all customers"));
        console.log(err);
        res.status(400).send({
            status: 'Could not retrieve customers'
        })

    }

}

// create new customer
async function create_customer(req, res) {

    // create new document
    const new_customer = new Customer({
        isGold: req.body.isGold,
        name: req.body.name,
        phone: req.body.phone
    });

    // attempt to save or catch
    try {

        const result = await new_customer.save();
        res.send({
            status: "New customer created successfully!",
            result: result,
        });

    } catch (err) {

        console.log(new Error("Could not create or save new customer."));
        console.log(err);
        res.status(400).send({status: "Error creating or saving a new customer..."});
        
    }

}

// get a specific customer
async function get_customer(req, res) {

    try {

        // findByID and handle none
        const customer = await Customer.findById(req.params.id);

        // Handle not found
        if (!customer) res.status(400).send({
            status: 'Customer not found..'
        });

        // ..else send customer
        res.send({
            status: 'Customer: ' + req.params.id + ' retrieved.',
            customer: customer,
        });

        
    } catch (err) {

        // log error
        console.log(new Error('Error retrieving customer: ' + req.params.id ));
        console.log(err);
        res.status(400).send({
            status: 'Error retrieving customer: ' + req.params.id 
        });
    }

}

// update a specific customer
async function update_customer(req, res) {

    try {
        
        // To return the updated document, use the findByIdAndUpdate
        const customer_update = await Customer.findByIdAndUpdate(req.params.id, {
            $set: {
                isGold: req.body.isGold,
                name:   req.body.name,
                phone:  req.body.phone
            }
        }, { new: true }); // updated course document is returned; ; { isPiblished: true } can return many results
      
        // Handle not found
        if (!customer_update) res.status(400).send({
            status: 'Customer not found..'
        });

        // ..else send updated customer
        res.send({
            status: 'Updated customer!',
            customer: customer_update
        });

    } catch (err) {
        
        console.log(new Error('Error updating customer:' + req.params.id));
        console.log(err);
        res.status(400).send({ status: 'Error updating customer:' + req.params.id });

    }

}

// delete a specific customer
async function delete_customer(req, res) {

    try {

        // delete a single customer
        const customer_delete = await Customer.findByIdAndRemove(req.params.id);

        // Handle not found
        if (!customer_delete) res.status(400).send({
            status: 'Customer not found..'
        });

        // ..else send updated customer
        res.send({
            status: 'Deleted customer!',
            result: customer_delete 
        });
        
    } catch (err) {

        console.log(new Error('Error deleting customer: ' + req.params.id));
        console.log(err);
        res.status(400).send({
            status: 'Could not delete customer: ' + req.params.id
        });
    }

}

// ...................................................................................................................................
// Initializations
// ...................................................................................................................................

// Create a new instance of Schema that's mapped to a model object
//  - exported from customer.js
const Customer = mongoose.model('Customer', customer_schema); // schema class that automatically generates a plural collection
console.log(Customer);

// ...................................................................................................................................
// External routes handlers
// ...................................................................................................................................

// get all customers
router.get('/all', async (req, res) => {

    // respond to client
    get_customers(req, res)
        .then( () => console.log('Request to get all customers'));

});

// create a new customer
router.post('/', async (req, res) => {

    // Joi validate client body request and return 404 Bad request if not valid
    const { error } = joi_validate_customer(req.body);
    if (error) return res.status(404).send({
        validation: error.details[0].message
    });

    // get current list of customer and create new customer
    create_customer(req, res)
        .then( () => console.log('Request to create new customer'));

});

// get a specific customer
router.get('/:id', async (req, res) => {

    // get customer from request params
    get_customer(req, res)
        .then( () => console.log("Request to retrieve customer"));

});

// update an existing customer
router.put('/:id', async (req, res) => {

    // Joi validate client body request and return 404 Bad request if not valid
    const { error } = joi_validate_customer(req.body);
    if (error) return res.status(404).send({
        validation: error.details[0].message
    });

    // update existing customer
    update_customer(req, res)
        .then( () => console.log("Request to update customer"));

});

// delete customer
router.delete('/:id', async (req, res) => {

    // delete customer of specified id
    delete_customer(req, res)
        .then( () => console.log('Request to delete customer') );

});

// ...................................................................................................................................
// Export routers
// ...................................................................................................................................
module.exports = router;