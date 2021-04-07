import React, { Component } from 'react';

// create component class, cc. Double insert, enter name of comonent class
class Counter extends Component {

    // Lifecylce hook called when this component is updated
    //      - Keeps track of previous props and state
    //      - ***Order matters here!!
    componentDidUpdate(prevProps, prevState) {
        console.log("Lifecylce Hook called: Counter - componentDidUpdate()");
        console.log("- Counter - componentDidUpdate() prevState: ", prevState);
        console.log("- Counter - componentDidUpdate() prevProps: ", prevProps);

        // We can use this information to say, make another ajax call....
        if (prevProps.counter.value != this.props.counter.value) {
            console.log("Making a hypothetical ajax call here...")
        }
    }

    // Lifecylce Cycle Unmount -> Called before component is removed from the DOM
    componentWillUnmount() {
        console.log("Lifecylce Hook called: Counter - componentWillUnmount()");
    }
    
    // replace all references to state with props.counter

    // js object to handle css styling in JSX
    styles = {
        fontSize: 10, // '10px' 
        fontWeight: "bold"
    };

    // Dynamic class handling - Refactored by highlighting code block and Ctrl + Shift + R
    getBadgeClasses() {

        // this method adapts the class parameter by observing state objects

        let classes = "badge m-2 badge-";
        classes += (this.props.counter.value === 0) ? "warning" : "primary";
        return classes;
    };

    // Change output of JSX object when count is zero
    formatCount() {

        // this notation stores the value of json property count in a constant that is the name of that property!
        const { value } = this.props.counter;
        const zeroCase = "Zero"
        return value === 0 ? zeroCase : value;
    };

    renderTags() {
        // Rendering "components" using conditional statements
        if (this.props.counter.tags.length === 0) return <p>There are no tags</p>
        return <ul>{ this.props.counter.tags.map( tag => <li key={tag} >{ tag }</li> )}</ul>
    
    };


    // Rendering the component
    render() { 

        // Every component has a props property. 
        // It holds data of properties specified when the component is called
        // i.e this is one way of communicating data between components
        // state.count gets set to this.props.value.
            // - This is how data is linked externally and used internally.
        
        // how do I get the components unique ID here...?
        console.log("Counter: []", this.props)

        // JSX instead of React.createElement
        return ( 
            <div>
                <h4>Counter: {this.props.id}</h4>
                <span className={ this.getBadgeClasses() }> { this.formatCount() } </span>
                <button onClick={ () => this.props.onIncrement(this.props.counter) } className="btn btn-secondary btn-sm">Increment</button>
                
                {/* when onClick, it calls the handleDelete method stored in the props object */}
                <button onClick={ () => this.props.onDelete(this.props.counter.id) }className="btn btn-danger btn-sm m-2">Delete</button>            
            </div>
        )
    };
};

// this is required
export default Counter;