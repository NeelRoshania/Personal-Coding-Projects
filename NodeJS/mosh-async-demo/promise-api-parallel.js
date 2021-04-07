// Promise Parallel
//
// 
// Running Promises in parralel
//  - Processes start at the same time
//  - Does not depend on the completion of other promises
//  - If any promises rejected, no data will be available

// define process 1
const p1 = new Promise((resolve, reject) => {
    
    // simulate first async operation
    setTimeout( () => {
        console.log('Calling API 1...');
        // reject(new Error('Failed to call API 1'));
        resolve(1);
    }), 2000;

});

// define process 2
const p2 = new Promise((resolve) => {
    
    // simulate first async operation
    setTimeout( () => {
        console.log('Calling API 2...');
        resolve(2);
    }), 2000;

});

// Kick of promises and get results of each
Promise.all([p1, p2])
    .then(result => console.log(result))
    .catch(err => console.log('Error: ', err));