// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/utils/math/Math.sol";
import "forge-std/console.sol";

contract CreditLine {
    mapping(address => ActiveCreditLine[]) public UserCreditLines;

    ERC20 private stableToken;

    address private tressuary;

    constructor(ERC20 token, address _tressuary) {
        stableToken = token;
        tressuary = _tressuary;
    }

    function Create(UserLine[] calldata lines) external {
        uint256 sumAmount = 0;
        for (uint256 i = 0; i < lines.length; i++) {
            UserLine memory line = lines[i];

            sumAmount += line.creditLine.amount;

            ActiveCreditLine memory activeLine = ActiveCreditLine({
                lender: msg.sender,
                amount: line.creditLine.amount,
                balance: line.creditLine.amount,
                interestRate: line.creditLine.interestRate,
                accumulatedInterest: 0,
                lastInterestCaluclation: block.timestamp
            });
            UserCreditLines[line.user].push(activeLine);
        }

        require(stableToken.transferFrom(msg.sender, address(this), sumAmount));
    }

    function Borrow(BorrowLine[] calldata lines) external {
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

    function Repayment(RepaymentLine[] calldata lines) external {
        uint256 sumAmount = 0;
        uint256 tressuaryAmount = 0;
        LenderInterestRepayment[]
            memory lenderAmount = new LenderInterestRepayment[](lines.length);

        for (uint256 i = 0; i < lines.length; i++) {
            RepaymentLine memory line = lines[i];
            uint256 outstandingBalance = UserCreditLines[msg.sender][
                line.creditIndex
            ].amount - UserCreditLines[msg.sender][line.creditIndex].balance;
            ActiveCreditLine memory creditLine = UserCreditLines[msg.sender][
                line.creditIndex
            ];
            uint256 lineBalance = line.amount;
            uint256 deltaLine = Math.min(
                line.amount,
                UserCreditLines[msg.sender][line.creditIndex].amount -
                    UserCreditLines[msg.sender][line.creditIndex].balance
            );
            UserCreditLines[msg.sender][line.creditIndex].balance += deltaLine;
            lineBalance -= deltaLine;

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

            if (
                UserCreditLines[msg.sender][line.creditIndex].balance ==
                UserCreditLines[msg.sender][line.creditIndex].amount &&
                lineBalance > 0
            ) {
                uint256 interestPaid = Math.min(
                    lineBalance,
                    UserCreditLines[msg.sender][line.creditIndex]
                        .accumulatedInterest
                );
                UserCreditLines[msg.sender][line.creditIndex]
                    .accumulatedInterest -= interestPaid;
                uint256 halfInterestPaid = (interestPaid * 1) / 2;
                tressuaryAmount += halfInterestPaid;
                lenderAmount[i] = LenderInterestRepayment({
                    lender: UserCreditLines[msg.sender][line.creditIndex]
                        .lender,
                    amount: halfInterestPaid
                });
                lineBalance -= interestPaid;
            }

            sumAmount += line.amount;
        }
        require(stableToken.transferFrom(msg.sender, address(this), sumAmount));

        if (tressuaryAmount > 0) {
            require(
                stableToken.transferFrom(msg.sender, tressuary, tressuaryAmount)
            );
        }

        for (uint256 i = 0; i < lenderAmount.length; i++) {
            if (lenderAmount[i].amount != 0) {
                require(
                    stableToken.transferFrom(
                        msg.sender,
                        lenderAmount[i].lender,
                        lenderAmount[i].amount
                    )
                );
            }
        }
    }

    function Update(UpdateCreditLine[] memory lines) external {
        // TODO: should be possible to update a credit line
        //       but should not be possible to edit the interst rate if there is an active borrow.
        for (uint256 i = 0; i < lines.length; i++) {
            UpdateCreditLine memory line = lines[i];

            uint256 currentLineAmount = UserCreditLines[line.user][
                line.creditIndex
            ].amount;
            uint256 currentLineBalance = UserCreditLines[line.user][
                line.creditIndex
            ].balance;

            require(
                line.interestRate == 0 ||
                    (line.interestRate != 0 &&
                        currentLineBalance == currentLineAmount)
            );

            UserCreditLines[line.user][line.creditIndex].amount = line.amount;
            UserCreditLines[line.user][line.creditIndex].balance += (line
                .amount - currentLineBalance);
        }
    }

    function GetUsercreditLineAmount(address user)
        external
        view
        returns (uint256)
    {
        uint256 amount = 0;
        for (uint256 i = 0; i < UserCreditLines[user].length; i++) {
            amount = UserCreditLines[user][i].balance;
        }
        return amount;
    }

    function GetCreditLineAmount() external view returns (uint256) {
        return this.GetUsercreditLineAmount(msg.sender);
    }

    function GetUserOutstandingAmount(address user)
        external
        view
        returns (uint256)
    {
        /**
            TODO:
                The outstadning amount should do an interest calculation on the fly.
                This way we can show the actual outstanding amount on the frontend, and 
                allow a user to repay it all at once, or just the principal.
        */
        uint256 amount = 0;
        for (uint256 i = 0; i < UserCreditLines[user].length; i++) {
            uint256 borrowed = UserCreditLines[user][i].amount -
                UserCreditLines[user][i].balance;
            uint256 fee = UserCreditLines[user][i].accumulatedInterest;
            amount = borrowed + fee;
        }
        return amount;
    }

    function GetOutstandingAmount() external view returns (uint256) {
        return this.GetUserOutstandingAmount(msg.sender);
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
    address lender;
}

struct UserLine {
    Line creditLine;
    address user;
}

struct UpdateCreditLine {
    address user;
    uint256 creditIndex;
    uint256 amount;
    uint256 interestRate;
}

struct BorrowLine {
    uint256 creditIndex;
    uint256 amount;
}

struct RepaymentLine {
    uint256 creditIndex;
    uint256 amount;
}

struct LenderInterestRepayment {
    uint256 amount;
    address lender;
}
