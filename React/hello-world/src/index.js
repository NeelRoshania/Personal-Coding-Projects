// es6 models

// import modules
import React from "react";
import ReactDOM from "react-dom";

// define element object and set to JSX expression as part of virtual DOM
// - Babel will boil JSX to React.createElement. This is why 'React' is required
// - This virtual DOM Object will be tracked and updated for changes in React
const element = <h1>Hello World</h1>;

// render the object element to HTML DOM id of root
ReactDOM.render(
    element, 
    document.getElementById("root")
    );

// In the real world,
// - Singular object element wont be rendered, but rather a react component!
