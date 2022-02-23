import streamlit as st
from multiapp import MultiApp
from apps import EthInitialize,activeContracts,withdrawContracts,USDCInitialize,USDCTestNet # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Show active contracts", activeContracts.show_active_contracts)
app.add_app("I'm owning ETH, swapping it to USDC", EthInitialize.EthInitializeApp)
app.add_app("I'm owning USDC, swaping it to ETH",USDCInitialize.USDCInitializeApp)
app.add_app("I want to cancel my contracts", withdrawContracts.withdraw_active_contracts)
app.add_app("TESTNET: get some 'fake' USDC",USDCTestNet.UsdcTestnet)

# The main app
app.run()