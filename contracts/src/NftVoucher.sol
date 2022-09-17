// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract NftVoucher is ERC721 {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    mapping(uint256 => uint256) private voucherBalance;
    ERC20 private stableToken;

    constructor(
        ERC20 token
    ) ERC721("CreditVoucher", "CV") {
        stableToken = token;
    }

    function createVoucher(address receiver, uint256 amount) external returns (uint256) {
        _tokenIds.increment();

        uint256 newItemId = _tokenIds.current();
        _mint(receiver, newItemId);

        voucherBalance[newItemId] = amount;
        require(stableToken.transferFrom(msg.sender, receiver, amount));

        return newItemId;
    }
}
