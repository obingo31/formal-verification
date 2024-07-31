rule cannot_spoof_withdrawFTN() {
    env e;
    address victim; // the real onBehalfOfAccount
    address adversary; // a spoofed, nonzero onBehalfOfAccount
    address owner;
    uint256 amount;
    
    require victim != adversary;
    require adversary != 0;

    // Setup the context of a permit with onBehalfOfAccount == victim
    require e.msg.sender == owner;
    // require  withdrawFTN(e, amount) == victim;

    // Attempt a call with a different nonzero onBehalfOfAccount
    // uint256 amount;

    withdrawFTN@withrevert(e, amount);
    assert lastReverted;
}

rule playFrontRun() {
    env e1;
    env e2;
    
    uint256 clientPickBox;
    uint256 attackerPickBox;
    require e1.msg.sender != e2.msg.sender;
    storage init = lastStorage;

    // Client tries to get their prize
    play(e1, clientPickBox);

    // Attacker tries to front-run
    play(e2, attackerPickBox) at init; // attacker attack

    // Client tries again after the attack
    play@withrevert(e1, clientPickBox );

    assert!lastReverted, "Cannot claim prize with the same parameters twice";
}

rule winDOS() {
    env e1;
    env e2;

    address victim;
    uint256 victimBetIndex;
    
    address attacker;
    uint256 attackerBetIndex;
    
    require e1.msg.sender != e2.msg.sender;

    storage init = lastStorage;

    // Client tries to get their prize
    calculateWin(e1, victim, victimBetIndex);

    // Attacker tries to front-run
    calculateWin(e2, attacker,  attackerBetIndex) at init; // attacker attack

    // Client tries again after the attack
    calculateWin@withrevert(e1, victim, victimBetIndex);

    assert!lastReverted, "Cannot claim prize with the same parameters twice";


}


rule distributeRewardRule() {
    env e1;
    env e2;

    address player;

    address attacker;

    require e1.msg.sender!= e2.msg.sender;

    storage init = lastStorage;

  
    distributeReward(e1, player); // if pass not reverted
    
  
    distributeReward(e2, attacker) at init; // attacker attack

   
    distributeReward@withrevert(e1, attacker);

    assert!lastReverted, "Cannot claim rewards with the same parameters twice";
}

// Additional rule to enforce the attack with dust transactions
rule dustTransactionAttack() {
    env e;

    address victim;
    uint256 victimBetIndex;

    address attacker;
    uint256 attackerBetIndex;

    // Set a dust amount (small value)
    uint256 dustAmount = 1;

    // Initialize storage with the last known state
    storage init = lastStorage;

    // Attacker places a dust transaction
    // SuperFirst.bets[attacker][attackerBetIndex].amount = dustAmount;
    calculateWin(e, attacker, attackerBetIndex);

    // Client tries to get their prize
    calculateWin@withrevert(e, victim, victimBetIndex);

    // Assertion to ensure that the contract handles dust transactions properly
    assert !lastReverted, "Dust transaction caused an unexpected revert";
}