
rule targetCallRevertConditions()
{
    env e;
    method f;

    changeAdmin@withrevert(e);
    bool isReverted = lastReverted;

    assert !isReverted <=> e.msg.value == 0;
}