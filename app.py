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

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./Compiled/USDC_Owner_abi.json')) as f:
        usdc_abi = json.load(f)

    with open(Path('./Compiled/ETH_Owner_abi.json')) as f:
        eth_abi = json.load(f)


    # Set the contract address (this is the address of the deployed contract)
    usdc_contract_address = os.getenv("USDC_OWNER_CONTRACT_ADDRESS")
    eth_contract_address = os.getenv("ETH_OWNER_CONTRACT_ADDRESS")

    # Get the contract
    usdc_contract = w3.eth.contract(
        address=usdc_contract_address,
        abi=usdc_abi
    )

    eth_contract = w3.eth.contract(
        address=eth_contract_address,
        abi=eth_abi
    )

    return usdc_contract, eth_contract

# Functions for crypto exchange transactions
def transact_offer(selected_offer):

    # Determine which offer is selected
    delim_str = selected_offer.split(';')
    id = int(delim_str[-1].split(':')[-1])
    off = st.session_state.offers
    for i, row in off.iterrows():
        #x = 1
        if row.TradeID == id:
            x = i
            updated_offers = off.drop([i])
    
    # Call contract to execute transaction functions

    # Remove transacted offer from the list
    st.session_state.offers = updated_offers

def add_offer(trade_type, exchange_rate, amount, offer_address):
    # Call the contract to create a token of this offer
    if trade_type is 'Buy':   # user wants to buy ETH
        tx_hash = usdc_contract.functions.initialize(amount, 'initializer address', 'token address').transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    else:                     # user own ETH and wants to sell
        tx_hash = eth.contract.functions.initialize().transact({'from': offer_address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    id = st.session_state.offers['TradeID'].max()+1
    
    # add the offer to the display list
    st.session_state.offers = st.session_state['offers'].append({'TradeID': id, 'Trade': trade_type, 'Rate': exchange_rate, 'Amount': amount, 'address': offer_address}, ignore_index=True)


# Utility functions
def display_offers(offers):
    output = []     # output strings             
    for row in offers.itertuples():
        #output.append(row.Trade)
        str = f"{row.Trade}; Exchange Rate: {row.Rate}; Amount: {row.Amount}; ID: {row.TradeID}"
        output.append(str)
    
    return output

################################################
#
# INITIALIZATION
#
################################################

# load both contracts
usdc_contract, eth_contract = load_contract()

# initialize current offer structure
if 'offers' not in st.session_state:
    # Read existing tokens and its offers in both contracts

    st.session_state['offers'] = pd.DataFrame(data = {'TradeID': [0, 1, 2], 'Trade': ['Sell', 'Buy', 'Buy'],
            'Rate': [2500,2480,'Market'],
            'Amount': [10, 5.5, 3.7],
            'address': ['0x788B21A949250f682e260679D0B3aFf2C29b884A', 
                        '0x250D5C91Af9Df21B473E3ab0c37A6566BA863404', 
                        '0x33b80ba090487012aB049380D781b91e39481CA8']
            })

# Get accounts addresses from Ganache
accounts = w3.eth.accounts

################################################
#
# Front End Code Starts here
#
################################################


# Welcome to CryptoFlea

st.title("Welcome to Crypto Flea Market!!")


# Display list of offers currently in the system
st.markdown("### Here are offers currently in the market.")

# Display a list of offers for user to select using a selection box
#st.session_state.offers['TradeID']
offers_str = display_offers(st.session_state.offers)

selected_offer = st.selectbox(
    'Which offer do you want to accept?', options=offers_str)



#transaction_amount = st.number_input("Input transaction amount")
your_address = st.selectbox("Select Transaction Account", options=accounts)
#your_address = st.text_input("Your wallet address")

st.button("Transact", on_click=transact_offer, args=[selected_offer])
 
#Here we can invite user to make his/her own offer
st.markdown("### Please make your offer here.")
trade_type = st.selectbox('Buy or Sell?', ('Buy','Sell'))
#offer_address = st.text_input("Transaction wallet address")
offer_address = st.selectbox("Transaction Wallet Address", options=accounts)
exchange_rate = st.text_input("Your exchange rate")
amount = st.text_input("Amount to be exchanged")
st.button("Make Offer", on_click=add_offer, args=[trade_type, exchange_rate, amount, offer_address])

