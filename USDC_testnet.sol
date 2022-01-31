pragma solidity ^0.5.0;

import "github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";

contract UsdcToken is ERC20, ERC20Detailed {
    address payable owner;

    modifier onlyOwner {
        require(msg.sender == owner, "You do not have permission to mint these tokens!");
        _;
    }

    constructor(uint initial_supply) ERC20Detailed("USDC TEST", "USDC", 6) public {
        owner = msg.sender;
        _mint(owner, initial_supply);
    }

    function mint(address recipient, uint amount) public onlyOwner {
        _mint(recipient, amount);
    }
}
