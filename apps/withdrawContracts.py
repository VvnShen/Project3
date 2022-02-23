from apps.basics import complile_contract,load_contract,update_transaction,w3
from apps.commonProperties import *

eth_contract_interface = complile_contract('BackEnd/DEX_ETHowner.sol',0)
usdc_token_interface = complile_contract('BackEnd/USDC_testnet.sol',1)
usdc_contract_interface = complile_contract('BackEnd/DEX_USDCOwner.sol',0)

def withdraw_active_contracts():
    withdraw_wallet = st.text_input("what's your wallet address?")
    st.write("By clicking Cancel contract button, your contract will be canceled. Gas fees will be charged by Ethereum Blockchain. Please think carefully before taking the action.")
    df_trade = pd.read_csv(trade_data)
    df_withdraw=df_trade[df_trade['STATUS']=='Initiated']
    df_withdraw=df_withdraw[df_withdraw['INITIALIZER']==withdraw_wallet]
    df_withdraw['INIT'] = df_withdraw['INIT_AMOUNT'].map(str).str.cat(df_withdraw['INIT_CCY'],sep=" ")

    colms = st.columns((1,3,1,1,1))
    fields = ['TRN_NB','Contract Address','PRICE','amount have been deposited',"Action"]
    for col, field_name in zip(colms, fields):
            # header
        col.write(field_name)

    for x, nb in enumerate(df_withdraw['TRN_NB']):
        x=nb-1
        col1, col2, col3,col4,col5= st.columns((1,3,1,1,1))
        col1.write(nb)  
        col2.write(df_withdraw['CONTRACT_ADDRESS'][x]) 
        col3.write(df_withdraw['PRICE'][x])
        col4.write(df_withdraw['INIT'][x])
        if col5.button('Cancel Contract', key=x):
            if df_withdraw['INIT_CCY'][x] == 'ETH':
                eth_contract=load_contract(eth_contract_interface,df_withdraw['CONTRACT_ADDRESS'][x])
                tx_hash = eth_contract.functions.withdrawSwap().transact({'value': df_withdraw['INIT_AMOUNT'][x].item()*eth_to_wei, 'from': withdraw_wallet, 'gas': 1000000})
                receipt = w3.eth.waitForTransactionReceipt(tx_hash)
                st.write(dict(receipt))
            else:
                usdc_contract=load_contract(usdc_contract_interface,df_withdraw['CONTRACT_ADDRESS'][x])
                tx_hash = usdc_contract.functions.withdrawSwap(df_withdraw['USDC_TOKEN_ADDRESS'][x]).transact({'from': withdraw_wallet, 'gas': 1000000})
                receipt = w3.eth.waitForTransactionReceipt(tx_hash)
                st.write(dict(receipt))

            update_transaction(trade_data,str(nb),'Canceled')
            



            





