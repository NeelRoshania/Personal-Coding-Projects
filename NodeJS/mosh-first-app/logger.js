// logger.js module
// All commandas are scoped to this module only

// Instantiate EventEmtter object
const EventEmitter = require('events'); // load events module as assign to class
var url = 'http://mylogger.io/log';

// extends the base class EventEmitter
class Logger extends EventEmitter {

    // Purpose, 
    //  - This class raises a unique event 'messageLogged'
    //  - Encapsulate emmiter objects together so that all events can be detected without ambiguety
    //  - Have all the capabilities of the EventEmitter Class

    // Class method log
    log(message) {

        // send http request
        console.log(message);
    
        // Raise: messageLogged event
        //  - As Logger inherits EventsEmitter, it's base methods can be called too
        //  - Pass data through event argument read as eventArg, arg, or whatever
        this.emit('messageLogged', { id: 1, data: {id: 1, url: 'http://...'} });
    
    }
}


// update module object have access to the function directly
module.exports = Logger;