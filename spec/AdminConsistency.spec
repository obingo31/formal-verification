methods {
    function upgradeTo(address) external;
    function upgradeToAndCall(address, bytes) external;
    function changeAdmin(address) external;
    function admin() external returns (address) envfree;
    function implementation() external returns (address) envfree;
    
    function _getAdmin() internal returns (address);
    function _getImplementation() internal returns (address);
}

rule adminFunctionsRevertForNonAdmin(method f) {
    require f.selector == sig:upgradeTo(address).selector ||
            f.selector == sig:upgradeToAndCall(address,bytes).selector ||
            f.selector == sig:changeAdmin(address).selector;
    
    env e;
    require e.msg.sender != admin(e) && e.msg.sender != 0;
    calldataarg arg;
    f@withrevert(e, arg);
    
    assert lastReverted, "Admin function did not revert for non-admin caller";
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ REVERTS: in implementation contract                                                                                              │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/

rule proxyCallReversionPropagation() {
    env e;
    require getImplementation() != 0;
    require e.msg.sender != admin() && e.msg.sender != 0;

    method f;
    calldataarg args;
    f@withrevert(e, args);

    assert lastReverted <=> wasDispatched(getImplementation(), f.selector) && lastDispatched.reverted,
        "Proxy call reversion should be propagated correctly";
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ This rule ensures that admin functions do not revert when called by the admin.                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/

rule adminFunctionsDoNotRevertForAdmin(method f) {
    require f.selector == sig:upgradeTo(address).selector ||
            f.selector == sig:upgradeToAndCall(address,bytes).selector ||
            f.selector == sig:changeAdmin(address).selector;
    
    env e;
    require e.msg.sender == _getAdmin();
    calldataarg arg;
    f@withrevert(e, arg);
    
    assert !lastReverted, "Admin function reverted for admin caller";
}

