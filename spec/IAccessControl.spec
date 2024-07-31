methods {
    function hasAdminRole(address)       external returns(bool) envfree;
    function getRoleAdmin(bytes32)           external returns(bytes32) envfree;
    function grantRole(bytes32, address)     external returns address envfree;
    function revokeRole(bytes32, address)    external returns address envfree;
    function renounceRole(bytes32, address)  external returns address envfree;
}
