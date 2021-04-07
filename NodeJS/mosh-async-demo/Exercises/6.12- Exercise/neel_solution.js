//
// Required functions
//
  
function getCustomer(id) {
    return new Promise ( (resolve, reject) => {
        
        // simulate api request 4s
        setTimeout( () => {

            const api_result = { id: 1, name: 'Mosh Hamedani', isGold: true, email: 'email' };
            console.log(api_result);
            resolve(api_result);

        }, 4000);

    })
}

function getTopMovies(customer_id) {
    return new Promise ( (resolve, reject) => {
        
        // simulate api request 4s
        setTimeout( () => {
            const api_result = ['movie1', 'movie2'];
            console.log(api_result);
            resolve(api_result);
        }, 4000);

    })
}

function sendEmail(email, movies) {
    return new Promise ( (resolve, reject) => {

        // simulate 4s api request
        setTimeout( () => {
            const api_result = 'Email sent...';
            onsole.log(api_result);
            resolve(api_result);
        }, 4000);

    })
}

async function display_output(customer_id, email, movies) {

    try {
        
        // get customer
        const customer      = await getCustomer(customer_id);
        
        // condition when customer isGold
        if (customer.isGold) {

            const top_movies    = await getTopMovies(customer_id);
            const email_status  = sendEmail(email, top_movies);
        }
        
    } catch (error) {
        
        console.log(new Error('Some async error'));
        console.log(err);

    }

}

//
// MAIN
//

const customer_id = 1;
display_output(customer_id);

