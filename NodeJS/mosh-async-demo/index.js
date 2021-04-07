// Asynchronous patterns
//      - Callbacks: When the result of an asynchronous function is ready, the callback function is called with output passed to the argument
//      - Promises
//      - Async/wait

// Notes
//      - Named Functions: To avoid ambiguety, defined name of function with named_
//      - functions that return new Promise objects need to be consumed to execute

//
//
// NAMED FUNCTIONS
//  - Named asynchronous functions to replace anonymous callback functions
//  - Function name may have the same name, but signatures are different because they take in different arguments
//

function named_getRepositories(user) {
    getRepositories(user.githubUsername, named_getCommits);
}

function named_getCommits(repos) {
    getCommits(repos, displayCommits); // not calling displayCommits, only making reference to it
}

function displayCommits(commits) {
    console.log('Commits found: ', commits);
}

//
// Asynchronous functions
//      - Modified to include asynchronous promises
//

// get user data from database of id 1
function getUser(id) {
    return new Promise( (resolve_callback, reject_callback) => {

        // schedule a task for the future 2000ms
        setTimeout(() => {

            console.log('Reading database...');
            const db_result = { id: id, githubUsername: 'mosh'}; // database returns a record object
            // return { id: id, githubUsername: 'mosh'} // will only be available after n seconds and likely may return none
            
            // once ready, pass result to a callback function or reject
            resolve_callback(db_result);
            // reject_callback(new Error('Failed to reach API...'));

        }, 2000);

    });
}

// get github repositories from github api asynchronously
function getRepositories(user) {
    return new Promise( (resolve_callback, reject_callback) => {
        
        // simulate 2s api request
        setTimeout(() => {

            console.log(`Getting repositories of user: ${user}`);
            const api_result = ['repo1', 'repo2', 'repo3'];
            
            // once ready, pass result to a callback function
            resolve_callback(api_result);

        }, 2000);
        
    });
}

// get github commits of all repos returned
function getCommits(repos) {
    return new Promise( (resolve_callback, reject_callback) => {

        // simulate 2s api request
        setTimeout(() => {

            console.log('Getting commits of repos: ', repos);
            const api_result = ['commit1', 'commit2', 'commit3']; 
            
            // once ready, pass result to a callback function
            resolve_callback(api_result);

        }, 2000);

    });    
}

// MAIN

console.log('Before non-blocking...');

// Dealing with christmas tree problem - replace anonymous functions with named functions
//  - anonymous function: () => {}
//  - start at deepest level

const user_id = 1;


// // 1. Named callback functions
// getUser(user_id, named_getRepositories);

// // 2. Anonymous callback functions
// getUser(1, (user) => {
//     getRepositories(user, (repos) => {
//         getCommits(repos, (commits) => {
//             console.log('Commits found: ', commits);
//         });
//     });
// });

// 3. Chained functions that return Promises
//      - Consuming promises by chaining dependent functional promises  
//          - getUser output passed to getRepositories, then passed to getCommits etc
//          - promises are chained dependently, with each promise waiting for the previous before executing
getUser(user_id)
    .then(user => getRepositories(user.githubUsername))
    .then(repos => getCommits(repos))
    .then(commits => console.log('Commits found: ', commits))
    .catch(err => console.log('Error: ', err.message)); // error handling


console.log('After Before non-blocking...');

// END MAIN 