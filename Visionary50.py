import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import time

# Load the company data from Excel
df = pd.read_excel("visionary50.xlsx")

# Ensure the file has the correct columns
df = df[["Ticker", "Weightage"]]

# Convert weightage to dictionary
stocks = dict(zip(df["Ticker"], df["Weightage"]))

base_value = 1000  # Base value for the index

time_stamps = []
index_values = []

# Function to fetch live prices
def fetch_prices(tickers):
    prices = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            prices[ticker] = stock.history(period="1d")['Close'].iloc[-1]
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            prices[ticker] = None
    return prices

# Function to update and plot the index
def update_and_plot():
    initial_weighted_cmp = None
    while True:
        live_prices = fetch_prices(stocks)
        valid_prices = {t: p for t, p in live_prices.items() if p is not None}
        
        if not valid_prices:
            print("No valid stock prices fetched. Retrying...")
            time.sleep(60)
            continue
        
        weighted_cmp = sum(valid_prices[ticker] * stocks[ticker] for ticker in valid_prices)
        
        if initial_weighted_cmp is None:
            initial_weighted_cmp = weighted_cmp
        
        index_value = (weighted_cmp / initial_weighted_cmp) * base_value
        index_value_rounded = round(index_value, 2)
        
        current_time = pd.Timestamp.now()
        time_stamps.append(current_time)
        index_values.append(index_value_rounded)
        
        # Plot
        plt.figure(figsize=(10, 6))
        plt.plot(time_stamps, index_values, label="Visionary50 Index", color='blue', linewidth=2)
        plt.title("Visionary50 Index Over Time")
        plt.xlabel("Time")
        plt.ylabel("Index Value")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.draw()
        plt.pause(60)  # Update every 60 seconds

# Start live plotting
plt.ion()
update_and_plot()
