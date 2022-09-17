// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;

import "forge-std/Test.sol";
import "../src/CreditLine.sol";
import "../src/MockDai.sol";
import "../src/NftVoucher.sol";

contract NftVoucherTest is Test {
    CreditLine public CreditLineInstance;
    MockDai public MockDaiInstance;
    NftVoucher public NftVoucherInstance;

    address public TestBorrower = address(0x41414141);
    address public TestLender = address(0x42424242);

    function setUp() public {
        MockDaiInstance = new MockDai();
        CreditLineInstance = new CreditLine(MockDaiInstance);
        NftVoucherInstance = new NftVoucher();

        MockDaiInstance.mint(TestLender, 100_000);
        vm.prank(TestLender);
        MockDaiInstance.approve(address(CreditLineInstance), 100_000);
    }

    function testCreate() public {
        // TODO: implement this function
        /*
            Creation will be based by calling the CreditLine voucher function
            Voucher will be received with the amount deposited set.
            Should now allow to transfer the NFT to other people ideally.
        */
    }

    function testExchange() public {
        // TODO: implement this function
        /*
            Should transfer the nft, and burn it.
            Should update the credit lines based on the amount set in the NFT.
        */
    }
}
