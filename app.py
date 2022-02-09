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

# Functions for crypto exchange transactions
def transact_offer(selected_offer, settler_address, usdc_token_address):

    # Determine which offer is selected
    delim_str = selected_offer.split(';')
    id = int(delim_str[-1].split(':')[-1])
    off = st.session_state.offers
    for i, row in off.iterrows():
        # Check if the Trade ID match the id given
        if row.TradeID == id:
            trade_type = row['Trade']
            price = int(row['Rate'])
            amount = int(row['Amount'])
            initialize_address = row['address']
            updated_offers = off.drop([i])
            
    
    # Call contract to execute transaction functions
    if trade_type is 'Buy':   # Selected offer is to buy ETH with USDC
        usdc_amount = amount
        eth_amount = int(eth_to_wei*(usdc_amount/price))
        #st.write(f'Initializer Address = {initialize_address}')
        #st.write(f'Settler Address = {settler_address}')
        tx_hash = usdc_contract.functions.settleSwap(usdc_amount*usdc_to_viv, settler_address, usdc_token_address).transact({'value': eth_amount, 'from': settler_address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        #st.write("Transaction receipt mined:")
        #st.write(dict(receipt))
    else:
        
        # load usdc token contract
        usdc_token_contract = load_contract('./Compiled/USDC_Token_abi.json', usdc_token_address)
        eth_amount = amount
        usdc_amount = int(price*eth_amount*usdc_to_viv)
        # First approve the amount to be transacted
        tx_hash = usdc_token_contract.functions.approve(eth_contract_address, usdc_amount).transact({'from':settler_address,'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        #st.write(dict(receipt))


        tx_hash = eth_contract.functions.settleSwap(settler_address, usdc_token_address, usdc_amount).transact({'value': eth_amount, 'from': initialize_address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        #st.write("Transaction receipt mined:")
        #st.write(dict(receipt))


    # Remove transacted offer from the list
    st.session_state.offers = updated_offers

def add_offer(trade_type, exchange_rate, amount, offer_address, usdc_token_address=None):
    # Call the contract to create a token of this offer
    if trade_type is 'Buy':   # user wants to buy ETH
        usdc_token_contract = load_contract('./Compiled/USDC_Token_abi.json', usdc_token_address)
        usdc_amount = amount

        # First approve the transcation from the token contract
        tx_hash = usdc_token_contract.functions.approve(usdc_contract_address, usdc_amount*usdc_to_viv).transact({'from':offer_address,'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.success(f'During initialization, {usdc_amount}USDC Token is locked from your wallet.')
        #st.write(dict(receipt))


        # Initialize the offer
        tx_hash = usdc_contract.functions.initialize(usdc_amount*usdc_to_viv, usdc_token_address).transact({'from': offer_address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        #st.write("Transaction receipt mined:")
        #st.write(dict(receipt))

    else:                     # user own ETH and wants to sell
        initialize_amount = amount*eth_to_wei
        tx_hash = eth_contract.functions.initialize().transact({'value': initialize_amount, 'from': offer_address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        #st.write("Transaction receipt mined:")
        #st.write(dict(receipt))

    if st.session_state.offers.empty:
        id = 0
    else:
        id = st.session_state.offers['TradeID'].max()+1

    # add the offer to the display list
    st.session_state.offers = st.session_state['offers'].append({'TradeID': id, 'Trade': trade_type, 'Rate': exchange_rate, 'Amount': amount, 'address': offer_address}, ignore_index=True)

    #if trade_type is 'Buy':
    #     st.session_state.approval_receipt = usdc_amount

# Utility functions
def display_offers(offers):
    if offers.empty:
        output = ['No offers in the market yet!']
    else:
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

# Set Contract Address
eth_contract_address = '0xc953Db9D4801E1aC97eD9b395c85F84606Da1019'
usdc_contract_address = '0xB2A46d57669E44496e9c6c6FDD3eE6c4ad6aFE1c'
#usdc_token_address = '0x7be2101967324E87A142D6D2672c3ce1A2ff720C'

# load both contracts
eth_contract = load_contract('./Compiled/ETH_Owner_abi.json', eth_contract_address)
usdc_contract = load_contract('./Compiled/USDC_Owner_abi.json', usdc_contract_address)
#usdc_token_contract = load_contract('./Compiled/USDC_Token_abi.json', usdc_token_address)

# Some hard facts
eth_to_wei = 1000000000000000000
usdc_to_viv = 1000000



# initialize current offer structure
if 'offers' not in st.session_state :
    # Read existing tokens and its offers in both contracts
    st.session_state['offers'] = pd.DataFrame(columns=['TradeID','Trade','Rate','Amount','address'])



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

####################################################################
# Display a list of offers for user to select using a selection box
#
offers_str = display_offers(st.session_state.offers)
selected_offer = st.selectbox(
    'Which offer do you want to accept?', options=offers_str)

if st.session_state.offers.empty == False:
    # Ask user for the transaction address
    your_address = st.selectbox("Select Transaction Account", options=accounts)
    usdc_token_address=st.text_input("Settler USDC Token address")
    # A button to make transaction of selected offer
    st.button("Transact", on_click=transact_offer, args=[selected_offer, your_address, usdc_token_address])

# Here we code our withdrawn button

###################################################  
#Here we can invite user to make his/her own offer
st.markdown("### Please make your offer here.")
trade_type = st.selectbox('Buy or Sell?', ('Buy','Sell'))

offer_address = st.selectbox("Transaction Wallet Address", options=accounts)
if trade_type == 'Buy':
    usdc_token_address = st.text_input("Initializer USDC Token address")
exchange_rate = st.text_input("Your limit price in USDC/ETH")
if trade_type == 'Buy':
    amount = int(st.number_input("Amount to be exchanged (USDC)"))
    st.button("Make Offer", on_click=add_offer, args=[trade_type, exchange_rate, amount, offer_address, usdc_token_address])
else:
    amount = int(st.number_input("Amount to be exchanged (ETH)"))
    st.button("Make Offer", on_click=add_offer, args=[trade_type, exchange_rate, amount, offer_address]) #, usdc_token_address])


