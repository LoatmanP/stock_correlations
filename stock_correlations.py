import streamlit as st
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt


st.write("""
# Stock Correlation Application
Insert two stocks to determine how strongly correlated they are
""")

stock_1 = st.text_input("Insert Ticker Symbol for First Stock (e.g., AAPL)")
stock_2 = st.text_input("Insert Ticker Symbol for Second Stock (e.g., AMZN)")

if stock_2 and stock_1:

    #get data on this ticker

    stock_1_tickerData = yf.Ticker(stock_1)
    stock_2_tickerData = yf.Ticker(stock_2)

    #get the historical prices for this ticker
    stock_1_tickerDf = stock_1_tickerData.history(period='max').reset_index()
    stock_2_tickerDf = stock_2_tickerData.history(period= 'max').reset_index()

    stock_1_tickerDf['stock'] = stock_1
    stock_2_tickerDf['stock'] = stock_2

    min_stock_1 = min(stock_1_tickerDf['Date'])
    min_stock_2 = min(stock_2_tickerDf['Date'])

    max_min_stock_date = max([min_stock_1, min_stock_2])

    stock_1_tickerDf = stock_1_tickerDf.loc[stock_1_tickerDf['Date'] >= max_min_stock_date]
    stock_2_tickerDf = stock_2_tickerDf.loc[stock_2_tickerDf['Date'] >= max_min_stock_date]

    df_1 = stock_2_tickerDf
    df_2 = stock_2_tickerDf

    stock_1_tickerDf.columns = ['Date', 'stock_1_Open', 'stock_1_High', 'stock_1_Low', 'stock_1_Close', 'stock_1_Volume', 'stock_1_Dividends',
           'stock_1_Stock Splits', 'stock_1']

    stock_2_tickerDf.columns = ['Date', 'stock_2_Open', 'stock_2_High', 'stock_2_Low', 'stock_2_Close', 'stock_2_Volume', 'stock_2_Dividends',
           'stock_2_Stock Splits', 'stock_2']

    bigdata  = stock_1_tickerDf.merge(stock_2_tickerDf, how = 'inner', on = 'Date')

    correlation = round(bigdata.stock_1_Close.corr(bigdata.stock_2_Close),2)

    st_plot = bigdata[['Date', 'stock_1_Close','stock_2_Close']]
    st_plot.columns = ['Date', "{0} Stock Price".format(stock_1), "{0} Stock Price".format(stock_2)]

    df = st_plot.melt('Date', var_name='stock', value_name='value')


    sns.set(font="IBM Plex Sans",  style='white')
    color_palette = ['29bf89','0083BB']
    fig, ax = plt.subplots()
    ax = sns.lineplot(x = 'Date', y = st_plot.iloc[:,1], data=st_plot, color='seagreen')
    ax2 = plt.twinx()
    ax= sns.lineplot(data=st_plot, color='royalblue', ax=ax2, x = 'Date', y = st_plot.iloc[:,2])
    ax.set_title("The correlation between {0} and {1} is: {2} ".format(stock_1, stock_2, correlation))
    plt.figure(facecolor='w')
    fig.legend(labels=["{0} Stock".format(stock_1),"{0} Stock".format(stock_2)],loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=2)

    st.pyplot(fig)









