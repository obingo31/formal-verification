/*
Solution to the challenge:
A user can request a flashloan from the pool with amount of 1000 (all the eth in the pool).
During the flashloan the user can deposit the eth taken back to the pool.
The pool will register all the eth on the user balance, however after the action is taken the pool 
only checks that it has at least the same balance as it did before (which holds since the user deposited
the eth).
The user can then freely withdraw the funds since the pool registered them on him.
*/
methods {
    function flashLoan(uint256) external;
    function _.execute() external => simulateAlternatives() expect void;
}

function simulateAlternatives() {
    // simualte different options 
    uint256 random;

    // call deposit() 
    if (random == 1) {
        env e;
        deposit(e);
    }

    // call withdraw()
    else if (random == 2) {
        env e;
        withdraw(e);
    }

    // call flashloan again
    else if (random == 3) {
        env e;
        uint256 newAmount;
        flashLoan(e,newAmount);
    }
    // do nothing 
    else  {
        
    }
}

ghost mathint sumOfBalances {
    init_state axiom sumOfBalances == 0;
}

hook Sload uint256 balance balances[KEY address addr] {
    require sumOfBalances >= to_mathint(balance);
}

hook Sstore balances[KEY address addr] uint256 newValue (uint256 oldValue) {
    sumOfBalances = sumOfBalances - oldValue + newValue;
}

invariant nativBalanceIsSumOfBalances()
    to_mathint(nativeBalances[currentContract]) >= sumOfBalances
    {
        preserved with (env e) {
            require e.msg.sender != currentContract;
        }
    }