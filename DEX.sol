// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4;
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol";
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/IERC20.sol";

contract UsdcToken is ERC20 {
    address payable owner;

    modifier onlyOwner {
        require(msg.sender == owner, "You do not have permission to mint these tokens!");
        _;
    }
    
    constructor(address payable settler) ERC20("USDCtest", "USDC") public {
        owner = payable(settler);
        _mint(owner, 100);
    }
//ERC20 in latest version doesn't support decimals specification, default=18. USDC is 6 decimal units. So I'll overload it.
        function decimals() public view virtual override returns (uint8) {
        return 6;
    }

    function mint(address recipient, uint amount) public onlyOwner {
        _mint(recipient, amount);
    }
}

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

    constructor (address payable settler) payable  public{
        initializer = payable(msg.sender);
        init_amount=msg.value;
        token = new UsdcToken(settler);
    }

//initializer who owns ETH, input the ETH value as the amount to swap USDC
    function initialize() 
        external 
        inState(State.Created) condition(msg.value != 0)
        payable {
        emit Initialize();
        initializer=payable(msg.sender);
        state = State.Locked;

    }

    function check_address () view public returns(address) {
        return address(this);
    }

//once a settler (who would call Dex_USDC_owner_trading) choose to settle this swap, call below function to settle for ETH owner
//amount of USDC to swap will be calculated in FE, here just pass an amount of USDC for settlement (FE: USDC_amount=price*init_amont_in_ETH)
    function settleSwap (address payable settler, uint USDC_amount)
        external
        inState(State.Locked) OnlyOwner condition(msg.value==init_amount)
        payable {
            emit SettleSwap();
            state = State.Release;
            uint256 allowance = token.allowance(settler, address(this));
            require(allowance >= USDC_amount, "Check the token allowance");
            settler.transfer(msg.value);
            token.transferFrom(settler,initializer, USDC_amount);

        }

}