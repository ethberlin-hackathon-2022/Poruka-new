// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Test.sol";
import "../src/CreditLine.sol";

contract CreditLineTest is Test {
    CreditLine public CreditLineInstance;

    address public TestBorrower = address(0x41414141);
    address public TestLender = address(0x42424242);

    function setUp() public {
        CreditLineInstance = new CreditLine();
    }

    function testCreate() public {
        Line memory line = Line(0x42, 0x42, 0);
        UserLine memory userLine = UserLine(line, TestBorrower);
        UserLine[] memory userLines = new UserLine[](1);
        userLines[0] = userLine;

        vm.prank(TestLender);
        CreditLineInstance.Create(userLines);

        assert(CreditLineInstance.GetCreditLineAmount() == 0x42);
    }

    function testBorrow() public {
        Line memory line = Line(0x42, 0x42, 0);
        UserLine memory userLine = UserLine(line, TestBorrower);
        UserLine[] memory userLines = new UserLine[](1);
        userLines[0] = userLine;

        vm.prank(TestLender);
        CreditLineInstance.Create(userLines);

        assert(CreditLineInstance.GetCreditLineAmount() == 0x42);

        vm.prank(TestLender);

        BorrowLine memory borrowUserLine = BorrowLine(0, 0x42);
        BorrowLine[] memory borrowUserLines = new BorrowLine[](1);
        borrowUserLines[0] = borrowUserLine;

        CreditLineInstance.Borrow(borrowUserLines);

        assert(CreditLineInstance.GetCreditLineAmount() == 0);
    }


    function testRepayment() public {
        Line memory line = Line(0x42, 0x42, 0);
        UserLine memory userLine = UserLine(line, TestBorrower);
        UserLine[] memory userLines = new UserLine[](1);
        userLines[0] = userLine;

        vm.prank(TestLender);
        CreditLineInstance.Create(userLines);

        assert(CreditLineInstance.GetCreditLineAmount() == 0x42);

        vm.prank(TestLender);

        BorrowLine memory borrowUserLine = BorrowLine(0, 0x42);
        BorrowLine[] memory borrowUserLines = new BorrowLine[](1);
        borrowUserLines[0] = borrowUserLine;

        CreditLineInstance.Borrow(borrowUserLines);
        assert(CreditLineInstance.GetCreditLineAmount() == 0);

        RepaymentLine memory repaymentLine = RepaymentLine(0, 0x42);
        RepaymentLine[] memory repaymentLines = new RepaymentLine[](1);
        repaymentLines[0] = repaymentLine;

        CreditLineInstance.Repayment(repaymentLines);
    }
}
