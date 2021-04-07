// Promise Race
//
// 
// Running Promises in parralel
//  - Processes start at the same time
//      - Does not depend on the completion of other promises
//      - Refer to functional promise chaining
//  - If any promises rejected, no data will be available

// define process 1
const p1 = new Promise((resolve, reject) => {
    
    // simulate first async operation
    setTimeout( () => {
        console.log('Calling API 1...');
        // reject(new Error('Failed to call API 1'));
        resolve(1); // pass 1 as the result of a resolved promise
    }), 2000;

});

// define process 2
const p2 = new Promise((resolve) => {
    
    // simulate first async operation
    setTimeout( () => {
        console.log('Calling API 2...');
        resolve(2); // pass 2 as the result of a resolved promise
    }), 2000;

});

// Do something (log to console) as soon as one of the async procceses are complete
//      - As soon as one promise is fulfilled, it's result will be passed as the final result
//      - In this case, result of promise 1 is delivered before 2

Promise.race([p1, p2])
    .then(result => console.log(result))
    .catch(err => console.log('Error: ', err));
