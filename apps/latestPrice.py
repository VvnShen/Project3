from web3 import Web3
import streamlit as st
from apps.basics import record_price,get_last_data
from apps.commonProperties import *
import altair as alt

# Change this to use your own infura ID
web3 = Web3(Web3.HTTPProvider('https://kovan.infura.io/v3/34ed41c4cf28406885f032930d670036'))
# AggregatorV3Interface ABI
abi = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
# Price Feed address
addr = '0x9326BFA02ADD2366b30bacB125260Af641031331'
# Set up contract instance
contract = web3.eth.contract(address=addr, abi=abi)

def latestPrice():  
    # Make call to latestRoundData()
    latestData = contract.functions.latestRoundData().call()
    price=latestData[1]/100000000
    if latestData[0] > get_last_data(price_data):
        record_price(price_data,latestData[0],latestData[1])
    return price


def get_historical_data_plot():
    validRoundId = get_last_data(price_data)
    start_validRoundId=validRoundId-50
    historicalData = contract.functions.getRoundData(start_validRoundId).call()
    record_price(his_price_data,historicalData[0],historicalData[1]/100000000,'w')
    for id in range(start_validRoundId,validRoundId+1):
        historicalData = contract.functions.getRoundData(id).call()
        record_price(his_price_data,historicalData[0],historicalData[1]/100000000)
    header_list = ['RoundId','Price']
    df=pd.read_csv(his_price_data,names=header_list)
    df_price=df['Price']
    st.sidebar.line_chart(df_price,use_container_width=True)

    