# 本脚本是针对全球各个国家历史发病数据的清洗工具
# 作者 https://github.com/tiffanyXiaoqing  mail: tiffany_xiqoing@foxmail.com
# 源数据来自 https://github.com/BlankerL/DXY-COVID-19-Data/blob/master/csv/DXYArea.csv
# 用户通过修改 inputfile 和  utputfile 定义源数据文件和输出文件

import pandas
from datetime import timedelta
from datetime import datetime

input_file = "testOut.csv"  # "nCov_world_0516.csv"
output_file = "testOut2.csv"

# 显示所有列
pandas.set_option('display.max_columns', None)
# 显示所有行
pandas.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pandas.set_option('max_colwidth', 200)

# ！！！ 根据需要选择合适的字符集
try:
    dataf = pandas.read_csv(input_file, encoding='UTF-8')
except:
    dataf = pandas.read_csv(input_file, encoding='gb2312')
#dataf = dataf[558:607]   #截取100行测试
dataf['日期'] = pandas.to_datetime(dataf['日期'], format='%Y-%m-%d')  # 1900 -> 2020

# 提取日期列表
df_t = dataf['日期']
df_date = df_t.drop_duplicates()  # 去重 这个返回Series对象
# 提取国家列表，包括中国和外国
df_c = dataf['国家']
df_country = df_c.drop_duplicates()  # 去重 这个返回Series对象

dataf.insert(loc=5, column='累计确诊', value=0)
dataf.insert(loc=5, column='现存确诊', value=0)  #现存确诊 = 累计确诊-累计治愈-累计死亡
dataf.insert(loc=6, column='累计治愈', value=0)
dataf.insert(loc=7, column='累计死亡', value=0)

NewList = []
for date_t in df_date:
    total_confirmedCount = 0
    total_curedCount = 0
    total_deadCount = 0
    for name in df_country:
        print(date_t.strftime('%Y-%m-%d') + name)  # 输出处理进度
        df2 = dataf.loc[(dataf['国家'] == name) & (dataf['日期'] == date_t), :]  # 通过索引标签来筛选数据
        if df2.empty:
            continue
        print(df2['确诊'].values)
        total_confirmedCount += df2['确诊'].values
        total_curedCount += df2['治愈'].values
        total_deadCount += df2['死亡'].values

    for name in df_country:
        df2 = dataf.loc[(dataf['国家'] == name) & (dataf['日期'] == date_t), :]  # 通过索引标签来筛选数据
        if df2.empty:
            continue
        new = pandas.DataFrame({'国家': name,
                                '确诊': df2['确诊'].values.astype(int),
                                '治愈': df2['治愈'].values.astype(int),
                                '死亡': df2['死亡'].values.astype(int),
                                '日期': date_t,
                                '累计确诊': total_confirmedCount.astype(int),
                                '现存确诊': (total_confirmedCount - total_curedCount - total_deadCount).astype(int),
                                '累计治愈': total_curedCount.astype(int),
                                '累计死亡': total_deadCount.astype(int)},
                               pandas.Index(range(1))
                               )
        NewList.append(new)

df = pandas.DataFrame(index=None) #最后的结果
df = df.append(NewList)

df.sort_values(['日期','确诊'], ascending = [False,False], inplace=True) #保证日期大且确认人数多的国家在前面
df.to_csv(output_file, encoding="utf_8_sig", index=False)  # 为保证excel打开兼容，输出为UTF8带签名格式
