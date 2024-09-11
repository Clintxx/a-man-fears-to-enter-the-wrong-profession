import pandas as pd

df = pd.read_excel('./job_data.xlsx')

# 1. 将 '工作城市' 列中的每行城市按照逗号 '、' 拆分成列表
df['工作城市'] = df['工作城市'].str.split('、')

# 2. 使用 explode 将城市列表展开为单独的行
df_exploded = df.explode('工作城市')

# 3. 去除工作城市列中的前后空格
df_exploded['工作城市'] = df_exploded['工作城市'].str.strip()

# 4. 清除 '工作城市：' 前缀
df_exploded['工作城市'] = df_exploded['工作城市'].str.replace('工作城市：', '', regex=False)

# 5. 过滤掉空字符串或空白城市
df_cleaned = df_exploded[df_exploded['工作城市'] != '']

# 6. 统计每个城市出现的次数
city_counts = df_cleaned['工作城市'].value_counts()

# 7. 清除 city_counts 中索引为空白或仅包含空格的城市
city_counts.index = city_counts.index.astype(str)  # 确保索引为字符串类型
city_counts_cleaned = city_counts[city_counts.index.str.strip() != '']  # 过滤空白城市

# 8. 保存统计结果到 Excel 文件
city_counts_cleaned.to_excel('./city_counts_cleaned.xlsx')

# 打印前10个城市的出现次数
print(city_counts_cleaned.nlargest(10))
