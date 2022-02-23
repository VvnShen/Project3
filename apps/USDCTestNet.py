import streamlit as st
from apps.basics import *
from apps.commonProperties import *


def UsdcTestnet():
    st.title('Wanna some fake USDC for testing?')
    wallet_address = st.selectbox("What's your wallet address?", options=accounts)
    if st.button("Get USDC"):
        # compile and deploy smart contract by using initializer's address
        usdc_token_interface = complile_contract(sol_USDC,1)
        usdc_token_address = deploy_contract(usdc_token_interface,wallet_address)
        st.write("Here you go!")
        st.write("Now you have 1000000000000 USDC to spend! Take a note of your USDC tken adrress:")
        st.write(usdc_token_address)
        