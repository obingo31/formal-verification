/*
* testing on initialization
*/

// using Initializable as initializable;
// using Lock as lock;

methods {
    // initialize, reinitialize, disable
    function initialize(address _locklist, uint128 _basePenaltyPercentage, uint128 _timePenaltyFraction, address _owner) external envfree;

     // view
    // function  _getInitializedVersion()      external returns uint8 envfree;
    // function _isInitializing() external returns bool   envfree;
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Definitions                                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
// definition isUninitialized() returns bool = _getInitializedVersion() == 0;
// definition isInitialized()   returns bool = _getInitializedVersion() > 0;
// definition isDisabled()      returns bool = _getInitializedVersion() == max_uint64;

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Invariant: A contract must only ever be in an initializing state while in the middle of a transaction execution.    │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
// invariant notInitializing()
//     !initializing();

/*

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Rule: Cannot initialize a contract that is already initialized.                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
// rule cannotInitializeTwice() {
//     require isInitialized();

//     initialize@withrevert();

//     assert lastReverted, "contract must only be initialized once";
// }






















