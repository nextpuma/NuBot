import key
import json
import Symbols
import Analiz
import time
import math
import telegram
import datetime
import Settings
#import matplotlib.pyplot as plt

from binance.client import Client
client = Client(key.api_key, key.api_secret)

from color import colorize
#from color import uncolorize

from telegram import (Animation, Audio, Contact, Document, Chat, Location,
                      PhotoSize, Sticker, TelegramObject, User, Video, Voice,
                      Venue, MessageEntity, Game, Invoice, SuccessfulPayment,
                      VideoNote, PassportData)

bot = telegram.Bot(token=key.token)

def Strategy_PingPong():
  #print("Please input symbol(TRX):")
  #symbol = input()          #TRX or GAS
  symbol = Settings.symbolPP
  #print("Please input base price(0.00000600):")
  #base_price = input()
  base_price = Settings.base_pricePP
  budget_BTC = Settings.budget_BTCPP
  #print("Please input start operation(SELL/BUY):")
  #start_operation = input() #SELL or BUY
  start_operation = Settings.start_operationPP
  up_profit = Settings.up_profitPP
  down_profit = Settings.down_profitPP
  k = 0
  a=1

  while k <1:
    if symbol == Symbols.SymbolsMatrix[a][0]:
      le = len(str(Symbols.SymbolsMatrix[a][2]))
      k = 1
    else:
      a = int(a) + 1
  
  print(str(le))

  while True:
    time.sleep(1)
    balanceALT = client.get_asset_balance(asset=str(symbol))
    balanceALTJSON = json.dumps(balanceALT)
    balanceALTRESP = json.loads(balanceALTJSON)
    balanceALTFREE = balanceALTRESP['free']

    price = client.get_symbol_ticker(symbol=str(symbol)+"BTC")
    priceJSON = json.dumps(price)
    priceRESP = json.loads(priceJSON)
    price = priceRESP['price']
    aprofit = float(price) / float(base_price) - 1
    aprofit = float(aprofit) * 100
    aprofit = round(aprofit,2)
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " Symbol:\t" + str(symbol + "BTC") + "\n\tBase price: " + str(base_price) + "\n\tProfit UP: " + str(up_profit) + "\n\tProfit DOWN: " + str(down_profit))
    print("\tPrice: " + str(price) + "\tProfit: " + str(aprofit) + "%\tBalance: " + str(balanceALTFREE))
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

    if start_operation == "SELL" and float(base_price)*float(up_profit) < float(price):
        qua = float(balanceALTFREE)
        if le==1:
          qua = math.floor(qua)
        else: 
          qua = str(qua)[0:le]
        OrderSell = client.create_order(symbol=str(symbol+"BTC"), side=client.SIDE_SELL, type=client.ORDER_TYPE_LIMIT, timeInForce=client.TIME_IN_FORCE_GTC, quantity=str(qua), price=str(price))
        print(str(OrderSell))
        start_operation = "BUY"

    if start_operation == "BUY" and float(base_price)*float(down_profit) > float(price):
        qua = float(budget_BTC) / float(price)
        if le==1:
          qua = math.floor(qua)
        else: 
          qua = str(qua)[0:le]
        OrderBuy = client.create_order(symbol=str(symbol+"BTC"), side=client.SIDE_BUY, type=client.ORDER_TYPE_LIMIT, timeInForce=client.TIME_IN_FORCE_GTC, quantity=str(qua), price=str(price))
        print(str(OrderBuy))
        start_operation = "SELL"  
  


