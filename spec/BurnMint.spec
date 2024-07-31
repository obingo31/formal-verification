// Define the ERC20 methods we want to test
methods {
    function _mint(address account, uint256 amount) external               => specMint(account, amount);
    function _burn(address account, uint256 amount) external             => specBurn(account, amount);
    function _transfer(address from, address to, uint256 amount) external => specTransfer(from, to, amount);
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Ghost: track mint, burn, and transfer amounts                                                                       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
ghost mapping(address => uint256) trackedMintAmount;
ghost mapping(address => uint256) trackedBurnAmount;
ghost mapping(address => mapping(address => uint256)) trackedTransferAmount;

// Specification functions
// function specMint(address account, uint256 amount) returns (bool) internal envfree; {
//     trackedMintAmount[account] += amount;
//     return true;
// }
/// 
function specMint(address account, uint256 amount)              returns bool { trackedMintAmount[account] = amount;        return true; }


// function specBurn(address account, uint256 amount) returns (bool) internal envfree; {
//     trackedBurnAmount[account] += amount;
//     return true;
// }
function specBurn(address account, uint256 amount)              returns bool { trackedBurnAmount[account] = amount;        return true; }

function specTransfer(address from, address to, uint256 amount) returns bool { trackedTransferedAmount[from][to] = amount; return true; }


// function specTransfer(address from, address to, uint256 amount) returns (bool) internal envfree; {
//     trackedTransferAmount[from][to] += amount;
//     return true;
// }

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Rule: Check mint and burn operations                                                                               │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule checkMintAndBurn {
    // Setup environment
    env e;

    // Define parameters for mint operation
    address account = e.newAddress();
    uint256 mintAmount = e.newUint(0, e.maxUint256());

    // Mint tokens
    e.call(address(this), "mint(address,uint256)", account, mintAmount);

    // Check the ghost variable for mint
    assert trackedMintAmount[account] == mintAmount;

    // Define parameters for burn operation
    uint256 burnAmount = e.newUint(0, mintAmount);

    // Burn tokens
    e.call(address(this), "burn(uint256)", burnAmount);

    // Check the ghost variable for burn
    assert trackedBurnAmount[e.sender()] == burnAmount;

    // Define parameters for transfer operation
    address to = e.newAddress();
    uint256 transferAmount = e.newUint(0, e.maxUint256());

    // Transfer tokens
    e.call(address(this), "transfer(address,uint256)", to, transferAmount);

    // Check the ghost variable for transfer
    assert trackedTransferAmount[e.sender()][to] == transferAmount;
}