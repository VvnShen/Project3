
import streamlit as st
import pandas as pd
from apps.basics import *
from apps.commonProperties import *

eth_contract_interface = complile_contract('BackEnd/DEX_ETHowner.sol',0)
usdc_token_interface = complile_contract('BackEnd/USDC_testnet.sol',1)
usdc_contract_interface = complile_contract('BackEnd/DEX_USDCOwner.sol',0)


def settle_ETH(price, init_amount,contract_address, initailizer,x,TRN_NB):
    settler_address = st.text_input("Your wallet address: ",key=x)
    usdc_token_address=st.text_input('your USDC token address',key=x)
    usdc_token_contract = load_contract(usdc_token_interface, usdc_token_address)
    usdc_amount = int(price*init_amount*usdc_to_viv)
    st.write(f'by clicking the settle button, you are approving {price*init_amount} USDC to be transferred out, and your wallet will have {init_amount} ETH deposited (gas fee excluded).')

    if st.button("Settle",key=x):
        tx_hash = usdc_token_contract.functions.approve(contract_address, usdc_amount).transact({'from':settler_address,'gas': 1000000})
        receipt1 = w3.eth.waitForTransactionReceipt(tx_hash)
        # st.write(dict(receipt1))
        eth_contract=load_contract(eth_contract_interface,contract_address)
        tx_hash = eth_contract.functions.settleSwap(settler_address, usdc_token_address, usdc_amount).transact({'value': init_amount*eth_to_wei, 'from': initailizer, 'gas': 1000000})
        receipt2 = w3.eth.waitForTransactionReceipt(tx_hash)
        update_transaction('./Data/Trade.csv',str(TRN_NB),'Settled',usdc_token_address,settler_address)
        st.write(f"The smart contract for this transaction is {contract_address}.")
        st.write("Transaction is completed. Please kindly checkout your account.")
        # st.write(dict(receipt2))

def settle_USDC(price, init_amount,contract_address, usdc_token_address,x,TRN_NB):
    settler_address = st.text_input("Your wallet address:",key=x)
    if price != 0:
        amount = int(eth_to_wei*(init_amount/price))   # in wei
    else: amount = 0

    if st.button("Settle USDC-ETH Swap"):
        usdc_contract = load_contract(usdc_contract_interface,contract_address)
        tx_hash = usdc_contract.functions.settleSwap(init_amount*usdc_to_viv, settler_address, usdc_token_address).transact({'value': amount, 'from': settler_address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        update_transaction(trade_data,str(TRN_NB),'Settled',usdc_token_address,settler_address)
        st.write("Transaction receipt mined:")
        st.write(dict(receipt))

    


            





