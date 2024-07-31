#!/bin/bash

# Add the command certoraRun SoftBank.sol:TargetContract --verify TargetContract:NoGuardSafety.spec here
certoraRun SoftBank.sol:TargetContract --verify TargetContract:Reentrancy.spec

for FILE in contracts/* 
do 
  echo $FILE 
  contract=`echo ${FILE} | perl -0777 -pe 's/.*\///g' | awk -F'.' '{print $1}'` 
  echo $contract
  certoraRun ${FILE} \
      --verify ${contract}:certora/spec/Reentrancy.spec \
      --optimistic_loop --loop_iter 3 \
      --prover_args "-enableStorageSplitting false" \
      --msg "${contract} : Reentrancy"
  
  certoraRun ${FILE} \
      --verify ${contract}:certora/spec/Reentrancy.spec \
      --optimistic_loop --loop_iter 3 \
      --msg "${contract} : Reentrancy"

  certoraRun ${FILE} \
      --verify ${contract}:certora/spec/ReadOnlyReentrancy.spec \
      --optimistic_loop --loop_iter 3 \
      --msg "${contract} : ROReentrancy"
done
