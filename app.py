import os
import json
from more_itertools import one
from pyparsing import one_of
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd

load_dotenv()

# Define and connect a new Web3 provider

#w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


#@st.cache(allow_output_mutation=True)
#def load_contract():

    # Load the contract ABI
#    with open(Path('./artwork_abi.json')) as f:
#        artwork_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
#    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
#    contract = w3.eth.contract(
#        address=contract_address,
#        abi=artwork_abi
#    )

#    return contract

def display_offers(offers):
    output = []     # output strings             
    for row in offers.itertuples():
        #output.append(row.Trade)
        str = f"{row.Trade}; Exchange Rate: {row.Rate}; ID: {row.TradeID}"
        output.append(str)
    
    return output


# initialize current offer structure
if 'offers' not in st.session_state:
    st.session_state['offers'] = pd.DataFrame(data = {'TradeID': [0, 1, 2], 'Trade': ['Sell', 'Buy', 'Buy'],
            'Rate': [2500,2480,'Market'],
            'Amount': [10, 5.5, 3.7],
            'address': ['0x788B21A949250f682e260679D0B3aFf2C29b884A', 
                        '0x250D5C91Af9Df21B473E3ab0c37A6566BA863404', 
                        '0x33b80ba090487012aB049380D781b91e39481CA8']
            })


# Welcome to CryptoFlea

st.title("Welcome to Crypto Flea Market!!")


# Display list of offers currently in the system
st.markdown("### Here are offers currently in the market.")




# Display a list of offers for user to select using a selection box
#st.session_state.offers['TradeID']
offers_str = display_offers(st.session_state.offers)

selected_offer = st.selectbox(
    'Which offer do you want to accept?', options=offers_str)

def remove_offer(selected_offer):
    delim_str = selected_offer.split(';')
    id = int(delim_str[-1].split(':')[-1])
    off = st.session_state.offers
    for i, row in off.iterrows():
        #x = 1
        if row.TradeID == id:
            x = i
            updated_offers = off.drop([i])
    st.session_state.offers = updated_offers

transaction_amount = st.number_input("Input transaction amount")
your_address = st.text_input("Your wallet address")

st.button("Transact", on_click=remove_offer, args=[selected_offer])
    #st.markdown(f'You selected {selected_offer}. {transaction_amount} of ether is transacted at {your_address}')
    #st.balloons()
    # remove the offer from the list

    

#def add_offer(trade_type, exchange_rate, limit, offer_address):
#    id = st.session_state['offers'][-1] + 1
#    st.session_state['offers'].append({'TradeID': id, 'Trade': trade_type, 'Rate': exchange_rate, 'Limit': limit, 'address': offer_address})


# Here we can invite user to make his/her own offer
#st.markdown("### Please make your offer here.")
#trade_type = st.selectbox('Buy or Sell?', ('Buy','Sell'))
#offer_address = st.text_input("Transaction wallet address")
#exchange_rate = st.text_input("Your exchange rate")
#st.button("Make Offer", on_click=add_offer, args=[trade_type, exchange_rate, 0, offer_address])

