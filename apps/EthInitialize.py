import streamlit as st
from apps.basics import *
from apps.commonProperties import *


def EthInitializeApp():
    st.title('ETH -> USDC')
    st.markdown('## Are you owning Ether and want to swap to some USDC?')
    st.markdown("## Yes! This is the right page for you.")
    st.markdown("### First of all, Please fill in below information carefully.")
    initialize_address = st.selectbox("What's your wallet address?", options=accounts)
    price = st.number_input('What ETH/USDC price you want this swap settle at? ')
    amount = int(st.number_input("How many ETH do you want to swap?"))
    initialize_amount = int(amount*eth_to_wei)   # initialize amount has to be in wei
    settle_amount = int(price*amount)
    if st.button("Initialize ETH-USDC Swap"):
        # compile and deploy smart contract by using initializer's address
        eth_contract_interface = complile_contract(sol,0)
        eth_contract_address = deploy_contract(eth_contract_interface,initialize_address)
        #load contract
        eth_contract = load_contract(eth_contract_interface,eth_contract_address)
        tx_hash = eth_contract.functions.initialize().transact({'value': initialize_amount, 'from': initialize_address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        TRN_NB = new_trade_ID(trade_data)
        record_new_transaction(trade_data,TRN_NB,price,amount,'ETH',settle_amount,'USDC',initialize_address,eth_contract_address)
        st.write("Congratulations! You have successfully initialized a new smart contract - ETH->USDC.")
        st.write(f"Your {amount} ETH have been locked under your new contract. Please take a note of your contract token address:")
        st.write(eth_contract_address)
        st.write(dict(receipt))
        