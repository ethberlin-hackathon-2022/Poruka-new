// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;

import "forge-std/Test.sol";
import "../src/CreditLine.sol";
import "../src/MockDai.sol";
import "../src/Treasury.sol";
import "../src/NftVoucher.sol";
import "forge-std/console.sol";

contract CreditLineTest is Test {
    CreditLine public CreditLineInstance;
    MockDai public MockDaiInstance;
    Treasury public TressuaryInstance;
    NftVoucher public NftVoucherInstance;

    address public TestBorrower = address(0x41414141);
    address public TestLender = address(0x42424242);
    address public TressuaryOwner = address(0x43434343);

    function setUp() public {
        MockDaiInstance = new MockDai();
        TressuaryInstance = new Treasury(TressuaryOwner);
        NftVoucherInstance = new NftVoucher(MockDaiInstance);
        CreditLineInstance = new CreditLine(MockDaiInstance, NftVoucherInstance, address(TressuaryInstance));

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
        uint256 interestBalance = CreditLineInstance.GetOutstandingAmount();

        /*
            10_000 * 10% = 1000 over one year
        */
        assert((1000 - interestBalance ) <= 1);
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

        vm.prank(TestLender);
        CreditLineInstance.Update(updateLines);

        vm.prank(TestBorrower);
        assert(CreditLineInstance.GetCreditLineAmount() == 0x82);
    }


    function testShouldNotBePossibleToUpdateAGivenCreditLineWithHigherInterestLineIfBorrowing() public {
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

        UpdateCreditLine[] memory updateLines = new UpdateCreditLine[](1);
        updateLines[0].creditIndex = 0;
        updateLines[0].amount = 0x82;
        updateLines[0].user = TestBorrower;
        updateLines[0].interestRate = 10;

        vm.prank(TestLender);
        vm.expectRevert();
        CreditLineInstance.Update(updateLines);
    }

    function testShouldBePossibleToIncreaseInterestIfNoBorrowingIsActiveOnTheCreditLine() public {
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


        UpdateCreditLine[] memory updateLines = new UpdateCreditLine[](1);
        updateLines[0].creditIndex = 0;
        updateLines[0].amount = 0x82;
        updateLines[0].user = TestBorrower;
        updateLines[0].interestRate = 10;

        vm.prank(TestLender);
        CreditLineInstance.Update(updateLines);
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

    function testShouldMintAnNftToBorrowerWhenCreditLineIsPaidBack() public {
        // TODO: implement this function
    }

    function testShouldBePossibleForLenderToWithdrawTheMoneyIfNotBeingBorrowed() public {
        // TODO: implement this function
    }

    function testShouldPutInterestIntoTressuary() public {
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
        uint256 interestBalance = CreditLineInstance.GetOutstandingAmount();

        /*
            10_000 * 10% = 1000 over one year
        */
        assert((1000 - interestBalance ) <= 1);

        RepaymentLine memory repaymentInterestLine = RepaymentLine(0, 1_000);
        RepaymentLine[] memory repaymentInterestLines = new RepaymentLine[](1);
        repaymentInterestLines[0] = repaymentInterestLine;

        vm.prank(TestBorrower);

        MockDaiInstance.increaseAllowance(address(CreditLineInstance), 100_000);
        MockDaiInstance.mint(TestBorrower, 2_000);

        vm.prank(TestBorrower);
        CreditLineInstance.Repayment(repaymentInterestLines);
        uint256 updatedInterestBalance = CreditLineInstance.GetOutstandingAmount();
        assert(updatedInterestBalance == 0);

        assert(499 <= MockDaiInstance.balanceOf(address(TressuaryInstance)));
        assert(499 <= MockDaiInstance.balanceOf(address(TestLender)));
    }

    function testShouldBePossibleToUseNftVoucherForOnBoarding() public {
        vm.prank(TestLender);
        MockDaiInstance.approve(address(NftVoucherInstance), 100_000);

        vm.prank(TestLender);
        uint256 voucherId = NftVoucherInstance.createVoucher(TestBorrower, 0x42);


        vm.prank(TestBorrower);
        CreditLineInstance.ExchangeVoucher(voucherId);

        vm.prank(TestBorrower);
        assert(CreditLineInstance.GetCreditLineAmount() == 0x42);
        assert(0x42 == MockDaiInstance.balanceOf(address(CreditLineInstance)));
    }
}
