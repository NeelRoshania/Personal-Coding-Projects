function sayHello(name) {
    console.log('Hello', name)
}

// Global Node js objects
console.log(window);    // window.console.log
setTimeout();           // window.
clearTimeout();         // window.
setInterval();          // window.
clearInterval();        // window.

// variables not added to the global object, only scoped to app.js
var message = ''

// defining a global function - avoid defining variables in the global scope
//      - Every varibale and function within a file, module, is scoped within it
//      - Every file defined as a module (private)
//      - app.js is tha main module

var sayHello = function() {

}

console.log(module)     // meta information about this file, or module

// adding a new module to an application





