import requests
from web3 import Web3
import math

key='YOUR KEY'

url='YOUR BLOCKCHAIN API'
w3 = Web3(Web3.HTTPProvider(url))

addr_Pos_Manager='0xF0cBce1942A68BEB3d1b73F0dd86C8DCc363eF49'
addr_pool='0xB1aeB76B4E3e628ee54753AD4B8eF68C41E67a9f'
position_NFT_ID=6641
token0_decimals=18
token1_decimals=18
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
    return sqr_ratio*shift, tick_ratio*shift
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
    return currentPrice, amount0/(10**(token0_decimals)), amount1/(10**(token1_decimals))

getamount(addr_Pos_Manager, getabi(addr_Pos_Manager), position_NFT_ID)  
