#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd


def loadDataSet():
    # 读取csv文件数据
    money_report = pd.read_csv("../static/data/money_report_train_sum.csv")
    year_report = pd.read_csv("../static/data/year_report_train_sum.csv")
    # 处理数据，把相同ID数据进行合并
    money = money_report.loc[:, ['ID', 'year', '债权融资额度', '债权融资成本', '股权融资额度',
                                 '股权融资成本', '内部融资和贸易融资额度', '内部融资和贸易融资成本',
                                 '项目融资和政策融资额度', '项目融资和政策融资成本']]
    # money.to_csv("../static/data/result.csv")
    # print(money.loc[:,'ID'])
    df = pd.DataFrame()
    dfIndex = 0
    indexDict = dict()
    for data in money.itertuples():
        dictIndex = getattr(data, 'ID')
        index = getattr(data, 'Index')
        if (indexDict.__contains__(dictIndex) == False):
            indexDict[dictIndex] = dfIndex
            df.loc[dfIndex] = money.loc[index]
        else:
            df.assign()


# 处理'year' label
def repairYear(year):
    year_report = pd.read_csv(year)  # 读取csv数据
    indexDict = dict()  # 创建一个空字典，用来存放ID对应的各年份和index
    for index, rows in year_report.iterrows():
        dictIndex = rows['ID']
        if (indexDict.__contains__(dictIndex) == False):  # 判断ID是否已经存在，不存在则创建一个数据，存放list，
            # list中的元素为数组，每个数组格式为[year,index]
            indexDict[dictIndex] = list()
            value = [rows['year'], index]
            indexDict[dictIndex].append(value)
        else:  # ID在字典dictIndex中已存在，则加入年份及其Index
            value = [rows['year'], index]
            indexDict[dictIndex].append(value)

    # 把对应年份添加上
    for key, values in indexDict.items():
        if (pd.isna(values[0][0])):  # 如果存放的第一个为nan值，赋值为2015，下同
            year_report.loc[values[0][1], 'year'] = 2015.0
        if (pd.isna(values[1][0])):
            year_report.loc[values[1][1], 'year'] = 2016.0
        if (pd.isna(values[2][0])):
            year_report.loc[values[2][1], 'year'] = 2017.0
    year_report.to_csv(year, index=False)  # 写回原文件


# year = "../static/data/money_report_train_sum.csv"
# repairYear(year)

# 合并各种融资额度和成本为融资额度 融资成本两个label
def mergeFinancing(money):
    money_report = pd.read_csv(money)
    money_report = money_report.fillna(0)

    base = pd.read_csv("../static/data/base_verify1.csv")
    base = base.loc[:, ['ID', 'flag']]

    indexDict = dict()  # 创建一个空字典，用来存放ID对应的各年份和index
    for index, rows in money_report.iterrows():
        dictIndex = rows['ID']
        if (indexDict.__contains__(dictIndex) == False):  # 判断ID是否已经存在，不存在则创建一个数据，存放list，
            # list中的元素为数组，每个数组格式为[year,index]
            indexDict[dictIndex] = list()
            value = [rows['year'], index]
            indexDict[dictIndex].append(value)
        else:  # ID在字典dictIndex中已存在，则加入年份及其Index
            value = [rows['year'], index]
            indexDict[dictIndex].append(value)

    money_report['融资额度'] = money_report.apply(lambda x: x['债权融资额度']
                                                        + x['股权融资额度'] + x['内部融资和贸易融资额度']
                                                        + x['项目融资和政策融资额度'], axis=1)
    money_report['融资成本'] = money_report.apply(lambda x: x['债权融资成本']
                                                        + x['股权融资成本'] + x['内部融资和贸易融资成本']
                                                        + x['项目融资和政策融资成本'], axis=1)
    new_money_report = money_report.loc[:, ['ID', 'year', '融资额度', '融资成本']]
    # new_money_report.to_csv(money, index=False)
    #创建新列，将各年份数据放到同意ID行里，保存到csv文件中
    i = 0
    for key, values in indexDict.items():
        base.loc[i, '2015融资额度'] = new_money_report.loc[values[0][1], '融资额度']
        base.loc[i, '2015融资成本'] = new_money_report.loc[values[0][1], '融资成本']
        base.loc[i, '2016融资额度'] = new_money_report.loc[values[1][1], '融资额度']
        base.loc[i, '2016融资成本'] = new_money_report.loc[values[1][1], '融资成本']
        base.loc[i, '2017融资额度'] = new_money_report.loc[values[2][1], '融资额度']
        base.loc[i, '2017融资成本'] = new_money_report.loc[values[2][1], '融资成本']
        i += 1
    base.to_csv("../static/data/base_verify_result.csv", index=False)

# money = "../static/data/money_information_verify1.csv"
# mergeFinancing(money)

