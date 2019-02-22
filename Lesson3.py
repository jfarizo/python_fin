from yahoo_fin.stock_info import get_data
import statsmodels.formula.api as sm
import pandas as pd
import pandas_datareader.data as web
import datetime
import seaborn as sns


mkt_rf = web.DataReader('F-F_Research_Data_5_Factors_2x3', 'famafrench')[0]

mkt_rf = mkt_rf.drop(['SMB','HML', 'RMW', 'CMA'], axis=1)
mkt_rf = mkt_rf.rename(columns={'Mkt-RF':'mktrf', 'RF':'rf'}) #rename some columns
mkt_rf['month'] = mkt_rf.index.month #create a month column
mkt_rf['year'] = mkt_rf.index.year #create a year column
mkt_rf = mkt_rf.set_index(['year', 'month'])
mkt_rf.head()

ticker = input('Input the ticker of the stock: ')
share = get_data(ticker, start_date = '01/21/2016' , end_date = '12/31/2018', index_as_date=True)

share['index1'] = share.index
share['month'] = pd.DatetimeIndex(share['index1']).month #obtain the month
share['year'] = pd.DatetimeIndex(share['index1']).year #obtain the year

share_dict = {'open':'first','high':'max','low':'min','close': 'last','volume': 'sum','adjclose': 'last', 'month':'last', 'year': 'last'}
share.index = pd.to_datetime(share.index) #tells pandas that the index is a date
share = share.resample('M', how=share_dict) #take only monthly data as we specified above
share = share.set_index(['year', 'month'])

stock = share['adjclose']
stock_lag = stock.shift(1)
stock_lag.name = 'adjcloselag'
stock = pd.concat([stock, stock_lag], axis=1)
stock['return_stock'] = (stock['adjclose'] - stock['adjcloselag'])/stock['adjcloselag']
stock = (stock['return_stock']*100) #Put returns in same units as the returns in the market data file

returns = pd.concat([stock, mkt_rf], axis=1, sort=True) #concatenate the dataframes
returns['r_rf'] = returns['return_stock']-returns['rf']
returns.dropna(inplace=True)

result = sm.ols(formula="r_rf ~ mktrf", data = returns).fit()

beta = result.params.mktrf
print (result.summary())

ax = sns.regplot(x="mktrf", y= "r_rf", data=returns )
display(ax)
#ax.set(ylim=(0, 10))
#ax.set(xlim=(0, 10))