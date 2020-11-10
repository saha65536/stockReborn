# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 18:26:28 2020

@author: saha
"""


import os
import pandas as pd# 导入DataFrame数据
import baostock as bs


class StockBase:
    
    def __init__(self,beg_date,end_date,anaMonth,checkMonth): 
        self.beg_date = beg_date
        self.end_date = end_date
        self.anaMonth = anaMonth
        self.checkMonth = checkMonth             
        #### 登陆系统 ####
        lg = bs.login()
        # 显示登陆返回信息
        print('login respond error_code:'+lg.error_code)
        print('login respond  error_msg:'+lg.error_msg) 
        self.getList()  
        self.getStocks()        
        
    def getList(self):
        stocks = []
    
        # 获取中证500成分股
        rs = bs.query_zz500_stocks()
        print('query_zz500 error_code:'+rs.error_code)
        print('query_zz500  error_msg:'+rs.error_msg)    
        
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            stocks.append(rs.get_row_data())
            
        # 获取中证500成分股
        rs = bs.query_hs300_stocks()
        print('query_hs300 error_code:'+rs.error_code)
        print('query_hs300  error_msg:'+rs.error_msg)    
        
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            stocks.append(rs.get_row_data())
            
        result = pd.DataFrame(stocks, columns=rs.fields)
        # 结果集输出到csv文件
        
        self.makeDIR('./data')
        result.to_csv('data/'+ 'stockList.csv', index=False) 
        
    def makeDIR(self,dirName):
        if not os.path.exists(dirName):
            os.mkdir(dirName)
        
    #获取list中每个股票数据
    def getStocks(self):
        dfall = pd.read_csv('data/'+ 'stockList.csv')
        for i in range(0,len(dfall)):
            print('begin read :' + str(i) + ' '+ dfall.iloc[i]['code']+ ' '+ dfall.iloc[i]['code_name'])
            self.read_onestock(dfall.iloc[i]['code'])
            
    #读取一只股票的数据    
    def read_onestock(self,stock_code):    
        
        if os.path.isfile('data/'+ stock_code + '.csv'):
            return
        
        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        rs = bs.query_history_k_data_plus(stock_code,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            start_date=self.beg_date, end_date=self.end_date,
            frequency="d", adjustflag="2")
        
        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
        
        #### 结果集输出到csv文件 ####   
        result.to_csv('data/'+ stock_code + '.csv', index=False)  
       
                    
    def queryInfo(self,stock_code,paramName):
        profit_list = []
        rs_profit = bs.query_profit_data(stock_code,year=2020, quarter=2)
        while (rs_profit.error_code == '0') & rs_profit.next():
            profit_list.append(rs_profit.get_row_data())
        
        result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
        paramV = result_profit[paramName]
        return float(paramV)
    
    def exportFile(self,df,name):
        self.makeDIR('./result')        
        df.to_csv('result/result_'  + name + '.csv' ,index=False,sep=',') 
                    
