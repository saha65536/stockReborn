# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 18:42:09 2020

@author: saha
"""

from stockBase import StockBase
import pandas as pd# 导入DataFrame数据

class DawnStar:#黎明之星形态
    def __init__(self):   
        self.insStockBase = StockBase('2019-01-01','2019-12-31','2020-09','2020-10')
        self.arr_codes = []
        self.arr_names = []
        self.arr_dates = []
        self.arr_profits = []
        self.analyse()
        
    #模型分析
    def analyse(self):
        dfall = pd.read_csv('data/'+ 'stockList.csv')
        for i in range(0,len(dfall)):
            print('begin Analyse :' + str(i) + ' '+ dfall.iloc[i]['code']+ ' '+ dfall.iloc[i]['code_name'])
            self.modelAnalyse(dfall.iloc[i]['code'],dfall.iloc[i]['code_name'])
            
        self.exportAnaResult()
        
    #分析每一只股票
    def modelAnalyse(self,stock_code,stock_name):
    	# 导入股票数据
        df = pd.read_csv('data/'+ stock_code + '.csv')
        # 格式化列名，用于之后的绘制
        df.rename(
                columns={
                'date': 'od', 'open': 'Open', 
                'high': 'High', 'low': 'Low', 
                'close': 'Close', 'volume': 'Volume'}, 
                inplace=True)
        # 转换为日期格式
        df['Date'] = pd.to_datetime(df['od'])
        # 将日期列作为行索引
        df.set_index(['Date'], inplace=True)
        
        bFind = False
        bIndex = 1
        for p in range(1,len(df)-2):
            #第一天收盘要跌
            if df.iloc[p]['Open'] < df.iloc[p]['Close'] :
                continue
            m = p + 1
            n = p + 2
            #中间这天的最高价不能高于第一天的最高价
            if df.iloc[m]['High'] > df.iloc[p]['High']:
                continue
            #中间这天的下影线是实体柱的两倍以上
            if df.iloc[m]['Open'] != df.iloc[m]['Close'] and (min(df.iloc[m]['Open'],df.iloc[m]['Close']) - df.iloc[m]['Low']) / abs(df.iloc[m]['Open'] - df.iloc[m]['Close']) < 2:
                continue
            #中间这天最低价要比收盘价跌超过3%
            if (min(df.iloc[m]['Open'],df.iloc[m]['Close']) - df.iloc[m]['Low'])/df.iloc[m]['Close']<0.03:
                continue
            #最后这天必须是阳线
            if df.iloc[n]['Open'] > df.iloc[n]['Close']:
                continue
            #最后这天收盘价必须比第一天的最高点高
            if df.iloc[n]['Close'] < df.iloc[p]['High']:
                continue
            #最后这天的量必须大于前两天
            if df.iloc[n]['Volume'] < df.iloc[p]['Volume'] or df.iloc[n]['Volume'] < df.iloc[m]['Volume']:
                continue    
            if df.iloc[n]['Volume'] < df.iloc[p]['Volume']*1.5:
                continue  
            #如果最后这天的量均大于第一天和第二天的3倍以上，则最后一天不能有上影线
            if df.iloc[n]['Volume'] > 3*df.iloc[p]['Volume'] and df.iloc[n]['Volume'] > 3*df.iloc[m]['Volume'] and df.iloc[n]['High'] != df.iloc[n]['Close']:
                continue
            self.arr_codes.append(stock_code)   
            self.arr_names.append(stock_name)
            self.arr_dates.append(df.iloc[p]['od'])
            bFind = True
            bIndex = p + 3
            break
        
        if bFind:
            profit = 0
            buyPrice =  df.iloc[bIndex]['Open']
            for i in range(bIndex + 1,bIndex+10):
                if df.iloc[i]['High'] / buyPrice > 1.03:
                    profit = 1.03
                    break
            if 0 == profit:
                profit = df.iloc[i]['Close'] / buyPrice    
            
            self.arr_profits.append(profit)
                    
        
    #输出分析结果
    def exportAnaResult(self):
        df = pd.DataFrame({'code':self.arr_codes,'name':self.arr_names,'date':self.arr_dates,'profit':self.arr_profits})

        self.insStockBase.exportFile(df,'dawnStar')    
                  
        
        
if __name__ == '__main__':
    DawnStar()
