// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;

import "forge-std/Test.sol";
import "../src/CreditLine.sol";
import "../src/MockDai.sol";
import "../src/NftVoucher.sol";
import "../src/Treasury.sol";

contract NftVoucherTest is Test {
    CreditLine public CreditLineInstance;
    MockDai public MockDaiInstance;
    NftVoucher public NftVoucherInstance;
    Treasury public TressuaryInstance;

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
        MockDaiInstance.approve(address(NftVoucherInstance), 100_000);
    }

    function testCreate() public {
        vm.prank(TestLender);
        NftVoucherInstance.createVoucher(TestBorrower, 0x42);
        assert(MockDaiInstance.balanceOf(address(NftVoucherInstance)) == 0x42);

    }
}
