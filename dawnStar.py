# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 18:42:09 2020

@author: saha
"""

from stockBase import StockBase
import pandas as pd# 导入DataFrame数据

class DawnStar:#黎明之星形态
    def __init__(self):   
        self.insStockBase = StockBase('2020-09-01','2020-10-31','2020-09','2020-10')
        self.arr_codes = []
        self.arr_names = []
        self.arr_dates = []
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
        
        for p in range(1,len(df)-2):
            if df.iloc[p]['Open'] < df.iloc[p]['Close'] :
                continue
            m = p + 1
            n = p + 2
            if df.iloc[m]['High'] > df.iloc[p]['High']:
                continue
            if df.iloc[m]['Open'] != df.iloc[m]['Close'] and (min(df.iloc[m]['Open'],df.iloc[m]['Close']) - df.iloc[m]['Low']) / abs(df.iloc[m]['Open'] - df.iloc[m]['Close']) < 2:
                continue
            if (min(df.iloc[m]['Open'],df.iloc[m]['Close']) - df.iloc[m]['Low'])/df.iloc[m]['Close']<0.03:
                continue
            if df.iloc[n]['Open'] > df.iloc[n]['Close']:
                continue
            if df.iloc[n]['Close'] < df.iloc[p]['High']:
                continue
            self.arr_codes.append(stock_code)   
            self.arr_names.append(stock_name)
            self.arr_dates.append(df.iloc[p]['od'])
            break
        
    #输出分析结果
    def exportAnaResult(self):
        df = pd.DataFrame({'code':self.arr_codes,'name':self.arr_names,'date':self.arr_dates})

        self.insStockBase.exportFile(df)      
        
        
if __name__ == '__main__':
    DawnStar()
