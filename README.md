# sangria_stn_public_api_wrapper
Makes using the public stn api easier.

Example:
```py
import asyncio
from sangria_stn_public_api_wrapper import stn_public_api_wrapper

async def main():
  key = str(input("Your Stn Api Key: "))
  stn_api_i = stn_public_api_wrapper(key) # init the wrapper
  
  price_res = await asyncio.create_task(stn_api_i.get_key_prices())
  
  if price_res.prices.buy_ref > 55:
    trade_res = await asyncio.create_task(stn_api_i.get_key_trade("sell"))
    
    if trade_res.state == 1:
      print(f"ordered a sell keys trade, the bot that sends the offer is {trade_res.result.bot}"
      
  await asyncio.sleep(10)
  
  fetch_trade_res = await asyncio.create_task(stn_api_i.get_trade_state(trade_res.result.id))
  print(f"the current state of the created Trade is : {fetch_trade_res.trade_status.state_str}")
    
asyncio.run(main())

```

Docs:

# Inits the Wrapper.
```py
stn_public_api_wrapper(apiKey, print_logs=False)
```
apiKey: Your stn api key 

print_logs: Defaults to true, if switched off it will no longer print if an api call was successfull or not

All classes that are returned by the api call functions have a
```
result.state
```
Property.

result.state = 0 --> Failed # will have a .error str property that explains what went wrong

result.state = 1 --> Successful # will also have a subclass with the values of the result

result.state = 2 --> Not Started Yet


# Gets the key prices stn currently pays.
```py
result = await stn_public_api_wrapper_instance.get_key_prices() ### is a coroutine
```
Example what you would want to access if the Call was Successfull:
```
result.state = 1
result.prices.buy_ref = 50.0 # how much they would give you for a sell intent trade with amount 1
result.prices.sell_ref = 55.0  # how much they would ask from  you for a buy intent trade with amount 1
```
Example what you would want to access if the Call was un-successfull:
```
result.state = 0
result.error = "some string explaining the error "
```





# Requests a trade from stn.
Note that stn only allows 1 key trade at a time.
```py
result = await stn_public_api_wrapper_instance.get_key_trade(intent, amount) ### is a coroutine
```
intent: either "buy" or "sell" depending on if you either want to buy or sell key

amount: an integer from 1-10, anything above or under that will raise an value error as stn doesnt allow you to trade keys in any other volumne


Example what you would want to access if the Call was Successfull:
```
result.state = 1
result.result.id = 121212 # the trade id stn has given for this trade, you can  request the trade state with get_trade_result with this id
result.result.bot = someSteamId64 # the steamid64 of the bot that will send you the trade
```
Example what you would want to access if the Call was un-successfull:
```
result.state = 0
result.error = "some string explaining the error "
```



# Gets the current TradeOffer State for a stn key trade.

```py
result = await stn_public_api_wrapper_instance.get_trade_state(stn_trade_id) ### is a coroutine
```
stn_trade_id: the id stn gives you for a get_key_trade call, aka result.result.id

Possible Trade States that exist:

0: Ready to be sent

1: Sent

2: Completed

3: Confirm pending

15: Cancelled after sending

20: Sending failed


Example what you would want to access if the Call was Successfull:
```
result.state = 1
result.trade_status.state = 0 # any of the trade statuses stn can give you from above, result.state != result.trade_status.state
result.trade_status.state_str = "Ready to be sent" # a translation of the state in int form to a str describing the state better for humans
result.trade_status.trade_id = someSteamTradeId # the trade steam id for this trade,  result.trade_status.trade_id != the stn id you get from get_key_trade()
```

Example what you would want to access if the Call was un-successfull:
```
result.state = 0
result.error = "some string explaining the error "
```








