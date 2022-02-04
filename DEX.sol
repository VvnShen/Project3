// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4;
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/IERC20.sol";


 /** Dex_ETH_owner_trading: initializer owns ETH, and want to swap with USDC. 
    1) required fileds to be input by initializer (Gather in front end): 
    * init_symbol(owns Ether/USDC); 
    * init_amount(how many Eth/USDC want to swap with the other);
    * initializer(wallet address);
    * price (rate to convert ETH/USDC)
    2) State.Locked mechenism to lock the init_amount in contract until order confirmed by the settler, then release it to settler.
    3) this should work in python for FE: tx_hash = contract.functions.initializer().transact({'from': initializer's adreess, 'gas': 1000000})
**/

contract Dex_ETH_owner_trading {
 
    address payable initializer;
    uint init_amount;
    IERC20 public token;
    
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
    modifier OnlyOwner(){
        require (msg.sender == initializer, "ETH owner must be the initializer here");
        _;
    }


    event Initialize();
    event SettleSwap();

 
    constructor () payable {
        initializer= payable(msg.sender);
        init_amount= msg.value;

    }

//this contract will be initialized bt whom owns Ether and wants to swap to UDDC
    function initialize() 
        external 
        inState(State.Created) condition(init_amount == msg.value)
        payable {
        emit Initialize();
        initializer=payable(msg.sender);
        state = State.Locked;

    }

//once a settler (who would call Dex_USDC_owner_trading) choose to settle this swap, call below function to settle for ETH owner
//amount of USDC to swap will be calculated in FE, here just pass an amount of USDC for settlement (FE: USDC_amount=price*init_amont_in_ETH*1000000)



    function settleSwap (address payable settler,address _token, uint USDC_amount)
        external
        inState(State.Locked) OnlyOwner condition(init_amount != 0)  
        payable {
            emit SettleSwap();
            state = State.Release;
            token = IERC20(_token);
            require (token.allowance(settler,address(this)) >= USDC_amount,"please make sure settler approve the token's delegation");
            settler.transfer(init_amount);
            _safeTransferFrom(token,settler,initializer, USDC_amount);

        }

    function _safeTransferFrom(
        IERC20 _token,
        address sender,
        address recipient,
        uint amount) private {
            bool sent = _token.transferFrom(sender, recipient, amount);
            require(sent, "Token transfer failed");
    }
}
