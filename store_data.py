import pandas as pd
import numpy as np
import pandas_datareader as pdr
import twstock
from sqlalchemy import create_engine
import mysql.connector

# 刪除資料表
mydb = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'alex50703',
    database = 'stockdash'
)
mycursor = mydb.cursor()

table_list = ['stock_trend','stock_ma_slope','stock_roi']
try:
    for table in table_list:
        mycursor.execute(
            f''' drop table {table}'''
        )

except:
    pass

print('資料庫重製')

# 獲取上市股票資訊
tickers = twstock.twse
df_tickers = pd.DataFrame(tickers).T
collect_df = df_tickers[df_tickers[0]=='股票'][[1,2,5,6]]
collect_df.columns = ['stock_id','stock_name','market','group']

engine = create_engine("mysql+pymysql://root:alex50703@127.0.0.1:3306/stockdash?charset=utf8mb4")

# 股市漲跌級均線計算/40m

count = 0
for stock_id, stock_name in zip(collect_df.stock_id,collect_df.stock_name):
    count += 1
    if count % 50 == 0:
        print(f'目前進度：{count}/931')
    try:
        df = pdr.DataReader(f'{stock_id}.TW', 'yahoo', start='2020/01/01')
        df = df.drop('Adj Close',axis=1)
        df = df.apply(lambda x: round(x, 2))
        df['Volume'] = round(df['Volume']/1000).astype('int')
        df['stock_id'] = stock_id
        df['stock_name'] = stock_name

        # 均線計算
        df['5ma'] = round(df['Close'].rolling(5).mean(),2)
        df['10ma'] = round(df['Close'].rolling(10).mean(),2)
        df['20ma'] = round(df['Close'].rolling(20).mean(),2)
        df['60ma'] = round(df['Close'].rolling(60).mean(),2)
        df['100ma'] = round(df['Close'].rolling(100).mean(),2)

        # 布林通道
        std_5 = df['Close'].rolling(5).std()
        df['upper_band_5'] = round(df['5ma']+2*std_5,2)
        df['lower_band_5'] = round(df['5ma']-2*std_5,2)
        std_10 = df['Close'].rolling(10).std()
        df['upper_band_10'] = round(df['10ma']+2*std_10,2)
        df['lower_band_10'] = round(df['10ma']-2*std_10,2)
        std_20 = df['Close'].rolling(20).std()
        df['upper_band_20'] = round(df['20ma']+2*std_20,2)
        df['lower_band_20'] = round(df['20ma']-2*std_20,2)
        
        # 存入資料庫
        df.to_sql('stock_trend',con=engine,if_exists='append')
        print(f'{stock_id}{stock_name} 以儲存')
    except:
        print(f'{stock_id}{stock_name} 儲存失敗')
        pass

print('*'*10,'資料儲存完成','*'*10)

stock_trend = pd.read_sql('stock_trend',engine)

    # 斜率
def slope_(x,y):
    
    slope, intercept = np.polyfit(x,y,1)
    slope = round(slope,3)

    return slope

# 變數計算
def variable_calculate(df):

    df = df.sort_values(by='Date')
    data = {'5ma_slope_5': slope_(range(5), (df['5ma'][-5:]/df['5ma'][-5:].sum())*100),    # 均線斜率
            '10ma_slope_5': slope_(range(5), (df['10ma'][-5:]/df['10ma'][-5:].sum())*100),
            '20ma_slope_5': slope_(range(5), (df['20ma'][-5:]/df['20ma'][-5:].sum())*100),
            '60ma_slope_5': slope_(range(5), (df['60ma'][-5:]/df['60ma'][-5:].sum())*100),
            }

    result = pd.DataFrame(data,index=[0])
    result['stock_id'] = df.stock_id.unique()[0]
    result['stock_name'] = df.stock_name.unique()[0]
    result['volume'] = df.Volume.iloc[-1]

    return result

# 均線斜率計算
for stock_id in collect_df.stock_id:
    try:
        data = stock_trend.query(f"stock_id == '{stock_id}'")
        data = data.sort_values(by='Date')
        data = variable_calculate(data)
        data['group'] = collect_df.query(f"stock_id == '{stock_id}'").group.values[0]
        
        # 存入資料庫
        data.to_sql('stock_ma_slope',con=engine,if_exists='append')
    
    except:
        pass

print('*'*10,'斜率資料儲存完成','*'*10)

# 報酬率計算
stock_name = []
stock_id_ = []
group = []
volume = []
close = []
roi_1 = []
roi_5 = []
roi_10 = []
roi_20 = []
roi_60 = []
for stock_id in collect_df.stock_id:
    try:
        data = stock_trend.query(f"stock_id == '{stock_id}'",engine='python').sort_values(by='Date') 
        roi_1.append(round((((data['Close'].iloc[-1])-(data['Close'].iloc[-2]))/(data['Close'].iloc[-2]))*100,2))
        roi_5.append(round((((data['Close'].iloc[-1])-(data['Close'].iloc[-6]))/(data['Close'].iloc[-6]))*100,2))
        roi_10.append(round((((data['Close'].iloc[-1])-(data['Close'].iloc[-11]))/(data['Close'].iloc[-11]))*100,2))
        roi_20.append(round((((data['Close'].iloc[-1])-(data['Close'].iloc[-21]))/(data['Close'].iloc[-21]))*100,2))
        roi_60.append(round((((data['Close'].iloc[-1])-(data['Close'].iloc[-61]))/(data['Close'].iloc[-61]))*100,2))
        stock_name.append(data['stock_name'].iloc[0])
        stock_id_.append(data['stock_id'].iloc[0])
        group.append(collect_df.query(f"stock_id == '{stock_id}'").group.values[0])
        volume.append(data['Volume'].iloc[-1])
        close.append(data['Close'].iloc[-1])
    except:
        pass 

data = pd.DataFrame({'stock_name':stock_name,
                'stock_id':stock_id_,
                'group':group,
                'volume':volume,
                'close':close,
                'roi_1':roi_1,
                'roi_5':roi_5,
                'roi_10':roi_10,
                'roi_20':roi_20,
                'roi_60':roi_60,
                })
data['state_1'] = np.where(data.roi_1>=0,'up','down')   # range=[10, -10], nbins=None
data['state_5'] = np.where(data.roi_5>=0,'up','down')   # range=[20,-20], nbins=None
data['state_10'] = np.where(data.roi_10>=0,'up','down') # range=[30,-30], nbins=None
data['state_20'] = np.where(data.roi_20>=0,'up','down') # range=[40,-40], nbins=None
data['state_60'] = np.where(data.roi_60>=0,'up','down') # range=[100,-100], nbins=None

data.to_sql('stock_roi',con=engine,if_exists='append')

print('*'*10,'報酬率資料儲存完成','*'*10)
print('資料庫更新完成')