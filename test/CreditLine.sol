// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;

import "forge-std/Test.sol";
import "../src/CreditLine.sol";
import "../src/MockDai.sol";

contract CreditLineTest is Test {
    CreditLine public CreditLineInstance;
    MockDai public MockDaiInstance;

    address public TestBorrower = address(0x41414141);
    address public TestLender = address(0x42424242);

    function setUp() public {
        MockDaiInstance = new MockDai();
        CreditLineInstance = new CreditLine(MockDaiInstance);

        MockDaiInstance.mint(TestLender, 0x256);
        vm.prank(TestLender);
        MockDaiInstance.approve(address(CreditLineInstance), 0x100);
    }

    function testCreate() public {
        Line memory line = Line(0x42, 0x42, 0);
        UserLine memory userLine = UserLine(line, TestBorrower);
        UserLine[] memory userLines = new UserLine[](1);
        userLines[0] = userLine;

        vm.prank(TestLender);
        CreditLineInstance.Create(userLines);

        vm.prank(TestBorrower);
        assert(CreditLineInstance.GetCreditLineAmount() == 0x42);
    }

    function testBorrow() public {
        Line memory line = Line(0x42, 0x42, 0);
        UserLine memory userLine = UserLine(line, TestBorrower);
        UserLine[] memory userLines = new UserLine[](1);
        userLines[0] = userLine;

        vm.prank(TestLender);
        CreditLineInstance.Create(userLines);

        vm.prank(TestBorrower);
        assert(CreditLineInstance.GetCreditLineAmount() == 0x42);

        BorrowLine memory borrowUserLine = BorrowLine(0, 0x42);
        BorrowLine[] memory borrowUserLines = new BorrowLine[](1);
        borrowUserLines[0] = borrowUserLine;

        vm.prank(TestBorrower);
        CreditLineInstance.Borrow(borrowUserLines);

        vm.prank(TestBorrower);
        assert(CreditLineInstance.GetCreditLineAmount() == 0);
    }

    function testExpectRevertIfMoreMoneyIsRequestedThanOnTheLine() public {
        Line memory line = Line(0x42, 0x42, 0);
        UserLine memory userLine = UserLine(line, TestBorrower);
        UserLine[] memory userLines = new UserLine[](1);
        userLines[0] = userLine;

        vm.prank(TestLender);
        CreditLineInstance.Create(userLines);

        vm.prank(TestBorrower);
        assert(CreditLineInstance.GetCreditLineAmount() == 0x42);

        BorrowLine memory borrowUserLine = BorrowLine(0, 0x50);
        BorrowLine[] memory borrowUserLines = new BorrowLine[](1);
        borrowUserLines[0] = borrowUserLine;

        vm.prank(TestBorrower);
        vm.expectRevert();
        CreditLineInstance.Borrow(borrowUserLines);
    }

    function testRepayment() public {
        Line memory line = Line(0x42, 0x42, 0);
        UserLine memory userLine = UserLine(line, TestBorrower);
        UserLine[] memory userLines = new UserLine[](1);
        userLines[0] = userLine;

        vm.prank(TestLender);
        CreditLineInstance.Create(userLines);

        vm.prank(TestBorrower);
        assert(CreditLineInstance.GetCreditLineAmount() == 0x42);

        vm.prank(TestLender);

        BorrowLine memory borrowUserLine = BorrowLine(0, 0x42);
        BorrowLine[] memory borrowUserLines = new BorrowLine[](1);
        borrowUserLines[0] = borrowUserLine;

        CreditLineInstance.Borrow(borrowUserLines);

        vm.prank(TestBorrower);
        assert(CreditLineInstance.GetCreditLineAmount() == 0);

        RepaymentLine memory repaymentLine = RepaymentLine(0, 0x42);
        RepaymentLine[] memory repaymentLines = new RepaymentLine[](1);
        repaymentLines[0] = repaymentLine;

        CreditLineInstance.Repayment(repaymentLines);
    }
}
