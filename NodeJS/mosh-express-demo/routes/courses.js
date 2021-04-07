// load requred modules
const express = require('express');
const Joi = require('@hapi/joi');
const router = express.Router(); // router instead of app


// *********************************************
// functions
// *********************************************

// decoupling validation logic for the course object
function validateCourse(course) {

    // Define Joi schema object
    const schema = Joi.object({
        name:   Joi.string().min(3).required()
    });

    // perform validation on schema object
    return schema.validate(course);

}

// these routes would are defined to follow the convention of /apo/courses
//      - This file is loaded as an object in index.js that maps to /api/courses
//      - Therefore, below routes do not need to contain it

// instantiations
courses = [
    {id: 1, name: 'course_1'},
    {id: 2, name: 'course_2'},
    {id: 3, name: 'course_3'}
]


// http get all courses
router.get('/', (req, res) => {
    
    // get list of courses from database and return them
    res.send(courses);

});

// http post to create a new db object
router.post('/', (req, res) => {

    // object destructuring i.e retrieving the key of interest within the object of interest
    const { error } = validateCourse(req.body);
    if (error) return res.status(400).send(error.details[0].message);

    const course = {
        id: courses.length + 1,
        name: req.body.name
    };

    courses.push(course);
    res.send(course);

});

// http get a course with a single id
router.get('/:id', (req, res) => {
      
    // check to see if course object exists, return 404 and exit route handler
    const course = courses.find(course => course.id == parseInt(req.params.id));
    if (!course) return res.status(404).send("404: Course not found");
    
    // otherwise send course to client
    res.send(course) 

});

// updating and already existing course objects with one object
router.put('/:id', (req, res) => {

    // check to see if course object exists, return 404 and exit route handler
    const course = courses.find(course => course.id == parseInt(req.params.id));

    // destructure error key from Joi
    if (!course) return res.status(404).send("404: Course not found");
    const { error } = validateCourse(req.body);

    // if validation error encountered, return object to client and end route through return
    if (error) return res.status(400).send(error.details[0].message);

    // Update course
    course.name = req.body.name;
    res.send(course)

});

// delete a specific object
router.delete('/:id', (req, res) => {

    // check to see if course object exists, return 404 and exit route handler
    const course = courses.find(course => course.id == parseInt(req.params.id));
    if (!course) return res.status(404).send("404: Course not found");

    // find object to delete and remove with splice
    const index = courses.indexOf(course);
    courses.splice(index, 1);

    // return response to client
    res.send(course);

});

module.exports = router; // export router