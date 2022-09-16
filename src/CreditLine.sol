// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract CreditLine {
    mapping(address => Line[]) public UserCreditLines;

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
            UserCreditLines[line.user].push(line.creditLine);
        }
    }

    function Borrow(BorrowLine[] memory lines) external {
        uint256 sumAmount = 0;
        for (uint256 i = 0; i < lines.length; i++) {
            BorrowLine memory line = lines[i];
            Line memory userLine = UserCreditLines[msg.sender][
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
            UserCreditLines[msg.sender][line.creditIndex].balance += line
                .amount;
            sumAmount += line.amount;
        }
        require(stableToken.transferFrom(msg.sender, address(this), sumAmount));
    }

    function GetCreditLineAmount() external view returns (uint256) {
        uint256 amount = 0;
        for (uint256 i = 0; i < UserCreditLines[msg.sender].length; i++) {
            amount = UserCreditLines[msg.sender][i].balance;
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
