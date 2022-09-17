// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;

import "forge-std/Test.sol";
import "../src/CreditLine.sol";
import "../src/MockDai.sol";
import "forge-std/console.sol";

contract CreditLineTest is Test {
    CreditLine public CreditLineInstance;
    MockDai public MockDaiInstance;

    address public TestBorrower = address(0x41414141);
    address public TestLender = address(0x42424242);

    function setUp() public {
        MockDaiInstance = new MockDai();
        CreditLineInstance = new CreditLine(MockDaiInstance);

        MockDaiInstance.mint(TestLender, 100_000);
        vm.prank(TestLender);
        MockDaiInstance.approve(address(CreditLineInstance), 100_000);
    }

    function testCreate() public {
        Line memory line = Line({
            amount: 0x42,
            interestRate: 0
        });
        UserLine memory userLine = UserLine(line, TestBorrower);
        UserLine[] memory userLines = new UserLine[](1);
        userLines[0] = userLine;

        vm.prank(TestLender);
        CreditLineInstance.Create(userLines);
        assert(MockDaiInstance.balanceOf(address(CreditLineInstance)) == 0x42);

        vm.prank(TestBorrower);
        assert(CreditLineInstance.GetCreditLineAmount() == 0x42);
    }

    function testBorrow() public {
        Line memory line = Line({
            amount: 0x42,
            interestRate: 0
        });
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

        assert(MockDaiInstance.balanceOf(address(CreditLineInstance)) == 0x0);
        assert(MockDaiInstance.balanceOf(address(TestBorrower)) == 0x42);

        vm.prank(TestBorrower);
        assert(CreditLineInstance.GetCreditLineAmount() == 0);
    }

    function testExpectRevertIfMoreMoneyIsRequestedThanOnTheLine() public {
        Line memory line = Line({
            amount: 0x42,
            interestRate: 0
        });
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
        Line memory line = Line({
            amount: 0x42,
            interestRate: 0
        });
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

        RepaymentLine memory repaymentLine = RepaymentLine(0, 0x42);
        RepaymentLine[] memory repaymentLines = new RepaymentLine[](1);
        repaymentLines[0] = repaymentLine;

        vm.prank(TestBorrower);
        MockDaiInstance.increaseAllowance(address(CreditLineInstance), 0x42);

        vm.prank(TestBorrower);
        CreditLineInstance.Repayment(repaymentLines);

        vm.prank(TestBorrower);
        assert(CreditLineInstance.GetCreditLineAmount() == 0x42);

        assert(MockDaiInstance.balanceOf(address(CreditLineInstance)) == 0x42);
        assert(MockDaiInstance.balanceOf(address(TestBorrower)) == 0x0);
    }

    function testRepaymentWithInterest() public {
        // 2022-01-01 22:00:00 GMT+0100
        vm.warp(1641070800);
        Line memory line = Line({
            amount: 10_000,
            // percentage interest rate
            interestRate: 10
        });

        UserLine memory userLine = UserLine(line, TestBorrower);
        UserLine[] memory userLines = new UserLine[](1);
        userLines[0] = userLine;

        vm.prank(TestLender);
        CreditLineInstance.Create(userLines);

        vm.prank(TestBorrower);
        assert(CreditLineInstance.GetCreditLineAmount() == 10_000);

        BorrowLine memory borrowUserLine = BorrowLine(0, 10_000);
        BorrowLine[] memory borrowUserLines = new BorrowLine[](1);
        borrowUserLines[0] = borrowUserLine;

        vm.prank(TestBorrower);
        CreditLineInstance.Borrow(borrowUserLines);
        vm.prank(TestBorrower);
        assert(CreditLineInstance.GetCreditLineAmount() == 0);

        RepaymentLine memory repaymentLine = RepaymentLine(0, 10_000);
        RepaymentLine[] memory repaymentLines = new RepaymentLine[](1);
        repaymentLines[0] = repaymentLine;

        vm.prank(TestBorrower);
        MockDaiInstance.increaseAllowance(address(CreditLineInstance), 10_000);

        vm.prank(TestBorrower);
        // 2023-01-01 22:00:00 GMT+0100
        vm.warp(1672603200);
        CreditLineInstance.Repayment(repaymentLines);

        vm.prank(TestBorrower);
        assert(CreditLineInstance.GetCreditLineAmount() == 10_000);

        assert(MockDaiInstance.balanceOf(address(CreditLineInstance)) == 10_000);
        assert(MockDaiInstance.balanceOf(address(TestBorrower)) == 0x0);

        vm.prank(TestBorrower);
        uint256 feeBalance = CreditLineInstance.GetOutstandingAmount();

        /*
            10_000 * 10% = 1000 over one year
        */
        assert((1000 - feeBalance ) <= 1);
    }

    function testShouldBePossibleToUpdateAGivenCreditLineWithHigherAmount() public {
        Line memory line = Line({
            amount: 0x42,
            interestRate: 0
        });
        UserLine memory userLine = UserLine(line, TestBorrower);
        UserLine[] memory userLines = new UserLine[](1);
        userLines[0] = userLine;

        vm.prank(TestLender);
        CreditLineInstance.Create(userLines);

        vm.prank(TestBorrower);
        assert(CreditLineInstance.GetCreditLineAmount() == 0x42);

        UpdateCreditLine[] memory updateLines = new UpdateCreditLine[](1);
        updateLines[0].creditIndex = 0;
        updateLines[0].amount = 0x82;
        updateLines[0].user = TestBorrower;

        vm.prank(TestBorrower);
        console.log(CreditLineInstance.GetCreditLineAmount());

        vm.prank(TestLender);
        CreditLineInstance.Update(updateLines);

        vm.prank(TestBorrower);
        console.log(CreditLineInstance.GetCreditLineAmount());
        vm.prank(TestBorrower);
        assert(CreditLineInstance.GetCreditLineAmount() == 0x82);
    }

    function testShouldBePossibleToUpdateAGivenCreditLineWithLowerAmountIfNotAmountIsNotBorrowed() public {
        // TODO: implement this function
    }

    function testShouldNotBePossibleToRepayMoreThanCreditAmount() public {
        // TODO: implement this function
    }

    function testShouldCorrectlyUpdateTheOutstandingAmountOnRepayment() public {
        // TODO: implement this function
    }

    function testShouldPutInterestIntoTressuary() public {
        // TODO: implement this function
    }

    function testShouldBePossibleToUseNftVoucherForOnBoarding() public {
        // TODO: implement this function
    }
}
