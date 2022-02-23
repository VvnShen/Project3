import os
import streamlit as st
import pandas as pd
from web3 import Web3
from dotenv import load_dotenv
load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

eth_to_wei = 1000000000000000000
usdc_to_viv = 1000000
total_USDC_token = 1000000000000000000
accounts = w3.eth.accounts
sol = './BackEnd/DEX_ETHowner.sol'
trade_data = './Data/Trade.csv'
sol_DEX = './BackEnd/DEX_USDCowner.sol'
sol_USDC= './BackEnd/USDC_testnet.sol'