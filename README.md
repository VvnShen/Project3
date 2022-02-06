# Project3
## Backend Functional Presentation
There are two types of smart contracts designed. One is for the person who initialize the contract (i.e. initializer) is owning ETH and swaping to USDC. The other is for initializers who owns USDC and wanrs to swap to ETH. This guide will present how backend works on the two contracts. 
Please get ready remix with solidity codes attached in the github, as well as Ganache and Metamask for testing.

### Session 1. contract Dex_ETH_owner_trading
This contract is for initializer who owns ETH and wants to swap to USDC.
1) import two accounts from Garache into Metamask Granache test network.
<img width="695" alt="image" src="https://user-images.githubusercontent.com/88476898/152664149-a2962b21-6b90-45a9-8e25-e4c8dd80c49c.png">

2) load UsdcToken under 'Account 2'.
This is to create some fake USDC. Account 2 here is acting as settler, as it owns USDC. 
settler address: 0x592F1B3afFE8b1c0830e02c929a6910E5d28dd23
USDC token: 0xa2fCAC3acc7e03D5F32b81732E1862e224d21977
![image](https://user-images.githubusercontent.com/88476898/152664182-89eec825-92fd-49d7-92ff-643e8f9f2326.png)


3) switch to 'Account 3', which is the initializer's account in this case. load Dex_ETH_owner_trading contract. 
initializer address: 0x71c0Ebe729a337b079b160F456C467752BE71b4f
Dex_ETH_owner_trading contract token: 0x7B7B4DD8fB7ACbd69264973B1C97970075f8DB2B
![image](https://user-images.githubusercontent.com/88476898/152664221-682c6f41-717a-400b-bc67-944195ff9900.png)

4) initialize the swap
please put a number in Value field. This number is the Ether amount initializer want to swap to USDC, i.e. here init_amount = 10 Ether.
![image](https://user-images.githubusercontent.com/88476898/152664258-a0962d85-8a1f-4313-98cb-3c3dbb8f10dd.png)
