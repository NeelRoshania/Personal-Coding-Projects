// Tree component
//     - One "Counters" can have many "Counter"

import React, { Component } from 'react';
import Counter from './counter';
// import Test from './test';

class Counters extends Component {

    render() { 

        // every React components contains 'props', a JS Object that includes all attributes of private objects
        if (this.props.value === undefined) console.log("**Underfined properties for Counters");
        
        // props object destructuring, compare to above -> now remove this.props
        const { onReset, counters, onDelete, onIncrement } = this.props;

        // this should return three more componenets to the UI
        return ( 
            <div>

                <button 
                onClick={onReset}
                className="btn btn-primary sm"
                >Reset</button>
            

                {/* key is a reserved component property in react */}
                {/* This can be observed on the react developer tools */}
                
                {/* **If a new counter property is specified in the counters state, we would have to update it manually here 
                        - More effecient to just pass in the counter object directly. It contains all the date we need for each counter
                        - Since the counter object is being passed as a property into Counter, it needs to be adjusted in the Counter component
                */}

                
                { counters.map(counter => 
                    <Counter 
                    key={ counter.id } 
                    onDelete={onDelete} 
                    onIncrement={onIncrement}
                    counter={ counter } // THIS IS THE REFERECNCE TO THE Counter COMPONENT ID FROM THIS STATE
                    />
                    )
                }
            </div>
        )
    }
}
 
export default Counters;