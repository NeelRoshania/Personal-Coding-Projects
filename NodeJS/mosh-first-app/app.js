// Node JS Documentation: https://nodejs.org/dist/latest-v12.x/docs/api/

// Notes
//  - Using HTTP Module to create a webserver that listens for HTTP requests
//  - The server needs to be restarted whenever code changes are made
//  - Adding more routes makes the code more complex within one callback function
//      - Use Express Framework to manage such complexities

// load module
const http = require('http');

// instantiate server object to handle request and response events
const server = http.createServer((req, res) => {
    
    // handle custome routes

    // send something to the client localhost:3000/
    if (req.url === '/') {
        res.write('Hello world!');
        res.end();
    }

    // handle api point localhost:3000/api/courses
    if (req.url === '/api/course') {

        // convert array object to string and write to response
        res.write(JSON.stringify([1, 2, 3]));
        res.end();
    }


}); // inherits Server, which inherits EventEmiiter

// listen on port 3000
server.listen(3000)
console.log("Listening on port 3000...");