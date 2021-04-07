// Using Mongo DB
//  - Creates a database, playground
//  - Defines a table/collection, courses
//  - Inserts a new row/document

// Setup
//  - npm init --yes
//  - npm i mongoose

// MongoDB Basics
//  - mongodb collection -> sql table
//  - mongodb document -> sql row
//  - Types
//      - String, Number, Date, Buffer, Boolean, ObjectID, Array
//      - Buffer -> Binary data

// mongoose
//  - Schema defines shape of documents in a mongodb collection
//  - Uses Object Relational Mapping for CRUD operations


//
// Functions
//

// save document to collection asychnronously
async function createCourse() {

    // create a row/map to a document in a mongodb database
    const course = new Course({
        name: 'Node.js course',
        author: 'Mosh',
        tags: ['angular', 'frontend'],
        category: 'Web',
        tags: ['front-end'],
        isPublished: true,
        price: 17.8
    }); // date defualted to now
 
    // validate with built-in validators
    // save to database using a asychronous operation
    // try {
    //     //  - Handle validation based promise rejections here
    //     //  - Use front and back end validation
    //     //  - Using default course object validation
    //     course.validate( (err) => {
    //         if (err) {
    //             console.log(new Error('Validation logic violated...'))
    //         } else {
    //             course.save();
    //         }
    //     }); // returns promise of void;
    // }
    // catch (exception) {
    //     console.log(exception);
    // }

    // create course document inclusive of custom validation logic and messaging
    try {
        
        const result = await course.save();
        console.log(result);
    
    } catch (exception){

        // iterate between validation errors
        for (field in exception.errors)
            console.log(exception.errors[field]);
            // console.log(exception.errors[field].message); // display message property of ValidationError object only
    
    }
}

// retrieve documents from a mongoose collection
async function getCourses() {

    // Pagination using skip
    //  - skip the first pageSize results of the current pageNumber then limit by pageSize

    // From end point query string parameters /api/courses/pageNumber=2&pageSize=10
    const pageNumber = 1;
    const pageSize = 10;

    // count courses where author starts with 'Mosh'
    // .find({ author: 'Mosh', isPublished: true })    
    const filtered_courses_regex_1 = await Course
        .find({ author: /^Mosh/ })
        .skip((pageNumber-1) * pageSize)
        .limit(pageSize)
        .sort({ name: 1 })
        .select({ name: 1, author: 1, isPublished: 1, price: 1});

    // console.log(courses);
    console.log(filtered_courses_regex_1);
    // console.log(filtered_courses_regex_1[3].price); // price property of 4th object will be rounded based on SchemaType Option validators

}

// update mongodb document in database by retrieving it first
async function update_course_document_approach_1(id) {

    // Approach 1: query first
    //     - findbyId()
    //     - Modify its properties
    //     - save()

    const course = await Course.findById(id).exec((err, doc) => {

        // handle server error else continue
        if (err) {
            console.log(new Error('Error finding course...'))
            console.log('MongoDB Error: ', err);
            return;
        } else {

            if (!doc) return; // exit function if course document is null

            doc.set({
                isPublished: false,
                author: 'Another Author'
            });

            doc.save();

            console.log(doc);
            return doc;
        }

    }); // id shouldn't be part of the schema

    // save the changes
    if (!course) {
        const result = await course.save();
        console.log(result);    
    } else {
        console.log('Could not retrieve course documents...')
    }
}

// update mongodb document directly in database without retrieving it first
async function update_course_document_approach_2(id) {

    // Approach 2: update first
    //     - Update directly in mongodb
    //     - Optionally: get the updated document
    
    // pass a query object
    const result = await Course.update({_id: id}, {
        $set: {
            author: 'Mosh',
            isPublished: true
        }
    }); // result is returned, not document
    console.log(result);

    // To return the updated document, use the findByIdAndUpdate
    const course = await Course.findByIdAndUpdate(id, {
        $set: {
            author: 'Jack',
            isPublished: false
        }
    }, { new: true }); // updated course document is returned; ; { isPiblished: true } can return many results
    console.log(course);

}

// remove mongodb document directly in database without retrieving it first
async function remove_document(id) {

    // delete one or many document
    // const result = await Course.deleteOne({ _id: id }); // find the first object and delete it; { isPiblished: true } can return many results
    const result = await Course.deleteMany({ _id: id }); // find the first object and delete it; { isPiblished: true } can return many results
    console.log(result); // returns null if nothing is to be deleted

    // delete document by Id
    const course = await Course.findByIdAndRemove(id); // find document by id and delete it,  returns the document deleted
    console.log(course);
    
}

//
// MAIN
//

// Retrieve/connect to mongoose client
const mongoose = require('mongoose');

// mongodb connection path
const mongodb_str = "mongodb://localhost:27017/playground";

// .connect returns a promise
mongoose.connect(mongodb_str)
    .then( () => console.log('Connected to MongoDB...'))
    .catch( err => console.log('Could not connect to MongoDB', err));

// create a mongoose schema with volidation logic and map to a MongoDB schema
// - mongoose validation: https://mongoosejs.com/docs/validation.html
// - mongoose SchemaType Options: https://mongoosejs.com/docs/schematypes.html#schematype-options
// - mongoose Getter/Setters: https://mongoosejs.com/docs/tutorials/getters-setters.html

const courseSchema = new mongoose.Schema({
    name: { 
        type: String, 
        required: true,
        minlength: 5,
        maxlength: 355,
        // match: /pattern/ // match string on regex
    }, // these are known as SchemaType Options
    category: {
        type: String,
        lowercase: true, // automatically convert input to lowercase
        required:true,
        enum: ['web', 'mobile', 'network'] // allow on this enumerated object as an input
    },
    author: String,
    tags: {
        type: Array,
        validate: {
            validator: function(v) {
                return v && v.length > 0;
            },
            message: 'A course should have atleast one tag'
        } // custom validation logic with validate property - if v is empty and less than 0 length, trigger validation error
    },
    date: { type: Date, default: Date.now },
    isPublished: Boolean,
    price: {
        type: Number,
        required: function() { return this.isPublished }, // if isPublished is true, required the price
        min: 10,
        max: 200,
        get: v => Math.round(v), // handling get requests when reading value of a property 
        set: v => Math.round(v) // handling set requests when setting value of a property
    }
});

// Create a new instance of Schema that's mapped to a model object
const Course = mongoose.model('Course', courseSchema); // schema class that automatically generates a plural collection

// createCourse(); // create/insert a new document
getCourses(); // find all courses in database
// update_course_document_approach_1('5ee35c4cc041093ee43c04bf');
// update_course_document_approach_2('5ee35c4cc041093ee43c04bf');
// remove_document('5ee35c4cc041093ee43c04bf');

