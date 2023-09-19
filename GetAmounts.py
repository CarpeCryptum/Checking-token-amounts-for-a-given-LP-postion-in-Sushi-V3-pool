import requests
from web3 import Web3
import math

key='YOUR KEY'

url='YOUR BLOCKCHAIN API'
w3 = Web3(Web3.HTTPProvider(url))

addr_Pos_Manager='address of the NonfungiblePositionManager contract on the given chain'
addr_pool='addrerss of the pool in which the LP is'
position_NFT_ID= >the ID number of the NFT token<
token0_decimals=18 #or what the nuber is for the given token
token1_decimals=18 #or what the nuber is for the given token
shift=10**(token0_decimals-token1_decimals)


def getabi(addr):
    page = requests.get('https://api.arbiscan.io/api?module=contract&action=getabi&address=' + addr + '&apikey=' + key + '')
    data = page.json()['result']
    return data

def getprice(addr, abi):
    contract = w3.eth.contract(address=addr, abi=abi)
    pricedata = contract.functions.slot0().call()
    sqr = float(pricedata[0])
    tick = float(pricedata[1])
    nmr = sqr**2
    denmr = 2**192
    sqr_ratio = nmr / denmr
    tick_ratio = 1.0001**tick
    return sqr_ratio, tick_ratio
def getamount(addr, abi, ID):
    contract = w3.eth.contract(address=addr, abi=abi)
    amountdata = contract.functions.positions(ID).call()
    liquidity = float(amountdata[7])
    tickUpper = float(amountdata[6])
    tickLower = float(amountdata[5])
    priceUpper=(1.0001**tickUpper)/shift
    priceLower=(1.0001**tickLower)/shift
    currentPrice=(getprice(addr_pool, getabi(addr_pool))[0])/shift
    amount0=liquidity*((math.sqrt(priceUpper)-math.sqrt(currentPrice))/(math.sqrt(currentPrice)*math.sqrt(priceUpper)))
    amount1=liquidity*(math.sqrt(currentPrice)-math.sqrt(priceLower))
    return currentPrice, amount0, amount1

getamount(addr_Pos_Manager, getabi(addr_Pos_Manager), position_NFT_ID)  
