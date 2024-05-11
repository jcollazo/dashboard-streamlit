import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

import json
import numpy as np
import yfinance as yf


COLOR_BULL = 'rgba(38,166,154,0.9)' # #26a69a
COLOR_BEAR = 'rgba(239,83,80,0.9)'  # #ef5350

#Change in future to tradier or Schwab
def loadChart(ticker):
    df = yf.Ticker(ticker).history(period="100d")[['Open', 'High', 'Low', 'Close', 'Volume']]
    return df

def pageIII():
    # Request historic pricing data via finance.yahoo.com API

    tickers = ("^SPX","SPY","QQQ","TSLA","AAPL","META","HD")
    ticker = st.sidebar.selectbox('Pick a ticker from the list', tickers)

    df = loadChart(ticker)
    
   
    # Some data wrangling to match required format
    df = df.reset_index()
    df.columns = ['time','open','high','low','close','volume']                  # rename columns
    df['time'] = df['time'].dt.strftime('%Y-%m-%d')                             # Date to string
    df['color'] = np.where(  df['open'] > df['close'], COLOR_BEAR, COLOR_BULL)  # bull or bear
    #df.ta.macd(close='close', fast=6, slow=12, signal=5, append=True)           # calculate macd

    # export to JSON format
    candles = json.loads(df.to_json(orient = "records"))
    volume = json.loads(df.rename(columns={"volume": "value",}).to_json(orient = "records"))
    #macd_fast = json.loads(df.rename(columns={"MACDh_6_12_5": "value"}).to_json(orient = "records"))
    #macd_slow = json.loads(df.rename(columns={"MACDs_6_12_5": "value"}).to_json(orient = "records"))
    #df['color'] = np.where(  df['MACD_6_12_5'] > 0, COLOR_BULL, COLOR_BEAR)  # MACD histogram color
    #macd_hist = json.loads(df.rename(columns={"MACD_6_12_5": "value"}).to_json(orient = "records"))


    chartMultipaneOptions = [
        {
            "width": 950,
            "height": 600,
            "layout": {
                "background": {
                    "type": "solid",
                    "color": 'white'
                },
                "textColor": "black"
            },
            "grid": {
                "vertLines": {
                    "color": "rgba(197, 203, 206, 0.5)"
                    },
                "horzLines": {
                    "color": "rgba(197, 203, 206, 0.5)"
                }
            },
            "crosshair": {
                "mode": 0
            },
            "priceScale": {
                "borderColor": "rgba(197, 203, 206, 0.8)"
            },
            "timeScale": {
                "borderColor": "rgba(197, 203, 206, 0.8)",
                "barSpacing": 15
            },
            "watermark": {
                "visible": True,
                "fontSize": 48,
                "horzAlign": 'center',
                "vertAlign": 'center',
                "color": 'rgba(171, 71, 188, 0.3)',
                "text": ticker,
            }
        },
        {
            "width": 1000,
            "height": 200,
            "layout": {
                "background": {
                    "type": 'solid',
                    "color": 'transparent'
                },
                "textColor": 'black',
            },
            "grid": {
                "vertLines": {
                    "color": 'rgba(42, 46, 57, 0)',
                },
                "horzLines": {
                    "color": 'rgba(42, 46, 57, 0.6)',
                }
            },
            "timeScale": {
                "visible": False,
            },
            "watermark": {
                "visible": True,
                "fontSize": 18,
                "horzAlign": 'left',
                "vertAlign": 'top',
                "color": 'rgba(171, 71, 188, 0.7)',
                "text": 'Volume',
            }
        },
        {
            "width": 1280,
            "height": 800,
            "layout": {
                "background": {
                    "type": "solid",
                    "color": 'white'
                },
                "textColor": "black"
            },
            "timeScale": {
                "visible": False,
            },
            "watermark": {
                "visible": True,
                "fontSize": 18,
                "horzAlign": 'left',
                "vertAlign": 'center',
                "color": 'rgba(171, 71, 188, 0.7)',
                "text": 'MACD',
            }
        }
    ]

    seriesCandlestickChart = [
        {
            "type": 'Candlestick',
            "data": candles,
            "options": {
                "upColor": COLOR_BULL,
                "downColor": COLOR_BEAR,
                "borderVisible": False,
                "wickUpColor": COLOR_BULL,
                "wickDownColor": COLOR_BEAR
            }
        }
    ]

    seriesVolumeChart = [
        {
            "type": 'Histogram',
            "data": volume,
            "options": {
                "priceFormat": {
                    "type": 'volume',
                },
                "priceScaleId": "" # set as an overlay setting,
            },
            "priceScale": {
                "scaleMargins": {
                    "top": 0,
                    "bottom": 0,
                },
                "alignLabels": False
            }
        }
    ]


    st.subheader("Reaper View")

    renderLightweightCharts([
        {
            "chart": chartMultipaneOptions[0],
            "series": seriesCandlestickChart
        },
        {
            "chart": chartMultipaneOptions[1],
            "series": seriesVolumeChart
        }
    ], 'multipane')