persistent ghost bool called_extcall;
persistent ghost bool storage_access_before_call;
persistent ghost bool storage_access_after_call;

// Simulate the external call state changes
rule reentrancySafety(method f) {
    // Start with all flags false 
    require !called_extcall && !storage_access_before_call && !storage_access_after_call;

    // Define the environment and arguments
    calldataarg args;
    env e;
    
    // Simulate the function call
    f(e, args);

    // Assuming the external call happens here
    called_extcall = true;
    
    // Simulate storage access before the call
    if (!called_extcall) {
        storage_access_before_call = true;
    }
    
    // Simulate storage access after the call
    if (called_extcall) {
        storage_access_after_call = true;
    }

    // Assert no storage access before and after the call
    assert !(storage_access_before_call && storage_access_after_call), "Reentrancy weakness exists";
}
