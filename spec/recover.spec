/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Rule: recover liveness and effects                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule recover(env e) {
    require nonpayable(e);

    address receiver;
    address other;

    // sanity
    requireInvariant noSelfWrap;
    requireInvariant totalSupplyIsSumOfBalances;
    requireInvariant totalSupplyIsSmallerThanUnderlyingBalance;

    uint256 value                        = underlyingBalanceOf(currentContract) - totalSupply();
    uint256 supplyBefore                 = totalSupply();
    uint256 balanceBefore                = balanceOf(receiver);

    uint256 otherBalanceBefore           = balanceOf(other);
    uint256 otherUnderlyingBalanceBefore = underlyingBalanceOf(other);

    recover@withrevert(e, receiver);
    bool success = !lastReverted;

    // liveness
    assert success <=> receiver != 0;

    // effect
    assert success => (
        balanceOf(receiver) == balanceBefore + value &&
        totalSupply() == supplyBefore + value &&
        totalSupply() == underlyingBalanceOf(currentContract)
    );
}