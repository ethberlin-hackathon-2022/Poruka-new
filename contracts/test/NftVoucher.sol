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
        CreditLineInstance = new CreditLine(MockDaiInstance, address(TressuaryInstance));
        NftVoucherInstance = new NftVoucher(MockDaiInstance);

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

    function testHandIn() public {
        // TODO: implement this function
        /*
            Should transfer the nft, and burn it.
            Should update the credit lines based on the amount set in the NFT.
            Should transfer the deposited amount from the ERC721, to the CreditLine contract.
        */
    }
}
