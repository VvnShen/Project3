// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4;
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol";

//this is to make other contracts to interact with USDC contract
interface IUsdcToken {
    function isTransferable(bool _choice) external;
    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
}



contract UsdcToken is ERC20 {
    address payable owner;
    bool public transferable = false;
    mapping(address => mapping(address => uint256)) private _allowances;

    modifier onlyOwner {
        require(msg.sender == owner, "You do not have permission to mint these tokens!");
        _;
    }

    modifier istransferable {
        require(transferable==false, "token under lock, can Not Trade");
         _;
    }
    
    constructor() ERC20("USDCtest", "USDC")  {
        owner = payable(msg.sender);
        //default initial supply of the token is 10000USDC (6 decimals)
        _mint(owner, 10000000000);

    }
//ERC20 in latest version doesn't support decimals specification, default=18. USDC is 6 decimal units. So I'll overload it.
    function decimals() public view virtual override returns (uint8) {
        return 6;
    }

    function mint(address recipient, uint amount) public onlyOwner {
        _mint(recipient, amount);
    }
//overload below functions so to add lock option on USDC smart contracts 
    function transfer(address recipient, uint256 amount) public istransferable virtual override returns (bool) {
        _transfer(_msgSender(), recipient, amount);
        return true;
    }

    function transferFrom(address sender, address recipient, uint256 amount) public istransferable virtual override returns (bool) {
        uint256 currentAllowance = _allowances[sender][_msgSender()];
        if (currentAllowance != type(uint256).max) {
            require(currentAllowance >= amount, "ERC20: transfer amount exceeds allowance");
            unchecked {
                _approve(sender, _msgSender(), currentAllowance - amount);
            }
        }
        _transfer(sender, recipient, amount);
        return true;
    }

    function isTransferable(bool _choice) public {
        transferable = _choice;
    }
    
}

