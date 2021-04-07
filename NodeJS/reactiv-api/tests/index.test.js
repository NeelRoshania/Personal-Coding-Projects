// Sources
//      - Jest Matchers https://jestjs.io/docs/using-matchers, https://jestjs.io/docs/expect

// Dependencies

// End point testing group
describe('Endpoint Testing', () => {

    // test positive test
    it('should pass', () => {
        
    });

    // test exceptions
    it('should fail', () => {
        expect(() => { throw new Error('Something failed...') })
    });

    // test object properties
    it('should test properties in an object', () => {
        
        const result = {id: 12345, firstName: 'Neel', lastName: 'Roshania'}; // db output
        expect(result).toMatchObject({firstName: 'Neel', lastName: 'Roshania'});
        expect(result.id).toBeGreaterThan(0);

    });

    // mock functions
    // module.function = jest.fn()
    // expect(module.function).toHaveBeenCalled(); // Determine if function called
    // expect(module.function.mock.calls[0][0]).toMatch('somePattern'); // access function arguments


});