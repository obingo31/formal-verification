/*
* Test access control
*/


rule AdminConsistencyAsRule( env e, method f) {
    // Precondition
    require _getAdmin(e) == admin(e);

   
    calldataarg args;
    f(e, args);

    // Postcondition
    assert _getAdmin(e) == admin(e),
        "Admin should be equal to admin";
}













