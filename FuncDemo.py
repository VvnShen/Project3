import os
import json
import eth_account
from more_itertools import one
from pyparsing import one_of
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd



################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


#@st.cache(allow_output_mutation=True)

def load_contract(json_file_path, contract_address):

    # Load the contract ABI
    with open(Path(json_file_path)) as f:
        abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    #address = os.getenv(address_name)

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=abi
    )

    return contract

################################################
#
# INITIALIZATION
#
################################################

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Set USDC Token Address
#usdc_token_address = os.getenv("USDC_TOKEN_CONTRACT_ADDRESS")
usdc_token_address = '0xf15435d605102DaFa34879b484767df1bFea0694'
eth_contract_address = '0xf868E1873a179723442eCFb42E835C0bE1792b3B'
usdc_contract_address = '0x67E9462ba96640908Ad95A5a947e0E974AB4F224'

# load both contracts
eth_contract = load_contract('./Compiled/ETH_Owner_abi.json', eth_contract_address)
usdc_contract = load_contract('./Compiled/USDC_Owner_abi.json', usdc_contract_address)
usdc_token_contract = load_contract('./Compiled/USDC_Token_abi.json', usdc_token_address)

eth_to_wei = 1000000000000000000
total_USDC_token = 10000000000
# Approve USDC limits
#tx_hash = usdc_token_contract.functions.approve('eth_contract_address', 5000000).transact({'gas': 1000000})
#receipt = w3.eth.waitForTransactionReceipt(tx_hash)


#st.write('Allowance Approved')
# Get accounts addresses from Ganache
accounts = w3.eth.accounts

st.title('Welcome To Operation One-Way-St')
#st.write("First we initialize swap by ETH Owner in exchange of USDC")
st.write("Initialize Swapping using ETH to buy USDC")
initialize_address = st.selectbox("ETH Initializer Wallet Address", options=accounts)
st.write(f'Token Address is {usdc_token_address}, and initialize_address is {initialize_address}')
amt = int(st.number_input("Amount to be transfer (ETH)"))
if st.button("Initialize"):
    tx_hash = eth_contract.functions.initialize().transact({'value': amt*eth_to_wei, 'from': initialize_address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

st.write('Here we settle the contract')
settler_address = st.selectbox("ETH Settler Wallet Address", options=accounts)
price = st.number_input('Price of ETH in USDC')
usdc_amount = int(price*amt*1000000)
if st.button("Settle"):
    tx_hash = eth_contract.functions.settleSwap(settler_address, usdc_token_address, usdc_amount).transact({'value': amt, 'from': initialize_address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
#initialize_address = accounts[1]
#st.write(f'Token Address is {usdc_token_address}, and initialize_address is {initialize_address}')
#st.write("First we initialize swap by ETH Owner in exchange of USDC")
#if st.button("Initialize"):
#    tx_hash = eth_contract.functions.initialize().transact({'from': initialize_address, 'gas': 1000000}, 'Value': 100)
#    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#    st.write("Transaction receipt mined:")
#    st.write(dict(receipt))


# To add approval function here

#st.write("Initialize Swapping using USDC to buy ETH")
#initialize_address = st.selectbox("Transaction Wallet Address", options=accounts)
#st.write(f'Token Address is sss {usdc_token_address}, and initialize_address is {initialize_address}')
#amount = 100
#if st.button("Initialize"):
##    tx_hash = usdc_contract.functions.initialize(amount, usdc_token_address).transact({'from': initialize_address, 'gas': 1000000})
##    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#    st.write("Transaction receipt mined:")
#    st.write(dict(receipt))

#st.write("Settling the offer")
