import os
import json
from more_itertools import one
from pyparsing import one_of
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

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

def display_offers(offerss):
    output = []     # output strings             
    for o in offerss:
        str = f"{o['Trade']}; Exchange Rate: {o['Rate']}; ID: {o['TradeID']}"
        output.append(str)
    
    return output


# initialize current offer structure
if 'offers' not in st.session_state:
    st.session_state['offers'] = [
        {'TradeID': 0, 'Trade': 'Sell', 'Rate': 2500, 'Limit': 10, 'address': '0x788B21A949250f682e260679D0B3aFf2C29b884A'},
        {'TradeID': 1, 'Trade': 'Buy', 'Rate': 2480, 'Limit': 5.5, 'address': '0x250D5C91Af9Df21B473E3ab0c37A6566BA863404'},
        {'TradeID': 2, 'Trade': 'Buy', 'Rate': 'Market', 'Limit': 3.7, 'address': '0x33b80ba090487012aB049380D781b91e39481CA8'}
    ]
    current_offers = st.session_state['offers']


# Welcome to CryptoFlea

st.title("Welcome to Crypto Flea Market!!")


# Display list of offers currently in the system
st.markdown("### Here are offers currently in the market.")


# Display a list of offers for user to select using a selection box
offers_str = display_offers(st.session_state['offers'])
selected_offer = st.selectbox(
    'Which offer do you want to accept?', options=offers_str)

def remove_offer(offer):
    st.session_state['offers'] = offer
    #st.session_state['offers'].remove(offer)
    #current_offers = st.session_state['offers']


transaction_amount = st.number_input("Input transaction amount")
your_address = st.text_input("Your wallet address")
delim_str = selected_offer.split(';')
id = int(delim_str[-1].split(':')[-1])
# Find the selected offer
#temp = st.session_state['offers'].copy()
#i=1
#for i in range(current_offers):
#    if current_offers[i]['TradeID'] == id:
#        #del st.session_state['offers'][i]
#        i = range
#selected_offer = current_offers[i]
new_offers = [i for i in st.session_state['offers'] if not (i['TradeID'] == id)]
st.button("Transact", on_click=remove_offer, args=new_offers)
    #st.markdown(f'You selected {selected_offer}. {transaction_amount} of ether is transacted at {your_address}')
    #st.balloons()
    # remove the offer from the list

    

def add_offer(trade_type, exchange_rate, limit, offer_address):
    id = st.session_state['offers'][-1] + 1
    st.session_state['offers'].append({'TradeID': id, 'Trade': trade_type, 'Rate': exchange_rate, 'Limit': limit, 'address': offer_address})


# Here we can invite user to make his/her own offer
st.markdown("### Please make your offer here.")
trade_type = st.selectbox('Buy or Sell?', ('Buy','Sell'))
offer_address = st.text_input("Transaction wallet address")
exchange_rate = st.text_input("Your exchange rate")
st.button("Make Offer", on_click=add_offer, args=[trade_type, exchange_rate, 0, offer_address])

