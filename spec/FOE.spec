import "./helpers.spec";
import "./IOwnable.spec";

methods {
    function balanceOf(address)                                                external returns (uint256);
    function transferFrom(address, address, uint256)                           external returns(uint256);
    function deposit(address, address, uint256)                                external returns(uint256);
    function withdraw(address, uint256, uint256, bool)                         external returns(uint256);
    function owner()                                                           external returns address envfree;
    function primaryAsset()                                                    external returns address envfree;
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Rule: Check for Fee-On-Transfer discrepancies in deposit function                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule depositFeeOnTransfer(env e, address from, address to, uint256 amount) {
    require nonpayable(e);

    address primaryToken = primaryAsset(e);

    // Get the balance before deposit
    uint256 balanceBefore = balanceOf(primaryToken);

    // Call the deposit function
    deposit(e, from, to, amount);

    // Get the balance after deposit
    uint256 balanceAfter = balanceOf(primaryToken);

    // Calculate the actual amount transferred
    mathint actualAmount = balanceAfter - balanceBefore;

    // Assert that the actual amount transferred is equal to or less than the amount specified
    // This accounts for possible Fee-On-Transfer or deflationary behavior
    assert actualAmount <= amount, "Fee-On-Transfer or deflationary discrepancy in deposit";
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Rule: Check for Fee-On-Transfer discrepancies in withdraw function                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule withdrawFeeOnTransfer(env e, address to, uint256 amount, uint256 id, bool isInternal) {
    require nonpayable(e);

    address primaryToken = primaryAsset(e);

    // Only the owner can call withdraw
    require e.msg.sender == owner(e);

    // Get the balance before withdraw
    uint256 balanceBefore = balanceOf(primaryToken);

    // Call the withdraw function
    withdraw(e, to, amount, id, isInternal);

    // Get the balance after withdraw
    uint256 balanceAfter = balanceOf(primaryToken);

    // Calculate the actual amount transferred
    mathint actualAmount = balanceBefore - balanceAfter;

    // Assert that the actual amount transferred is equal to or more than the amount specified
    // This accounts for possible Fee-On-Transfer or deflationary behavior
    assert actualAmount >= amount, "Fee-On-Transfer or deflationary discrepancy in withdraw";
}
