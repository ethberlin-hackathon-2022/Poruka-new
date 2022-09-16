// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "forge-std/console.sol";

contract CreditLine {
    mapping(address => ActiveCreditLine[]) public UserCreditLines;

    ERC20 private stableToken;

    constructor(ERC20 token) {
        stableToken = token;
    }

    function Create(UserLine[] memory lines) external {
        for (uint256 i = 0; i < lines.length; i++) {
            UserLine memory line = lines[i];
            require(
                stableToken.transferFrom(
                    msg.sender,
                    address(this),
                    line.creditLine.amount
                )
            );
            ActiveCreditLine memory activeLine = ActiveCreditLine({
                amount: line.creditLine.amount,
                balance: line.creditLine.amount,
                interestRate: line.creditLine.interestRate,
                accumulatedInterest: 0,
                lastInterestCaluclation: block.timestamp
            });
            UserCreditLines[line.user].push(activeLine);
        }
    }

    function Borrow(BorrowLine[] memory lines) external {
        uint256 sumAmount = 0;
        for (uint256 i = 0; i < lines.length; i++) {
            BorrowLine memory line = lines[i];
            ActiveCreditLine memory userLine = UserCreditLines[msg.sender][
                line.creditIndex
            ];
            require(line.amount <= userLine.balance);
            UserCreditLines[msg.sender][line.creditIndex].balance -= line
                .amount;

            sumAmount += line.amount;
        }
        require(stableToken.transfer(msg.sender, sumAmount));
    }

    function Repayment(RepaymentLine[] memory lines) external {
        uint256 sumAmount = 0;
        for (uint256 i = 0; i < lines.length; i++) {
            RepaymentLine memory line = lines[i];
            uint256 outstandingBalance = UserCreditLines[msg.sender][
                line.creditIndex
            ].amount - UserCreditLines[msg.sender][line.creditIndex].balance;
            ActiveCreditLine memory creditLine = UserCreditLines[msg.sender][
                line.creditIndex
            ];
            UserCreditLines[msg.sender][line.creditIndex].balance += line
                .amount;

            if (creditLine.interestRate != 0) {
                uint256 secondsInAyear = 3600 * 24 * 365;
                // TODO: In theory we should store all borrows and lendings and calculate the accumualted interest intependent.
                //       However that would be gas costly, so we doing it this way for now.
                uint256 power = 10**16;
                uint256 deltaTime = block.timestamp -
                    UserCreditLines[msg.sender][line.creditIndex]
                        .lastInterestCaluclation;
                uint256 interestRate = UserCreditLines[msg.sender][
                    line.creditIndex
                ].interestRate;
                uint256 interestPerYear = (interestRate * power) /
                    secondsInAyear;
                uint256 accumulatedInterest = ((outstandingBalance *
                    (interestPerYear) *
                    deltaTime) / (power * 10**2));

                UserCreditLines[msg.sender][line.creditIndex]
                    .accumulatedInterest += accumulatedInterest;
            }

            sumAmount += line.amount;
        }
        require(stableToken.transferFrom(msg.sender, address(this), sumAmount));
    }

    function UpdateCreditLine() public {
        // TODO: should be possible to update a credit line
        //       but should not be possible to edit the interst rate if there is an active borrow.
    }

    function GetCreditLineAmount() external view returns (uint256) {
        uint256 amount = 0;
        for (uint256 i = 0; i < UserCreditLines[msg.sender].length; i++) {
            amount = UserCreditLines[msg.sender][i].balance;
        }
        return amount;
    }

    function GetOutstandingAmount() external view returns (uint256) {
        uint256 amount = 0;
        for (uint256 i = 0; i < UserCreditLines[msg.sender].length; i++) {
            uint256 borrowed = UserCreditLines[msg.sender][i].amount -
                UserCreditLines[msg.sender][i].balance;
            uint256 fee = UserCreditLines[msg.sender][i].accumulatedInterest;
            amount = borrowed + fee;
        }
        return amount;
    }
}

struct Line {
    uint256 amount;
    uint256 interestRate;
}

struct ActiveCreditLine {
    uint256 amount;
    uint256 balance;
    uint256 accumulatedInterest;
    uint256 interestRate;
    uint256 lastInterestCaluclation;
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
