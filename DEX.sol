// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4;
// Due to the more advanced solodity version used here, I can't import safemath as it's not supportive in higher version. So I'm pasting the library here directly.
library SafeMath {
    function tryAdd(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        uint256 c = a + b;
        if (c < a) return (false, 0);
        return (true, c);
    }
    function trySub(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        if (b > a) return (false, 0);
        return (true, a - b);
    }
    function tryMul(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        if (a == 0) return (true, 0);
        uint256 c = a * b;
        if (c / a != b) return (false, 0);
        return (true, c);
    }
    function tryDiv(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        if (b == 0) return (false, 0);
        return (true, a / b);
    }
    function tryMod(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        if (b == 0) return (false, 0);
        return (true, a % b);
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");
        return c;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a, "SafeMath: subtraction overflow");
        return a - b;
    }
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) return 0;
        uint256 c = a * b;
        require(c / a == b, "SafeMath: multiplication overflow");
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b > 0, "SafeMath: division by zero");
        return a / b;
    }
    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b > 0, "SafeMath: modulo by zero");
        return a % b;
    }
    function sub(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
        require(b <= a, errorMessage);
        return a - b;
    }
    function div(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
        require(b > 0, errorMessage);
        return a / b;
    }
    function mod(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
        require(b > 0, errorMessage);
        return a % b;
    }
}

 /** Dex_ETH_owner_trading: initializer owns ETH, and want to swap with USDC. 
    1) required fileds to be input by initializer (Gather in front end): 
    * init_symbol(owns Ether/USDC); 
    * init_amount(how many Eth/USDC want to swap with the other);
    * initializer(wallet address);
    * price (rate to convert ETH/USDC)
    2) State.Locked mechenism to lock the init_amount in contract until order confirmed by the settler, then release it to settler.
    3) initializer is the same as person to create the contract. This seems to be the only way to lock the amount.
**/

contract Dex_ETH_owner_trading {
 
    address payable initializer;
    uint init_amount;
    
    //controlling the flowing of funds
    enum State { Created, Locked, Release, Inactive }
    State public state;

    modifier condition(bool condition_){
        require(condition_);
        _;
    }

    modifier inState(State state_){
        require (state == state_, "invalid state");
        _;
    }
    event Initialize();

    constructor () payable{
        initializer = payable(msg.sender);
        init_amount=msg.value;
    }


    function initialize() 
        external 
        inState(State.Created) condition(msg.value==init_amount)
        payable {
        emit Initialize();
        initializer=payable(msg.sender);
        state = State.Locked;

    }



}