// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TargetContract {
    mapping(address => uint256) public balances;

    // Update the `balances` mapping to include the new ETH deposited by msg.sender
    function addBalance() external payable {
        balances[msg.sender] += msg.value;
    }

    // Send ETH worth `balances[msg.sender]` back to msg.sender
    function withdraw() external {
        // Ensure the sender has a balance to withdraw
        require(balances[msg.sender] != 0);
        // Attempt to transfer
        (bool sent, ) = msg.sender.call{value: balances[msg.sender]}("");// This is the vulnerable line
        require(sent, "Failed to send Ether");
        // Update the balance to reflect the transfer after being drained
        balances[msg.sender] = 0; 
    }

    function withdrawAll() external {
        uint256 amount = balances[msg.sender];
        balances[msg.sender] = 0;
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed.");
    }

    
}
