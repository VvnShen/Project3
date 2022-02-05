import os
import json
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

def display_offers(offers):
    output = []     # output strings             
    for o in offers:
        str = f"{o['Trade']}; Exchange Rate: {o['Rate']}"
        output.append(str)
    
    return output

# initialize current offer structure
offers = [
    {'Trade': 'Sell', 'Rate': 2500, 'Limit': 10, 'address': '0x788B21A949250f682e260679D0B3aFf2C29b884A'},
    {'Trade': 'Buy', 'Rate': 2480, 'Limit': 5.5, 'address': '0x250D5C91Af9Df21B473E3ab0c37A6566BA863404'},
    {'Trade': 'Buy', 'Rate': 'Market', 'Limit': 3.7, 'address': '0x33b80ba090487012aB049380D781b91e39481CA8'}
]


# Welcome to CryptoFlea

st.title("Welcome to Crypto Flea Market!!")

# Display list of offers currently in the system
st.markdown("### Here are offers currently in the market.")
#st.markdown("```User: Apple; Trade: Sell; Exchange Rate: 2500 USDC```")

# Display a list of offers for user to select using a selection box
offers_str = display_offers(offers)
selected_offer = st.selectbox(
     'Which offer do you want to accept?', options=offers_str)#offers, format_func=display_offers) 
     #('Sell; Exchange Rate: 2500 USDC', 'Buy; Exchange Rate: 2300 USDC', 'Buy; Exchange Rate: Market Order'))


transaction_amount = st.number_input("Input transaction amount")
if st.button("Transact"):
    st.markdown(f'{transaction_amount} of ether is transacted')
    st.balloons()

# Here we can invite user to make his/her own offer

st.markdown("### Please make your offer here.")
trade_type = st.selectbox('Buy or Sell?', ('Buy','Sell'))
wallet_address = st.text_input("Your wallet address")
exchange_rate = st.text_input("Your exchange rate")
if st.button("Make Offer"):
    offers.append({'Trade': trade_type, 'Rate': exchange_rate, 'Limit': 0, 'address': wallet_address})

