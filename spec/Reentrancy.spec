persistent ghost bool called_extcall;
persistent ghost bool g_reverted;
persistent ghost uint32 g_sighash;

// Hook on "CALL" opcodes to simulate reentrancy and check for reverts
hook CALL(uint g, address addr, uint value, uint argsOffset, uint argsLength, uint retOffset, uint retLength) uint rc {
  called_extcall = true;
  env e;
  bool cond;


  // Adjusted to include the new function signature
    if (g_sighash == sig:claim().selector) {
        claim@withrevert(e); // name of the function that is being called
        g_reverted = lastReverted;
    }
    else {
        g_reverted =true; // if the function is not withdraw, then we revert
    }
}

// Rule filtering for non-view functions
rule no_reentrancy(method f, method g) filtered { f->f.isView, g ->g.isView } {
  require!called_extcall;
  require!g_reverted;
  env e;
  calldataarg args;

  require g_sighash == g.selector;
  f@withrevert(e, args);

  assert called_extcall => g_reverted, "Reentrancy weakness exists";
}