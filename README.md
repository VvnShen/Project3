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
Note 10 Ether is depositing into the Dex_ETH_owner_trading contract, and get locked until a settler come to settle the swap. The state=1 below means locked.
![image](https://user-images.githubusercontent.com/88476898/152664283-b5f17040-1df7-4a05-bfb2-b0aeb7804eb4.png)

5) ok time to settle the swap. 
Assume USDC amount that is going to settle = 10000000000. smallest unit for USDC is 6 decimals. So here it is 10000 USDC.
The box to be filled in settleSwap is from step 2: 
settler: 0x592F1B3afFE8b1c0830e02c929a6910E5d28dd23
_token: 0xa2fCAC3acc7e03D5F32b81732E1862e224d21977
USDC_amount=10000000000
![image](https://user-images.githubusercontent.com/88476898/152664357-46854202-288a-45f0-8e84-b2938f6f7656.png)

Before click transact, remember to give allowance of the contract to transfer USDC on behalf of the settler. Please switch back to account 2, and input approve fileds as below under USDCtoken. 
Spender: 0x7B7B4DD8fB7ACbd69264973B1C97970075f8DB2B (from step 3)
![image](https://user-images.githubusercontent.com/88476898/152664452-3729d3b2-b0e8-4f6c-8f22-d5cf7bec668b.png)
then switch back to Account 3, filled in 10 Ether in value box and click 'transact'.
![image](https://user-images.githubusercontent.com/88476898/152664520-ff2d01c8-1659-4477-9fe6-4519957b95e0.png)

6) Full transaction is completed. Let's review the account balances. 
Account 2: settler. He got Ether, amount below is expected with gas fee included.
![image](https://user-images.githubusercontent.com/88476898/152664549-ec4ece22-ec54-4ed0-9440-e39464a10a75.png)
Account 3: Initializer. After importing token, we can see 10000 USDC and Ether amounts deducted, including gas fees. 
![image](https://user-images.githubusercontent.com/88476898/152664580-1dd6107b-e823-434b-a65c-93b4ebaf5e63.png)

7) what if initializer change his mind before the settlement, that he doesn't want to swap any more?
repeat step 3 and 4 firstly, so to back to the stage of before settlement. 
click withdraw button. 
![image](https://user-images.githubusercontent.com/88476898/152664648-6a8e5ee9-160f-49f7-b684-48591658b441.png)
What it does is to return back the Eth amount deposited in the contract and change the status to canceled (State=3).
![image](https://user-images.githubusercontent.com/88476898/152664669-1184b764-f4b3-43e4-bb08-3807d10451e2.png)





