// Promises objects
//      - Asynchronous functions with callbacks should be modified to include promises
//      - Accepts user defined functional arguments 
//      - Instantiated objects return two methods, then and catch


const p = new Promise((resolve, reject) => {

    // kick off asychronous operations
    setTimeout( () => {

        // pending -> resolved
        resolve(1);

        // pending -> rejected
        reject(new Error('Error message...'));

    }, 2000 );

});


// Consuming promises
//      - then: for the success scenario
//      - catch: for the failed scenario
//      - p can be a const or a function

p
 .then(result => console.log('Result of promise: ', result))
 .catch(err => console.log('Error: ', err.message));