from solcx import compile_source
from csv import DictWriter
import csv
from apps.commonProperties import *

def complile_contract(contract_source_file,key):
    with open(contract_source_file, "r") as f:
        contract_source_code = f.read()
    compiled_sol = compile_source(contract_source_code, output_values=['abi', 'bin'])
    contractName = list(compiled_sol.keys())[key]
    contract_interface = compiled_sol[contractName]
   
    return contract_interface


def deploy_contract(contract_interface, user_address):
    bytecode = contract_interface['bin']
    abi = contract_interface['abi']
    w3.eth.default_account = user_address
    contract_to_deploy = w3.eth.contract(abi=abi,bytecode=bytecode)
    tx_hash = contract_to_deploy.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt['contractAddress']


def load_contract(contract_interface, token_address):
    abi = contract_interface['abi']
    contract = w3.eth.contract(
        address=token_address,
        abi=abi
    )

    return contract

def record_new_transaction(file_name,TRN_NB,PRICE,INIT_AMOUNT,INIT_CCY,SETTLE_AMOUNT,SETTLE_CCY,INITIALIZER,CONTRACT_ADDRESS,USDC_TOKEN_ADDRESS=None):
    CSV_Header = ['TRN_NB','PRICE','INIT_AMOUNT','INIT_CCY','SETTLE_AMOUNT','SETTLE_CCY','INITIALIZER','SETTLER','CONTRACT_ADDRESS','USDC_TOKEN_ADDRESS','STATUS']
    body_dict = {
        'TRN_NB':TRN_NB,
        'PRICE':PRICE,
        'INIT_AMOUNT':INIT_AMOUNT,
        'INIT_CCY':INIT_CCY,
        'SETTLE_AMOUNT':SETTLE_AMOUNT,
        'SETTLE_CCY':SETTLE_CCY,
        'INITIALIZER':INITIALIZER,
        'SETTLER':'',
        'CONTRACT_ADDRESS':CONTRACT_ADDRESS,
        'USDC_TOKEN_ADDRESS':USDC_TOKEN_ADDRESS,
        'STATUS':'Initiated'
    }
    with open(file_name,'a',newline='') as file:
        dictwriter_object = DictWriter(file, fieldnames=CSV_Header)
        dictwriter_object.writerow(body_dict)
        file.close()


def new_trade_ID(file_name):
    with open(file_name,'r') as file:
        TRN_NB = len(file.readlines())
        file.close()
    return TRN_NB


def update_transaction(file_name,TRN_NB,Status,USDC_TOKEN_ADDRESS=None,SETTLER=None):
    CSV_Header = ['TRN_NB','PRICE','INIT_AMOUNT','INIT_CCY','SETTLE_AMOUNT','SETTLE_CCY','INITIALIZER','SETTLER','CONTRACT_ADDRESS','USDC_TOKEN_ADDRESS','STATUS']
    data = []

    with open(file_name,'r') as file_read:
        csv_reader = csv.DictReader(file_read, fieldnames=CSV_Header)
        header = next(csv_reader)

        for line in csv_reader:
            if line['TRN_NB'] == TRN_NB:
                line['STATUS']=Status
                line['USDC_TOKEN_ADDRESS']=USDC_TOKEN_ADDRESS
                line['SETTLER']=SETTLER
            data.append(line)
        file_read.close()

    with open(file_name,'w') as file_write:
        csv_writer = csv.DictWriter(file_write, fieldnames=CSV_Header)
        csv_writer.writeheader()
        csv_writer.writerows(data)
        file_write.close()


def record_price(file_name,roundId,price,mode='a'):
    CSV_Header = ['RoundId','Price']
    body_dict = {
        'RoundId':roundId,
        'Price':price
    }
    with open(file_name,mode,newline='') as file:
        dictwriter_object = DictWriter(file, fieldnames=CSV_Header)
        dictwriter_object.writerow(body_dict)
        file.close()
    
def get_last_data(file_name,data='RoundId'):
    df=pd.read_csv(file_name)
    last_data=df.tail(1).values.tolist()
    if data == 'RoundId':
        return int(last_data[0][0])
    else:
        return int(last_data[0][1])







    

