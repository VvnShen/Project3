// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4;
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol";
import 'USDC_testnet.sol';


 /** Dex_ETH_owner_trading: initializer owns ETH, and want to swap with USDC. 
    1) required fileds to be input by initializer (Gather in front end): 
    * init_symbol(owns Ether/USDC); 
    * init_amount(how many Eth/USDC want to swap with the other);
    * initializer(wallet address);
    * price (rate to convert ETH/USDC)
    2) State.Locked mechenism to lock the init_amount in contract until order confirmed by the settler, then release it to settler.
    3) this should work in python for FE: tx_hash = contract.functions.initializer().transact({'from': initializer's adreess, 'gas': 1000000})
**/

contract Dex_USDC_owner_trading {
 
    address payable initializer;
    IUsdcToken public token;
    bool public transferable = false;
     mapping(address => uint) balances;
    
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
    modifier istransferable {
        require(transferable==false, "token under lock, can Not Trade");
         _;
    }


    event Initialize();
    event SettleSwap();
    event Transfer();


//this contract will be initialized bt whom owns USDC and wants to swap to Ether
    function initialize(uint init_amount,address payable initializer_,address _token) 
        external 
        OnlyOwner 
        payable {
        emit Initialize();
        state = State.Locked;
        initializer=initializer_;
        token = IUsdcToken(_token);
        require (token.allowance(initializer,address(this)) >= init_amount,"please make sure settler approve the token's delegation");
        token.isTransferable(true);

    }


//amount of Ether to swap will be calculated in FE, here just pass an amount of Ether for settlement (FE: USDC_amount=price*init_amont_in_ETH*1000000)

    function settleSwap (uint init_amount,address payable initializer_, address payable settler,address _token, uint ETH_amount)
        external
        inState(State.Locked) OnlyOwner condition(init_amount != 0)  
        payable {
            emit SettleSwap();
            state = State.Release;
            initializer=initializer_;
            token = IUsdcToken(_token);
            require (token.allowance(settler,address(this)) >= ETH_amount,"please make sure settler approve the token's delegation");
            token.isTransferable(false);
            _safeTransferFrom(token, initializer,settler,init_amount);
            balances[initializer] += ETH_amount;
            balances[settler] -= ETH_amount;
            

        }

    function _safeTransferFrom(
        IUsdcToken _token,
        address sender,
        address recipient,
        uint amount) private {
            bool sent = _token.transferFrom(sender, recipient, amount);
            require(sent, "Token transfer failed");
    }
}
