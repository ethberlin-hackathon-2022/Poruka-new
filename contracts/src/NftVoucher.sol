// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract NftVoucher is ERC721 {
    using Counters for Counters.Counter;
    Counters.Counter private _voucherIds;

    mapping(uint256 => uint256) private voucherBalance;
    mapping(uint256 => address) private voucherLender;

    ERC20 private stableToken;

    constructor(ERC20 _stableToken) ERC721("CreditVoucher", "CV") {
        stableToken = _stableToken;
    }

    function createVoucher(address receiver, uint256 amount)
        external
        returns (uint256)
    {
        _voucherIds.increment();

        uint256 newItemId = _voucherIds.current();
        _mint(receiver, newItemId);

        voucherBalance[newItemId] = amount;
        voucherLender[newItemId] = msg.sender;

        require(stableToken.transferFrom(msg.sender, address(this), amount));

        return newItemId;
    }

    function handIn(address cashier, uint256 voucherId)
        external
        returns (uint256)
    {
        uint256 balance = voucherBalance[voucherId];
        if (balance != 0) {
            voucherBalance[voucherId] = 0;
            require(stableToken.transfer(cashier, balance));
            _burn(voucherId);
            return 0;
        }

        return 1;
    }

    function getLender(uint256 voucherId) external view returns (address) {
        return voucherLender[voucherId];
    }

    function getVoucherAmount(uint256 voucherId)
        external
        view
        returns (uint256)
    {
        return voucherBalance[voucherId];
    }
}
