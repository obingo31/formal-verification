methods {
    function owner() external  returns (address) envfree;
    function transferOwnership(address)  external returns address;
    function renounceOwnership()  external returns address;
}
