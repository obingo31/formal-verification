rule claimStakingIncentiveRule() {
    env e1;
    env e2;

    uint256 numClaimedEpochsClient;
    uint256 numClaimedEpochsAttacker;
    uint256 chainIdClient;
    uint256 chainIdAttacker;
    bytes32 stakingTargetClient;
    bytes32 stakingTargetAttacker;
    bytes  bridgePayloadClient;
    bytes bridgePayloadAttacker;

    require e1.msg.sender!= e2.msg.sender;

    storage init = lastStorage;

    // Client's attempt to claim staking incentives
    claimStakingIncentives(e1, numClaimedEpochsClient, chainIdClient, stakingTargetClient, bridgePayloadClient); // if pass not reverted
    
    // Attacker's attempt to claim staking incentives
    claimStakingIncentives(e2, numClaimedEpochsAttacker, chainIdAttacker, stakingTargetAttacker, bridgePayloadAttacker) at init; // attacker attack

    // Attempt to claim staking incentives with the same parameters as the client
    claimStakingIncentives@withrevert(e1, numClaimedEpochsClient, chainIdClient, stakingTargetClient, bridgePayloadClient);

    assert!lastReverted, "Cannot claim staking incentives with the same parameters twice";
}

