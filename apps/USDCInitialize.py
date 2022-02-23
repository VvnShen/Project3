from apps.basics import *
from apps.commonProperties import *




def USDCInitializeApp():
    st.title('USDC -> ETH')
    st.markdown('## Are you owning USDC and want to convert some to ETH?')
    st.markdown("## Yes! This is the right page for you.")
    st.markdown("### First of all, Please fill in below information carefully.")
    initialize_address = st.selectbox("What's your wallet address?", options=accounts)
    price = st.number_input('What ETH/USDC price you want this swap settle at? ')
    usdc_amount = int(st.number_input("How many USDC do you want to swap?"))
    usdc_token_address=st.text_input('Please also provide USDC token address')

    usdc_testnet_contract_interface = complile_contract(sol_USDC,1)
    usdc_token_contract = load_contract(usdc_testnet_contract_interface, usdc_token_address)
    
    st.write("By clicking below button, you are authorizing the contract to lock USDC tokens in your wallet.")
    if st.button("Initialize USDC-ETH Swap"):
        usdc_contract_interface = complile_contract(sol_DEX,0)
        usdc_contract_address = deploy_contract(usdc_contract_interface,initialize_address)
        usdc_contract=load_contract(usdc_contract_interface,usdc_contract_address)
        tx_hash = usdc_token_contract.functions.approve(usdc_contract_address, usdc_amount*usdc_to_viv).transact({'from':initialize_address,'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        tx_hash = usdc_contract.functions.initialize(usdc_amount*usdc_to_viv, usdc_token_address).transact({'from': initialize_address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        TRN_NB = new_trade_ID(trade_data)
        record_new_transaction(trade_data,TRN_NB,price,usdc_amount,'USDC',usdc_amount/price,'ETH',initialize_address,usdc_contract_address,usdc_token_address)
        st.write("Congratulations! You have successfully initialized a new smart contract - USDC->ETH.")
        st.write(f"Your {usdc_amount} USDC have been locked under your new contract. Please take a note of your contract token address:")
        st.write(usdc_contract_address)
        st.write(dict(receipt))



        