// Exercise

//  - Load data from exercise-data.json to mongodb database mongo-exercises and collectio courses
//  - mongoimport --db mongo-exercises --collection courses --drop --file exercise-data.json --jsonArray


// process flow
//  - connect to mongodb database
//  - Define schema and and model
//  - Query data


// dependencies
const mongoose = require('mongoose');

//
// functions
//


async function query(course_model) {

    //  - select all published backened courses
    //  - sort them by name
    //  - pick only the name and author column

    return await course_model
    .find( {isPublished: true, tags: 'backend'} )
    .select({ name: 1, author: 1, tags: 1 })
    .sort({ name: 1 });
}

async function query_2(course_model) {

    //  - select all published frontend and backened courses
    //  - sort them by price in descending
    //  - pick only the name and author column

    // return await course_model
    // .find( {isPublished: true, tags: { $in: [ 'frontend', 'backend'] } } )
    // .select({ name: 1, author: 1, tags: 1, price: 1 })
    // .sort({ price: -1 });

    return await course_model
    .find( {isPublished: true} )
    .or( [ {tags: 'frontend'}, {tags: 'backend'} ] )
    .select({ name: 1, author: 1, tags: 1, price: 1 })
    .sort({ price: -1 });
}

async function query_3(course_model) {

    //  - select all published frontend and backened courses
    //  - where price is greater than 15
    //  - contain the word 'by' in name /pattern/
    //  - pick only the name and author column

    return await course_model
    .find( {isPublished: true} )
    .or([ 
        {price: {$gte: 15}},
        {name: /.*by*/i}
    ])
    .select({ name: 1, author: 1, tags: 1, price: 1 })
    .sort({ price: -1 });
}

//
// MAIN
//

// mongodb connection path
const mongodb_str = "mongodb://localhost:27017/mongo-exercises";

// connect to db else log error
mongoose.connect(mongodb_str)
    .then( () => console.log("Connected to DB...") )
    .catch( (err) => console.log("Error connecting...", err));

// define mongoose scehma for new and existing documents
const courseSchema = new mongoose.Schema({

    tags:           [ String ],
    date:           {  type: Date, default: Date.now},
    name:           String,
    author:         String,
    isPublished:    Boolean,
    price:          Number

});

// map schema to mongoose Model for CRUD operations - singular name of Model
const Course = new mongoose.model('Course', courseSchema);

// start query operations
async function run() {
    
    // need to wrap all promises in an async function
    const courses = await query(Course);
    const course_2 = await query_2(Course);
    const course_3 = await query_3(Course);
    console.log(course_3);
}

run();