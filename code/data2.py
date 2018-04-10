# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import operator
import matplotlib.pyplot as plt
import statsmodels.api as sm


# 标称属性
attribute = ['Permit Type', 'Block', 'Lot', 'Street Number', 'Street Number Suffix', 'Street Name', 'Street Suffix', 
              'Current Status', 'Structural Notification', 'Voluntary Soft-Story Retrofit', 'Fire Only Permit',  
              'Existing Use', 'Proposed Use', 'Plansets', 'TIDF Compliance', 'Existing Construction Type', 
              'Proposed Construction Type', 'Site Permit', 'Supervisor District', 'Neighborhoods - Analysis Boundaries',
              'Number of Existing Stories', 'Number of Proposed Stories', 'Estimated Cost', 'Revised Cost', 'Existing Units', 
              'Proposed Units']

name_category = ['Permit Type', 'Block', 'Lot', 'Street Number', 'Street Number Suffix', 'Street Name', 'Street Suffix', 
              'Current Status', 'Structural Notification', 'Voluntary Soft-Story Retrofit', 'Fire Only Permit',  
              'Existing Use', 'Proposed Use', 'Plansets', 'TIDF Compliance', 'Existing Construction Type', 
              'Proposed Construction Type', 'Site Permit', 'Supervisor District', 'Neighborhoods - Analysis Boundaries']
# 数值属性
name_value = ['Number of Existing Stories', 'Number of Proposed Stories', 'Estimated Cost', 'Revised Cost', 
                 'Existing Units', 'Proposed Units']


#======================================================读取数据===========================================================
data_origin = pd.read_csv("Building_Permits.csv",na_values = "?")


#======================================================数据摘要===========================================================

# -----------------------------------------------------标称属性-----------------------------------------------------------
# 使用value_counts函数统计每个标称属性的取值频数
for item in name_category:
    
    print (item, '频数：\n', pd.value_counts(data_origin[item].values), '\n')

# -----------------------------------------------------数值属性-----------------------------------------------------------
    
# 最大值
data_show = pd.DataFrame(data = data_origin[name_value].max(), columns = ['max'])
# 最小值
data_show['min'] = data_origin[name_value].min()
# 均值
data_show['mean'] = data_origin[name_value].mean()
# 中位数
data_show['median'] = data_origin[name_value].median()
# 四分位数
data_show['quartile'] = data_origin[name_value].describe().loc['25%']
# 缺失值个数
data_show['missing'] = data_origin[name_value].describe().loc['count'].apply(lambda x : 368-x)

print(data_show)


#======================================================数据可视化===========================================================

# -----------------------------------------------------直方图-----------------------------------------------------------
fig = plt.figure(figsize = (20,20))
i = 1
for item in name_value:
    ax = fig.add_subplot(2, 4, i)
    data_origin[item].plot(kind = 'hist', title = item, ax = ax)
    i += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
fig.savefig('histogram.jpg')

# -----------------------------------------------------QQ图-----------------------------------------------------------
fig = plt.figure(figsize = (20,20))
i = 1
for item in name_value:
    ax = fig.add_subplot(2, 4, i)
    sm.qqplot(data_origin[item], ax = ax)
    ax.set_title(item)
    i += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
fig.savefig('qqplot.jpg')

# -----------------------------------------------------盒图-----------------------------------------------------------
fig = plt.figure(figsize = (20,20))
i = 1
for item in name_value:
    ax = fig.add_subplot(2, 4, i)
    data_origin[item].plot(kind = 'box')
    i += 1
fig.savefig('boxplot.jpg')

#======================================================缺失数据处理===========================================================
#======================================================剔除===========================================================

# 将缺失值对应的数据整条剔除，生成新数据集
data_filtrated = data_origin.dropna()
# 绘制可视化图
fig = plt.figure(figsize = (20,20))
i = 1
# 对标称属性，绘制折线图
for item in name_category:
    ax = fig.add_subplot(5, 5, i)
    ax.set_title(item)
    pd.value_counts(data_origin[item].values).plot(ax = ax, marker = '^', label = 'origin', legend = True)
    pd.value_counts(data_filtrated[item].values).plot(ax = ax, marker = 'o', label = 'filtrated', legend = True)
    i += 1
 
   
i = 19
# 对数值属性，绘制直方图
for item in name_value:
    ax = fig.add_subplot(5, 5, i)
    ax.set_title(item)
    data_origin[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'origin', legend = True)
    data_filtrated[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'filtrated', legend = True)
    ax.axvline(data_origin[item].mean(), color = 'r')
    ax.axvline(data_filtrated[item].mean(), color = 'b')
    i += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)

# 保存图像和处理后数据
fig.savefig('missing_data_delete.jpg')
data_filtrated.to_csv('missing_data_delete.csv', mode = 'w', encoding='utf-8', index = False,header = False)

#======================================================最高频替代===========================================================

# 建立原始数据的拷贝
data_filtrated = data_origin.copy()
# 对每一列数据，分别进行处理
for item in attribute:
    # 计算最高频率的值
    most_frequent_value = data_filtrated[item].value_counts().idxmax()
    # 替换缺失值
    data_filtrated[item].fillna(value = most_frequent_value, inplace = True)

    # 绘制可视化图
fig = plt.figure(figsize = (20,20))

i = 1
# 对标称属性，绘制折线图
for item in name_category:
    ax = fig.add_subplot(5, 5, i)
    ax.set_title(item)
    pd.value_counts(data_origin[item].values).plot(ax = ax, marker = '^', label = 'origin', legend = True)
    pd.value_counts(data_filtrated[item].values).plot(ax = ax, marker = 'o', label = 'filtrated', legend = True)
    i += 1    

i = 19
# 对数值属性，绘制直方图
for item in name_value:
    ax = fig.add_subplot(5, 5, i)
    ax.set_title(item)
    data_origin[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'origin', legend = True)
    data_filtrated[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'droped', legend = True)
    ax.axvline(data_origin[item].mean(), color = 'r')
    ax.axvline(data_filtrated[item].mean(), color = 'b')
    i += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)

# 保存图像和处理后数据
fig.savefig('missing_data_most.jpg')
data_filtrated.to_csv('missing_data_most.csv', mode = 'w', encoding='utf-8', index = False,header = False)


#======================================================属性间相关关系===========================================================

# 使用pandas中Series的***interpolate()***函数，对数值属性进行插值计算，并替换缺失值。

# 建立原始数据的拷贝
data_filtrated = data_origin.copy()
# 对数值型属性的每一列，进行插值运算
for item in name_value:
    data_filtrated[item].interpolate(inplace = True)

    # 绘制可视化图
fig = plt.figure(figsize = (20,20))

i = 1
# 对标称属性，绘制折线图
for item in name_category:
    ax = fig.add_subplot(5, 5, i)
    ax.set_title(item)
    pd.value_counts(data_origin[item].values).plot(ax = ax, marker = '^', label = 'origin', legend = True)
    pd.value_counts(data_filtrated[item].values).plot(ax = ax, marker = 'o', label = 'filtrated', legend = True)
    i += 1   
    
i = 19
# 对数值属性，绘制直方图
for item in name_value:
    ax = fig.add_subplot(5, 5, i)
    ax.set_title(item)
    data_origin[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'origin', legend = True)
    data_filtrated[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'droped', legend = True)
    ax.axvline(data_origin[item].mean(), color = 'r')
    ax.axvline(data_filtrated[item].mean(), color = 'b')
    i += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)

# 保存图像和处理后数据
fig.savefig('missing_data_corelation.jpg')
data_filtrated.to_csv('missing_data_corelation.csv', mode = 'w', encoding='utf-8', index = False,header = False)

