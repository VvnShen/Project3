// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4;
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol";
import 'USDC_testnet.sol';

 //Dex_USDC_owner_trading: initializer owns USDC, and want to swap with ETH. 
contract Dex_USDC_owner_trading {
 
    address payable initializer;
    address payable settler;
    IUsdcToken public token;
    bool public transferable = true;
    mapping(address => uint) balances;

    enum State { Created, Locked, Release, Cancelled }
    State public state;

    modifier condition(bool condition_){
        require(condition_);
        _;
    }

    modifier onlyInitializer (){
        require (msg.sender==initializer, "please switch to initializer's account for initializing this swap");
        _;
    }

    modifier istransferable {
        require(transferable==true, "token under lock, can Not Trade");
         _;
    }
    modifier inState(State state_){
        require (state == state_, "State is not created");
        _;
    }

    constructor () {
        initializer = payable(msg.sender);
    }

    event Initialize();
    event SettleSwap();

    

//this contract will be initialized by whom owns USDC and wants to swap to Ether
    function initialize(uint init_amount, address _token)
        //inState(State.Created) 
        onlyInitializer external  payable {
        emit Initialize();
        token = IUsdcToken(_token);
        require (token.allowance(initializer,address(this)) >= init_amount,"please approve the token's delegation to this contract address ") ;
        token.isTransferable(false);
        state = State.Locked;

    }

//amount of Ether to swap will be calculated in FE, here just pass an amount of Ether for settlement (FE: USDC_amount=price*init_amont_in_ETH*1000000)
    function settleSwap (uint init_amount, address payable settler_,address _token)
        external       
        inState(State.Locked)
        payable  condition(init_amount != 0)   {
            emit SettleSwap();
            token = IUsdcToken(_token);
            settler=settler_;
            require (msg.sender==settler, "please switch to settler's account for settling this swap");
            require (settler.balance >= msg.value,"settler, please make sure you have enough ETH amounts to swap");
            token.isTransferable(true);
            state = State.Release;
            _safeTransferFrom(token, initializer,settler,init_amount);
            initializer.transfer(msg.value);
            // state = State.Created
        }
//this function is to withdraw the swap for initizlier before settleswap is completed. partially withdrawal is not supportive
    function withdrawSwap (address _token) external inState(State.Locked) onlyInitializer {
        token = IUsdcToken(_token);
        token.isTransferable(true);
        state = State.Cancelled;
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