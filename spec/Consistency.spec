

using Proxy as proxy;

methods {
    function upgradeTo(address) external;
    function upgradeToAndCall(address, bytes calldata) external returns (bytes memory);
    function changeAdmin(address) external;
    function admin() external returns (address);
    function implementation() external returns (address);
    function _getAdmin() internal returns (address);
    function _getImplementation() internal returns (address);
}

// Rule to check admin access control
rule adminAccessControl(method f) {
    env e;
    calldataarg args;
    address sender = e.msg.sender;
    address currentAdmin = proxy._getAdmin();
    
    require sender != currentAdmin && sender != 0;
    
    f@withrevert(e, args);
    
    assert lastReverted, 
        "Non-admin addresses should not be able to call admin functions";
}

// Rule to check implementation address integrity
rule implementationAddressIntegrity(method f) {
    env e;
    calldataarg args;
    address before = proxy._getImplementation();
    
    f(e, args);
    
    address after = proxy._getImplementation();
    
    assert after != 0, "Implementation address should never be zero";
    assert before != after => e.msg.sender == proxy._getAdmin(),
        "Only admin should be able to change implementation";
}

// Rule to check proxy functionality
rule proxyFunctionality(method f) {
    env e;
    calldataarg args;
    address sender = e.msg.sender;
    address currentAdmin = proxy._getAdmin();
    
    require sender != currentAdmin && sender != 0;
    
    // This part is simplified as we can't directly check delegation in CVL2
    // In a real test, you'd need to set up a mock implementation contract
    f@withrevert(e, args);
    
    assert !lastReverted, 
        "Non-admin calls should be forwarded to implementation";
}

// Rule to check storage slot consistency
rule storageSlotConsistency() {
    env e;
    
    // Check IMPLEMENTATION_KEY
    address impl = proxy._getImplementation();
    assert impl == proxy.implementation(), 
        "IMPLEMENTATION_KEY storage inconsistency";
    
    // Check OWNER_KEY
    address admin = proxy._getAdmin();
    assert admin == proxy.admin(), 
        "OWNER_KEY storage inconsistency";
}

// Rule to check upgrade atomicity
rule upgradeAtomicity() {
    env e;
    address newImpl;
    bytes  data;
    
    proxy.upgradeToAndCall@withrevert(e, newImpl, data);
    
    bool reverted = lastReverted;
    address currentImpl = proxy._getImplementation();
    
    assert !reverted => currentImpl == newImpl, 
        "Upgrade should be atomic: new implementation set on success";
    assert reverted => currentImpl != newImpl, 
        "Upgrade should be atomic: old implementation retained on failure";
}

// Rule to check event emission
rule eventEmission(method f) {
    env e;
    calldataarg args;
    
    if (f.selector == sig:upgradeTo(address).selector ||
        f.selector == sig:upgradeToAndCall(address,bytes).selector) {
        address oldImpl = proxy._getImplementation();
        f(e, args);
        address newImpl = proxy._getImplementation();
        
        assert oldImpl != newImpl => 
            e.emitted(Upgraded(newImpl)),
            "Upgraded event must be emitted when implementation changes";
    }
    
    if (f.selector == sig:changeAdmin(address).selector) {
        address oldAdmin = proxy._getAdmin();
        f(e, args);
        address newAdmin = proxy._getAdmin();
        
        assert oldAdmin != newAdmin => 
            e.emitted(AdminChanged(oldAdmin, newAdmin)),
            "AdminChanged event must be emitted when admin changes";
    }
}

// Invariant to ensure admin and implementation are never zero
invariant adminAndImplNeverZero()
    proxy._getAdmin() != 0 && proxy._getImplementation() != 0;