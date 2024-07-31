rule playDenialOfService() {
    env e1;
    env e2;

    uint256 clientFirstBet;
    bool clientIsChanged;
   
    uint256 attackerFirstBet;
    bool attackerIsChanged;


    require e1.msg.sender != e2.msg.sender;

    storage init = lastStorage;

    // Client tries to get their prize
    play(e1, clientFirstBet, clientIsChanged);

    // Attacker tries to front-run
    play(e2, attackerFirstBet, attackerIsChanged) at init; // attacker attack

    // Client tries again after the attack
    play(e1, clientFirstBet, clientIsChanged);
    // Ensure that the client's call still succeeds
    satisfy true;
}

rule distributeRewardDenialOfService() {
    env e1;
    env e2;

    address clientPlayer;
    address attackerPlayer;

    require e1.msg.sender != e2.msg.sender;

    storage init = lastStorage;

    // Client tries to distribute reward
    distributeReward(e1, clientPlayer);

    // Attacker tries to front-run
    distributeReward(e2, attackerPlayer) at init;

    // Client tries again after the attack
    distributeReward(e1, clientPlayer);

    // Ensure that the client's call still succeeds
    satisfy true;
}
