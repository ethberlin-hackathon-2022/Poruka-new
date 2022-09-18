// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/utils/math/Math.sol";
import "forge-std/console.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./NftVoucher.sol";

contract CreditLine {
    mapping(address => ActiveCreditLine[]) public UserCreditLines;

    ERC20 private stableToken;
    NftVoucher private nftVouchers;

    address private tressuary;

    constructor(
        ERC20 _stableToken,
        NftVoucher _nftVoucher,
        address _tressuary
    ) {
        stableToken = _stableToken;
        nftVouchers = _nftVoucher;
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
        
        string memory zeroAllowanceMessage = "Zero allowance to ";
        string memory addressStr = Strings.toHexString((address(this)));

        require(0 < stableToken.balanceOf(msg.sender), string.concat("Zero balance ", Strings.toHexString(uint160(address(msg.sender)), 20), " of ", Strings.toHexString(uint160(address(stableToken)), 20)));
        require(0 < stableToken.allowance(msg.sender, address(this)), string.concat(zeroAllowanceMessage, addressStr));
        require(stableToken.transferFrom(msg.sender, address(this), sumAmount), "Failed transfer");
    }

    function Borrow(BorrowLine[] calldata lines) external {
        uint256 sumAmount = 0;
        for (uint256 i = 0; i < lines.length; i++) {
            BorrowLine memory line = lines[i];
            ActiveCreditLine storage userLine = UserCreditLines[msg.sender][
                line.creditIndex
            ];
            require(line.amount <= userLine.balance);
            userLine.balance -= line.amount;

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
            ActiveCreditLine storage creditLine = UserCreditLines[msg.sender][
                line.creditIndex
            ];
            uint256 lineBalance = line.amount;
            uint256 deltaLine = Math.min(
                line.amount,
                creditLine.amount - creditLine.balance
            );
            creditLine.balance += deltaLine;
            lineBalance -= deltaLine;

            if (creditLine.interestRate != 0) {
                uint256 secondsInAyear = 3600 * 24 * 365;
                // TODO: In theory we should store all borrows and lendings and calculate the accumualted interest intependent.
                //       However that would be gas costly, so we doing it this way for now.
                uint256 power = 10**16;
                uint256 deltaTime = block.timestamp -
                    creditLine.lastInterestCaluclation;
                uint256 interestRate = creditLine.interestRate;
                uint256 interestPerYear = (interestRate * power) /
                    secondsInAyear;
                uint256 accumulatedInterest = ((outstandingBalance *
                    (interestPerYear) *
                    deltaTime) / (power * 10**2));

                creditLine.accumulatedInterest += accumulatedInterest;
            }

            if (creditLine.balance == creditLine.amount && lineBalance > 0) {
                uint256 interestPaid = Math.min(
                    lineBalance,
                    creditLine.accumulatedInterest
                );
                creditLine.accumulatedInterest -= interestPaid;
                uint256 halfInterestPaid = (interestPaid * 1) / 2;

                tressuaryAmount += halfInterestPaid;
                lenderAmount[i] = LenderInterestRepayment({
                    lender: creditLine.lender,
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
            ActiveCreditLine storage userCreditLines = UserCreditLines[
                line.user
            ][line.creditIndex];
            uint256 currentLineAmount = userCreditLines.amount;
            uint256 currentLineBalance = userCreditLines.balance;

            require(
                line.interestRate == 0 ||
                    (line.interestRate != 0 &&
                        currentLineBalance == currentLineAmount)
            );

            userCreditLines.amount = line.amount;
            userCreditLines.balance += (line.amount - currentLineBalance);
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

    function ExchangeVoucher(uint256 voucherId) external {
        address lender = nftVouchers.getLender(voucherId);
        uint256 amount = nftVouchers.getVoucherAmount(voucherId);
        ActiveCreditLine memory activeLine = ActiveCreditLine({
            lender: lender,
            amount: amount,
            balance: amount,
            interestRate: 0,
            accumulatedInterest: 0,
            lastInterestCaluclation: block.timestamp
        });
        UserCreditLines[msg.sender].push(activeLine);

        require(nftVouchers.handIn(address(this), voucherId) == 0);
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
