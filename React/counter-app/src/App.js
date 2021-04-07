import React, { Component } from 'react';
import './App.css';
import NavBar from './components/navbar'
import Counters from './components/counters';


class App extends Component {
  state = { 
      // create a counters object to uniquely identify each Component
      counters: [
          { id: 1, value: 0, component_type: "Counter"},
          { id: 2, value: 0, component_type: "Counter" },
          { id: 3, value: 0, component_type: "Counter" },
          { id: 4, value: 0, component_type: "Counter" },
          { id: 5, value: 0, component_type: "Counter" }
      ]
  };


  // ** Note when each constructor is called for each lifecycle hook. Refer to documentation.

  // Lifecylce hook -> constructor
  constructor (props) {
    super(props); // important to pass to parent constructor
    console.log("Lifecylce Hook called: App - constructor()", this.props);

  }

  // Lifecylce hook -> componentDidMount();
  //    - Perfect place to make ajax calls from a server
  //    - Places the component into the DOM when called
  componentDidMount() {
    console.log("Lifecylce Hook called: App - componentDidMount()");
  }
  

  // Handling a delete event from a counter component
  handleDelete = (counter_component_id) => {

      // This method will delete a component based on it's ID
      //      - The delete button is pressed in the counter component
      //      - It calls this method and brings in the counter component id

      //  ** Updating the state
      //      - State won't be reinitialized with a new array
      //      - Instead, we're going to filter out the counter_component_id we want to delete
      //      - Notice that key and id prop is the same for Counter below and have the same value.
      //          - key property is reserved in react, and so id needs to be called again to have access to the component id

      console.log("**handleDelete -> onDelete counter id: ", counter_component_id)
      const counters = this.state.counters.filter(c => c.id !== counter_component_id)
      this.setState({ counters })
  };

  // Since Counter is no longer handling increments to counter values, this functions serves as an event handler to Counter
  //      - This method is passed as a props property to counter.
  //      - When the button in the counter component is clicked, it calls this method through props
  //      - The counter argument is passed to this method IN THE COUNTER COMPONENT
  handleIncrement = (counter) => {

      // update this component's state using a spread operating and cloning the states propery.
      // why? because updating a component's state is strictly a no go
      const counters = [...this.state.counters];
      const index = counters.indexOf(counter)
      counters[index] = {...counter};
      counters[index].value++;

      // update state -> Update Phase initiated
      this.setState({counters})

  };

  // Handling a reset event to return components to original state
  handleReset = () => {
      
      console.log("**handleReset -> onClick")

      // Reset the value property of each counter object in state
      //      - This wont work!
      const counters = this.state.counters.map( counter => {
          counter.value = 0;
          return counter;
      })

      this.setState({ counters })
  };


  // Lifecylce hook -> render();
  //    - All children rendered recursively i.e in the order with which they are presented!
  render() { 

    // Check out the console to view order of lifecycle hooks!
    console.log("Lifecylce Hook called: App - render()");

    return ( 

      // replace default with boostrap template
      <React.Fragment>
        
        {/* Filter counter components who's value is greater than 1 */}
        <NavBar 
          totalCounters = {this.state.counters.filter(c => c.value > 0).length}
        />

        {/* Counters component */}
        <main className="container">
          <Counters
            // event = handler
            counters = {this.state.counters}
            onReset = {this.handleReset}
            onIncrement = {this.handleIncrement}
            onDelete = {this.handleDelete}
          />
        </main>
      
      </React.Fragment>

     );
  };
};

export default App;
