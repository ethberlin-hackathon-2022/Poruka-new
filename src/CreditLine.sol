// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract CreditLine {
    mapping(address => Line[]) public UserCreditLines;

    function Create(UserLine[] memory lines) public {}

    function Borrow(BorrowLine[] memory lines) public {}

    function Repayment(RepaymentLine[] memory lines) public {}

    function GetCreditLineAmount() public view returns (uint256) {
        uint256 amount = 0;
        for (uint256 i = 0; i < UserCreditLines[msg.sender].length; i++) {
            amount = UserCreditLines[msg.sender][i].amount;
        }
        return amount;
    }
}

struct Line {
    uint256 amount;
    uint256 balance;
    uint256 interest;
}

struct UserLine {
    Line creditLine;
    address user;
}

struct BorrowLine {
    uint256 creditIndex;
    uint256 amount;
}

struct RepaymentLine {
    uint256 creditIndex;
    uint256 amount;
}
