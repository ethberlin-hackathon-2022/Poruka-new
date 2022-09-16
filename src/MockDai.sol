// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MockDai is ERC20 {
    constructor() ERC20("MockDai", "MDai") {}

    function mint(address user, uint256 amount) external {
        _mint(user, amount);
    }
}
