rule permitDenialOfService(){
    env e1;
    env e2;

    address clientHolder;
    address clientSpender;
    uint256 clientAmount;
    uint256 clientDeadline;
    uint8 clientV;
    bytes32 clientR;
    bytes32 clientS;

    address attackerHolder;
    address attackerSpender;
    uint256 attackerAmount;
    uint256 attackerDeadline;
    uint8 attackerV;
    bytes32 attackerR;
    bytes32 attackerS;

    require e1.msg.sender != e2.msg.sender;

    storage init = lastStorage;

    permit(e1, clientHolder, clientSpender, clientAmount, clientDeadline, clientV, clientR, clientS); // if pass not reverted
    
    permit(e2, attackerHolder, attackerSpender, attackerAmount, attackerDeadline, attackerV, attackerR, attackerS) at init; // attacker attack

    permit(e1, clientHolder, clientSpender, clientAmount, clientDeadline, clientV, clientR, clientS);

    satisfy true;
    }