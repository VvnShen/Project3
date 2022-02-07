// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4;
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/IERC20.sol";
import 'USDC_testnet.sol';


 //Dex_ETH_owner_trading: initializer owns ETH, and want to swap with USDC. 
contract Dex_ETH_owner_trading {
 
    address payable initializer;
    uint init_amount;
    IUsdcToken public token;
    
    //controlling the flowing of funds
    enum State { Created, Locked, Release, Cancelled }
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
        //inState(State.Created) 
        condition(msg.value !=0)
        payable {
        emit Initialize();
        initializer=payable(msg.sender);
        state = State.Locked;

    }

//once a settler (who would call Dex_USDC_owner_trading) choose to settle this swap, call below function to settle for ETH owner
//amount of USDC to swap will be calculated in FE, here just pass an amount of USDC for settlement (FE: USDC_amount=price*init_amont_in_ETH*1000000)



    function settleSwap (address payable settler,address payable _token, uint USDC_amount)
        external
        inState(State.Locked) OnlyOwner condition(msg.value != 0)  
        payable {
            emit SettleSwap();
            state = State.Release;
            token = IUsdcToken(_token);
            settler.transfer(msg.value);
            initializer.transfer(msg.value);
            _safeTransferFrom(token,settler,initializer, USDC_amount);
        }
//this function is to withdraw the swap for initizlier before settleswap is completed. partially withdrawal is not supportive
    function withdrawSwap () external payable inState(State.Locked) OnlyOwner {
        initializer.transfer(msg.value);
        state = State.Cancelled;
    }

    function _safeTransferFrom(
        IUsdcToken _token,
        address sender,
        address recipient,
        uint amount) private  {
            bool sent = _token.transferFrom(sender, recipient, amount);
            require(sent, "Token transfer failed");
    }


  
}
