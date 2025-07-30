# **Version 0:**
-**Usage** : python3 bank_nifty_V0.py
- It is a Python script that implements the trading strategy for Bank Nifty straddles using the Kite Connect API. (Basic version – only creates log files.)

# **Version 1:**
-**Usage** : python3 bank_nifty_V1.py
- In this the Version added live chart for PLCE plot using Matplotlib. Real-time tracking of Bank Nifty straddle trades. Log file generation retained from Version 0.

# **Version 2:**
--**Usage** : python3 bank_nifty_V2.py
-This version extends Version 1 by plotting live charts for both PLCE and PLPE plot using Matplotlib, enabling real-time tracking of Bank Nifty straddle trades. Log file generation is retained from Version 0.

# **Version 3:**
- -**Usage** : python3 bank_nifty_V0.py
- This version builds on Version 0 by adding SMA20 (Simple Moving Average) calculation and plotting for the CE (Call Option) value. Log file generation is retained.

# **Version 4:**
- In this version the Strategy1 is implimented
- Strtegy1 : Log file generation is retained from Version 0. In this the strategy implimented is, 
- **If offline = 0**: The program fetches live data and performs the necessary calculations.
- **If offline = 1**: It reads data from an Excel sheet and computes the corresponding values.
- **When plot = 0**: Only the output values are printed.
- **When plot = 1**: The output values are displayed along with a chart for visual representation.
- **File Name:** bank_nifty_sty1_V4.zip
- Inside zip file all input files required and two .py files are attached
- 1. bank_ce_pe_sty50_V4.py : ATM Strike, 50-point CE/PE strategy.
- 2. bank_ce_pe_sty100_V4.py: ATM Strike, 100-point CE/PE strategy
- **Usage** :python3 bank_ce_pe_sty50_V4.py or python3 bank_ce_pe_sty100_V4.py
- 
# **Version 5:**
- To be done
