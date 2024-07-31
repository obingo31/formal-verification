/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Modifier: onlyGovernor                                                                                               │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule onlyGovernorModifier {
    method f;
    env e;
    calldataarg args;
    address nonGovernor = 0x4B20993Bc481177ec7E8f571ceCaE8A9e22C02db; // Enter the address of a non-governor account here
   
    address oldGovernor = e.contract.governor;
    address oldPendingGovernor = e.contract.pendingGovernor;

    f(e, args);

    address newGovernor = e.contract.governor;
    address newPendingGovernor = e.contract.pendingGovernor;

    // Check that the function is only callable by the governor
    assert oldGovernor == newGovernor && oldPendingGovernor == newPendingGovernor,
        "The caller of the function must be the governor";

    assert e.msg.sender == nonGovernor,
        "The function was called by a non-governor account";
}
