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
            const api_result = ['commit1', 'commit2', 'commit3']; // remove commit3 to trigger resolve error
            
            // once ready, pass result to a callback function
            if (api_result.length === 3) {
                resolve_callback(api_result);
            } else {
                reject_callback("Failed to get commits...");
            }
            
            // reject_callback(new Error('**Could not get commits!'));
        }, 2000);

    });    
}

// MAIN

console.log('Before non-blocking...');
const user_id = 1; // get user of id 1

// 4. Async and Await approach (synatactical sugar approach)
//  - async function { const user = await getUser(1)}
//  - Looks and read synchronously, but still operates using promises

async function display_output() {

    //  - Not catch method to chain, like promise based chaining
    //      - Wrap code in try catch block
    try {
        
        const user    = await getUser(user_id); // js will release the thread and make it available for other work
        const repos   = await getRepositories(user.githubUsername);
        const commits = await getCommits(repos);

        console.log('Commits: ', commits);

        
    } catch (err) {
        console.log(new Error('Async Error'));
        console.log('Error returned by Promise object: ', err);
    }

}

// trigger async function
display_output();


console.log('After Before non-blocking...');

// END MAIN 