 methods {
    // envfree functions 
    function totalSupply() external returns uint256 envfree;
    function balanceOf(address) external returns uint256 envfree;
    function allowance(address,address) external returns uint256 envfree;
    // function _owner() external returns address envfree;
}


// @title Checks that `transferFrom()`  decreases allowance of `e.msg.sender`
rule integrityOfTransferFrom(address sender, address recipient, uint256 amount) {
    env e;
    
    require sender != recipient;
    require amount != 0;


    uint256 allowanceBefore = allowance(sender, e.msg.sender);
    transferFrom(e, sender, recipient, amount);
    uint256 allowanceAfter = allowance(sender, e.msg.sender);
    
    assert (
        allowanceBefore > allowanceAfter
        ),
        "allowance must decrease after using the allowance to pay on behalf of somebody else";
}