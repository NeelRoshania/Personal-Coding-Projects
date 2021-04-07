// Using the Promise API
//      - To simulate failed or resolved promises

// calling a resolved promise
const p = Promise.resolve({ id: 1});
p.then(result => console.log(result));

// calling a rejected promise with a native error object to include the call stack
const r = Promise.reject(new Error('Simulating a failed rejection...'));
r.catch(err => console.log(err));
