# Project3
## Backend Functional Presentation
There are two types of smart contracts designed. One is for the person who initialize the contract (i.e. initializer) is owning ETH and swaping to USDC. The other is for initializers who owns USDC and wanrs to swap to ETH. This guide will present how backend works on the two contracts. 
Please get ready remix with solidity codes attached in the github, as well as Ganache and Metamask for testing.

### 1. contract Dex_ETH_owner_trading
This contract is for initializer who owns ETH and wants to swap to USDC.
1) import two accounts from Garache into Metamask Granache test network.
<img width="1196" alt="image" src="https://user-images.githubusercontent.com/88476898/152663839-759c6538-d0c6-4639-b2b5-0cbc7fb5f306.png">

2) load UsdcToken under 'Account 2' 
![image](https://user-images.githubusercontent.com/88476898/152664000-a555e360-ee74-4f14-b68e-7733bdff2a7d.png)
This is to create some fake USDC. Account 2 here is acting as settler, as it owns USDC. 

3)
