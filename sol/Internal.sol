// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {MerkleMultiProof} from "./MerkleMultiProof.sol";
import {Client} from "./Client.sol";

// Library for CCIP internal definitions common to multiple contracts.
library Internal {
  error InvalidEVMAddress(bytes encodedAddress);

  /// @dev The minimum amount of gas to perform the call with exact gas.
  /// We include this in the offramp so that we can redeploy to adjust it
  /// should a hardfork change the gas costs of relevant opcodes in callWithExactGas.
  uint16 internal constant GAS_FOR_CALL_EXACT_CHECK = 5_000;
  // @dev We limit return data to a selector plus 4 words. This is to avoid
  // malicious contracts from returning large amounts of data and causing
  // repeated out-of-gas scenarios.
  uint16 internal constant MAX_RET_BYTES = 4 + 4 * 32;

  /// @notice A collection of token price and gas price updates.
  /// @dev RMN depends on this struct, if changing, please notify the RMN maintainers.
  struct PriceUpdates {
    TokenPriceUpdate[] tokenPriceUpdates;
    GasPriceUpdate[] gasPriceUpdates;
  }

  /// @notice Token price in USD.
  /// @dev RMN depends on this struct, if changing, please notify the RMN maintainers.
  struct TokenPriceUpdate {
    address sourceToken; // Source token
    uint224 usdPerToken; // 1e18 USD per 1e18 of the smallest token denomination.
  }

  /// @notice Gas price for a given chain in USD, its value may contain tightly packed fields.
  /// @dev RMN depends on this struct, if changing, please notify the RMN maintainers.
  struct GasPriceUpdate {
    uint64 destChainSelector; // Destination chain selector
    uint224 usdPerUnitGas; // 1e18 USD per smallest unit (e.g. wei) of destination chain gas
  }

  /// @notice A timestamped uint224 value that can contain several tightly packed fields.
  struct TimestampedPackedUint224 {
    uint224 value; // ───────╮ Value in uint224, packed.
    uint32 timestamp; // ────╯ Timestamp of the most recent price update.
  }

  /// @dev Gas price is stored in 112-bit unsigned int. uint224 can pack 2 prices.
  /// When packing L1 and L2 gas prices, L1 gas price is left-shifted to the higher-order bits.
  /// Using uint8 type, which cannot be higher than other bit shift operands, to avoid shift operand type warning.
  uint8 public constant GAS_PRICE_BITS = 112;

  struct PoolUpdate {
    address token; // The IERC20 token address
    address pool; // The token pool address
  }

  struct SourceTokenData {
    // The source pool address, abi encoded. This value is trusted as it was obtained through the onRamp. It can be
    // relied upon by the destination pool to validate the source pool.
    bytes sourcePoolAddress;
    // The address of the destination token pool, abi encoded in the case of EVM chains
    // This value is UNTRUSTED as any pool owner can return whatever value they want.
    bytes destTokenAddress;
    // Optional pool data to be transferred to the destination chain. Be default this is capped at
    // CCIP_LOCK_OR_BURN_V1_RET_BYTES bytes. If more data is required, the TokenTransferFeeConfig.destBytesOverhead
    // has to be set for the specific token.
    bytes extraData;
  }

  /// @notice Report that is submitted by the execution DON at the execution phase. (including chain selector data)
  /// @dev RMN depends on this struct, if changing, please notify the RMN maintainers.
  struct ExecutionReportSingleChain {
    uint64 sourceChainSelector; // Source chain selector for which the report is submitted
    EVM2EVMMessage[] messages;
    // Contains a bytes array for each message, each inner bytes array contains bytes per transferred token
    bytes[][] offchainTokenData;
    bytes32[] proofs;
    uint256 proofFlagBits;
  }

  /// @notice Report that is submitted by the execution DON at the execution phase.
  /// @dev RMN depends on this struct, if changing, please notify the RMN maintainers.
  struct ExecutionReport {
    EVM2EVMMessage[] messages;
    // Contains a bytes array for each message, each inner bytes array contains bytes per transferred token
    bytes[][] offchainTokenData;
    bytes32[] proofs;
    uint256 proofFlagBits;
  }

  /// @notice The cross chain message that gets committed to EVM chains.
  /// @dev RMN depends on this struct, if changing, please notify the RMN maintainers.
  struct EVM2EVMMessage {
    uint64 sourceChainSelector; // ───────────╮ the chain selector of the source chain, note: not chainId
    address sender; // ───────────────────────╯ sender address on the source chain
    address receiver; // ─────────────────────╮ receiver address on the destination chain
    uint64 sequenceNumber; // ────────────────╯ sequence number, not unique across lanes
    uint256 gasLimit; //                        user supplied maximum gas amount available for dest chain execution
    bool strict; // ──────────────────────────╮ DEPRECATED
    uint64 nonce; //                          │ nonce for this lane for this sender, not unique across senders/lanes
    address feeToken; // ─────────────────────╯ fee token
    uint256 feeTokenAmount; //                  fee token amount
    bytes data; //                              arbitrary data payload supplied by the message sender
    Client.EVMTokenAmount[] tokenAmounts; //    array of tokens and amounts to transfer
    bytes[] sourceTokenData; //                 array of token data, one per token
    bytes32 messageId; //                       a hash of the message data
  }

  /// @dev EVM2EVMMessage struct has 13 fields, including 3 variable arrays.
  /// Each variable array takes 1 more slot to store its length.
  /// When abi encoded, excluding array contents,
  /// EVM2EVMMessage takes up a fixed number of 16 lots, 32 bytes each.
  /// For structs that contain arrays, 1 more slot is added to the front, reaching a total of 17.
  uint256 public constant MESSAGE_FIXED_BYTES = 32 * 17;

  /// @dev Each token transfer adds 1 EVMTokenAmount and 1 bytes.
  /// When abiEncoded, each EVMTokenAmount takes 2 slots, each bytes takes 2 slots, excl bytes contents
  uint256 public constant MESSAGE_FIXED_BYTES_PER_TOKEN = 32 * 4;

  function _toAny2EVMMessage(
    EVM2EVMMessage memory original,
    Client.EVMTokenAmount[] memory destTokenAmounts
  ) internal pure returns (Client.Any2EVMMessage memory message) {
    return Client.Any2EVMMessage({
      messageId: original.messageId,
      sourceChainSelector: original.sourceChainSelector,
      sender: abi.encode(original.sender),
      data: original.data,
      destTokenAmounts: destTokenAmounts
    });
  }

  bytes32 internal constant EVM_2_EVM_MESSAGE_HASH = keccak256("EVM2EVMMessageHashV2");

  function _hash(EVM2EVMMessage memory original, bytes32 metadataHash) internal pure returns (bytes32) {
    // Fixed-size message fields are included in nested hash to reduce stack pressure.
    // This hashing scheme is also used by RMN. If changing it, please notify the RMN maintainers.
    return keccak256(
      abi.encode(
        MerkleMultiProof.LEAF_DOMAIN_SEPARATOR,
        metadataHash,
        keccak256(
          abi.encode(
            original.sender,
            original.receiver,
            original.sequenceNumber,
            original.gasLimit,
            original.strict,
            original.nonce,
            original.feeToken,
            original.feeTokenAmount
          )
        ),
        keccak256(original.data),
        keccak256(abi.encode(original.tokenAmounts)),
        keccak256(abi.encode(original.sourceTokenData))
      )
    );
  }

  /// @notice This methods provides validation for parsing abi encoded addresses by ensuring the
  /// address is within the EVM address space. If it isn't it will revert with an InvalidEVMAddress error, which
  /// we can catch and handle more gracefully than a revert from abi.decode.
  /// @return The address if it is valid, the function will revert otherwise.
  function _validateEVMAddress(bytes memory encodedAddress) internal pure returns (address) {
    if (encodedAddress.length != 32) revert InvalidEVMAddress(encodedAddress);
    return _validateEVMAddressFromUint256(abi.decode(encodedAddress, (uint256)));
  }

  /// @dev We disallow the first 1024 addresses to never allow calling precompiles. It is extremely unlikely that
  /// anyone would ever be able to generate an address in this range.
  uint256 public constant PRECOMPILE_SPACE = 1024;

  /// @notice This method provides a safe way to convert a uint256 to an address.
  /// It will revert if the uint256 is not a valid EVM address, or a precompile address.
  /// @return The address if it is valid, the function will revert otherwise.
  function _validateEVMAddressFromUint256(uint256 encodedAddress) internal pure returns (address) {
    if (encodedAddress > type(uint160).max || encodedAddress < PRECOMPILE_SPACE) {
      revert InvalidEVMAddress(abi.encode(encodedAddress));
    }
    return address(uint160(encodedAddress));
  }

  /// @notice Enum listing the possible message execution states within
  /// the offRamp contract.
  /// UNTOUCHED never executed
  /// IN_PROGRESS currently being executed, used a replay protection
  /// SUCCESS successfully executed. End state
  /// FAILURE unsuccessfully executed, manual execution is now enabled.
  /// @dev RMN depends on this enum, if changing, please notify the RMN maintainers.
  enum MessageExecutionState {
    UNTOUCHED,
    IN_PROGRESS,
    SUCCESS,
    FAILURE
  }

  /// @notice CCIP OCR plugin type, used to separate execution & commit transmissions and configs
  enum OCRPluginType {
    Commit,
    Execution
  }
}