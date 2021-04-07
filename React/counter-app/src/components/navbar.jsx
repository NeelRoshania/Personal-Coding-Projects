import React from 'react'; // Component no longer needed in this case

// Using stateless functional componets to handle componets instead of a class
//      - 'this' is no longer available as we have swapped class instates to stateless functional components

// Lifecylce hooks cannot be used here!
//      - This is a function, not a React Class Component

const NavBar = ({totalCounters}) => {
    return ( 

        <nav className="navbar navbar-light bg-light">
            <a className="navbar-brand">
                Navbar 
                <span className="badge badge-pill badge-secondary">
                    {totalCounters}
                </span>
            </a>
        </nav>

        );
};
 
export default NavBar; 