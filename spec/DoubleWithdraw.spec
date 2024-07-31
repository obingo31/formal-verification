rule noDoubleDutch(address account) {
    uint256 amount = balanceOf(account);
    env e;
    require e.msg.sender == account;
    withdrawFTN(e, amount);
    uint256 x;
    withdrawFTN@withrevert(e, x);
    assert lastReverted;
}