
from re import S
import time
from typing import Text 
import aiohttp 

import asyncio


class new_requested_key_trade:
    async def get(self, apiKey, action, amount:int, printStuff=False):


        self.endpoint = "https://api.stntrading.eu/RequestKeyTrade/v1"

        self.apikey = apiKey

        self.state = 2 #aka not started yet
        self.error = None
        self.result = None

        if amount < 1 or amount > 10 or not isinstance(amount, int):
            raise ValueError(f"amount must be between 1 and 10 and a integer you provided {amount} with type {type(int)} ")

        if action != "buy" and action != "sell":
            raise ValueError(f"Action must be either 'buy' or 'sell' you provided the action as: {action} ")
            
        async with aiohttp.ClientSession() as session:
            async with session.post(self.endpoint, data={
                "apikey": self.apikey,
                "action": action,
                "amount": int(amount)
            }) as resp:
                if resp.status != 200:
                    if printStuff == True: print(f"gettting a new key trade failed, status code was {resp.status} and the response text was {await resp.text()}")
                    self.state = 0 # aka failed
                    self.error = f"request hat a not 200 code code was {resp.status}, res was {await resp.text()} "
                    return

                loaded_json = await resp.json()
                if loaded_json["success"] == 1:
                    self.result = self.request_result(loaded_json["result"]["tradeDetails"]["id"], loaded_json["result"]["tradeDetails"]["bot"])

                    if printStuff == True: print(f"stn key trade was created successfully, trade Id: {self.result.id}")
                    self.state = 1
                    return

                if loaded_json["success"] == 0:
                    self.state == 0
                    self.error = loaded_json["error"]
                    if printStuff == True: print(f"getting a new key trade failed, it returned a status code 0 with the error: {self.error} ")
                    return

    class request_result:
        def __init__(self, id:int, bot:str) -> None:
            self.id = id
            self.bot = int(bot)

class new_requested_key_prices:
    async def get(self, apikey, printStuff=False):
        
        self.url = f"https://api.stntrading.eu/GetKeyPrices/v1?apikey={apikey}"

        self.state = 2

        self.prices = None
        self.error = None
        

        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
                if resp.status != 200:
                    if printStuff == True: print(f"getting key prices failed, status code was not 200, status code: {resp.status}, text {await resp.text()} ")
                    self.state = 0
                else:

                    loadedJson = await resp.json()
                    if loadedJson["success"] == 0:
                        if printStuff == True: print(f"getting key prices failed, success == 0, status code: {resp.status}, error {loadedJson['error']} ")
                        self.state = 0
                        self.error = loadedJson["error"]
                        return None

                    if loadedJson["success"] == 1:
                        self.prices = self.request_result(loadedJson['result']["pricing"]["buyPrice"], loadedJson['result']["pricing"]["sellPrice"])
                        if printStuff == True: print(f"getting key prices succeeded, success == 1, status code: {resp.status}, ref buy: {self.prices.buy_ref} sell ref: {self.prices.sell_ref}")
                        self.state = 1
                        return None


        

    class request_result:
        def __init__(self, buy_scrap, sell_scrap):
            self.buy_ref = float(str(buy_scrap / 9)[:5])
            self.sell_ref = float(str(sell_scrap / 9)[:5])

class new_requested_trade_state:
    async def get(self, apikey, tradeId, printStuff=False):
        
        self.url = f"https://api.stntrading.eu/GetTradeStatus/v1?apikey={apikey}&id={tradeId}"

        self.state = 2
        self.error = None
        self.trade_status = None

        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp: 
                if resp.status != 200:
                    if printStuff == True: print(f"getting key prices failed, status code was not 200, status code: {resp.status}, text {await resp.text()} ")
                    self.state = 0
                else:
                    loadedJson = await resp.json()
                    if loadedJson["success"] == 0:
                        if printStuff == True: print(f"getting trade status failed, success == 0, status code: {resp.status}, error {loadedJson['error']} ")
                        self.state = 0
                        self.error = loadedJson["error"]
                        return None

                    if loadedJson["success"] == 1:
                        self.trade_status = self.request_result(loadedJson["result"]["trade"]["state"], loadedJson["result"]["trade"]["tradeOfferId"])
                        if printStuff == True: print(f"getting trade status was success, success == 1, status code: {resp.status}, state Str: {self.trade_status.state_str} ")
                        self.state = 1


    class request_result:
        def __init__(self, state, trade_id) -> None:
            
            self.id_to_str = {
                0: "Ready to be sent",
                1: "Sent",
                2: "Completed",
                3: "Confirm pending",
                15: "Cancelled after sending",
                20: "Sending failed",
            }

            self.state = state
            self.state_str = self.id_to_str[state]
            self.trade_id = trade_id if self.state == 1 or self.state == 2 else None
            

class stn_public_api_wrapper:
    def __init__(self, apiKey, print_logs=True):
        self.apiKey = apiKey
        self.print_logs = print_logs

    async def get_key_trade(self, intent, amount):
        new_trade_obj = new_requested_key_trade()
        await new_trade_obj.get(self.apiKey, intent, amount, printStuff=self.print_logs)
        return new_trade_obj

    async def get_key_prices(self):
        new_prices_obj = new_requested_key_prices()
        await new_prices_obj.get(self.apiKey, printStuff=self.print_logs)
        return new_prices_obj

    async def get_trade_state(self, trade_id:int):
        new_fetch_trade_obj = new_requested_trade_state()
        await new_fetch_trade_obj.get(self.apiKey, trade_id, printStuff=self.print_logs)
        return new_fetch_trade_obj