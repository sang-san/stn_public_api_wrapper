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
