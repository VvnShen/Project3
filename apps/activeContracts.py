from apps.basics import *
from apps.settle import *
from apps.commonProperties import *


def show_active_contracts():
    df_trade = pd.read_csv(trade_data)
    df_initiated=df_trade[df_trade['STATUS']=='Initiated']
    df_initiated['INIT'] = df_initiated['INIT_AMOUNT'].map(str).str.cat(df_initiated['INIT_CCY'],sep=" ")
    df_initiated['SETTLE'] = df_initiated['SETTLE_AMOUNT'].map(str).str.cat(df_initiated['SETTLE_CCY'],sep=" ")

    colms = st.columns((1, 1,2,2,1))
    fields = ['TRN_NB','PRICE','Do you have...','want to swap to...',"Action"]
    for col, field_name in zip(colms, fields):
        col.write(field_name)# header

    for x, nb in enumerate(df_initiated['TRN_NB']):
        x=nb-1
        col1, col2, col3,col4,col5= st.columns((1,1,2,2,1))
        col1.write(nb)  
        col2.write(df_initiated['PRICE'][x]) 
        col3.write(df_initiated['SETTLE'][x])
        col4.write(df_initiated['INIT'][x])
        if col5.checkbox('SWAP', key=x):
            if df_initiated['INIT_CCY'][x]=='ETH':
                settle_ETH(df_initiated['PRICE'][x],df_initiated['INIT_AMOUNT'][x].item(),df_initiated['CONTRACT_ADDRESS'][x],df_initiated['INITIALIZER'][x],x,nb)
            else:
                settle_USDC(df_initiated['PRICE'][x],df_initiated['INIT_AMOUNT'][x].item(),df_initiated['CONTRACT_ADDRESS'][x],df_initiated['USDC_TOKEN_ADDRESS'][x],x,nb)
                
            




            





