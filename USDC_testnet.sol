// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4;
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol";

contract UsdcToken is ERC20 {
    address payable owner;

    modifier onlyOwner {
        require(msg.sender == owner, "You do not have permission to mint these tokens!");
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

    
}
