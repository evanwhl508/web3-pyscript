from pyscript import document, window
from pyodide.http import pyfetch
from pyodide.code import run_js

MESSAGE = "This is a message to sign for PyScript - Metamask integration"
document.getElementById("message").innerHTML = f"Message to sign: <b>{MESSAGE}</b>"

def get_joke(event):
    jokes_element = document.getElementById("jokes")
    joke_str = pyjokes.get_joke()
    jokes_element.innerText = joke_str

async def sign_message_on_click(event):
    if not window.ethereum.selectedAddress:
        # prompt alert dialog
        window.alert("Please login with MetaMask")
        return
    message = MESSAGE
    signature = await run_js("window.ethereum.request({method: 'personal_sign',params: ['"+ message + "', window.ethereum.selectedAddress]})")
    document.getElementById("signature").innerText = f"{signature}"

async def get_wallet_balance_api(addr: str):
    # read api key from element with id "api-key"
    etherscan_api_key = document.getElementById("api-key").value
    if not etherscan_api_key:
        window.alert("Please enter your etherscan API key")
        return
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={addr}&tag=latest&apikey={etherscan_api_key}"
    res = await pyfetch(url)
    data = await res.json()
    wallet_balance = data.get("result")
    return wallet_balance

async def get_wallet_balance_api_on_click(addr: str):
    if not window.ethereum.selectedAddress:
        # prompt alert dialog
        window.alert("Please login with MetaMask")
        return
    user_account = window.ethereum.selectedAddress
    wallet_balance = await get_wallet_balance_api(user_account)
    balance_element = document.getElementById("wallet_balance_api")
    balance_element.innerHTML = f"Wallet balance from etherscan API: {wallet_balance}"

async def get_wallet_balance_js(addr: str):
    wallet_balance = await run_js("window.ethereum.request({method: 'eth_getBalance',params: ['" + addr + "', 'latest']})")
    return wallet_balance[2:]

async def get_wallet_balance_js_on_click(addr: str):
    if not window.ethereum.selectedAddress:
        # prompt alert dialog
        window.alert("Please login with MetaMask")
        return
    user_account = window.ethereum.selectedAddress
    wallet_balance = await get_wallet_balance_js(user_account)
    balance_element = document.getElementById("wallet_balance_js")
    balance_element.innerText = f"Wallet balance from Metamask RPC: {wallet_balance}"

async def connect_wallet_on_click(event):
    is_metamask: bool = window.ethereum.isMetaMask
    is_connected: bool = window.ethereum.isConnected()
    # connect metamask if not connected
    if not window.ethereum.selectedAddress:
        window.ethereum.enable()
    user_account = window.ethereum.selectedAddress
    wallet_element = document.getElementById("public_address")
    wallet_element.innerText = f"My public address is: {user_account}"
