// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/access/AccessControl.sol";

contract Treasury is AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

    constructor(address ADMIN) {
        _setupRole(ADMIN_ROLE, ADMIN);
    }

    function withdraw(uint256 amount) public payable {
        require(hasRole(ADMIN_ROLE, msg.sender), "Caller is not a ADMIN");
        address payable receiver = payable(msg.sender);
        receiver.transfer(amount);
    }
}
