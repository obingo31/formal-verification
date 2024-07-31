// Show that if an adversary attempts to spoof the onBehalfOfAccount
// and call getPrize(), the call will revert
rule cannot_spoof_onBehalfOfAccount_claim() {
    env e;
    address victim; // the real onBehalfOfAccount
    address adversary; // a spoofed, nonzero onBehalfOfAccount
    require victim != adversary;
    require adversary == 0;
    uint256 amount;

    // Setup the context of a permit with onBehalfOfAccount == victim
    require e.msg.sender == currentContract;
    // require claim == victim;

    // Attempt getPrize() with a spoofed onBehalfOfAccount
    claim@withrevert(e, amount);
    assert lastReverted;

      // Attempt a call with a different nonzero onBehalfOfAccount
    // uint256 value;
    // bytes data;
    // call@withrevert(e, currentContract, adversary, value, data);
    // assert lastReverted;
}
