from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import pymysql
import pandas as pd
from job51.job51.settings import *

"""
    使用 apriori 计算频繁项集
"""
def connectMysql():
    # 连接数据库
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PWD,
        db=MYSQL_DB,
        charset=MYSQL_CHARSET
    )
    # 创建游标，执行sql语句
    cur = conn.cursor()
    cur.execute('SELECT job_name,salary,address,work_year,education FROM job51')
    resultList = cur.fetchall()
    return resultList


def load_data():
    result = []
    resultList = connectMysql()
    for res in resultList:
        result.append(list(res))
    return result


dataset = load_data()[:10000]
item_df = pd.DataFrame(dataset)
te = TransactionEncoder()
df_tf = te.fit_transform(dataset)
df = pd.DataFrame(df_tf,columns=te.columns_)
frequent_itemsets = apriori(df, min_support=0.01, use_colnames=True)
frequent_itemsets.sort_values(by='support', ascending=False, inplace=True)
print(frequent_itemsets[frequent_itemsets.itemsets.apply(lambda x: len(x)) == 2])
# metric可以有很多的度量选项，返回的表列名都可以作为参数
association_rule = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.9)
# 关联规则可以提升度排序
association_rule.sort_values(by='lift', ascending=False, inplace=True)

print(association_rule)
# 规则是：antecedents->consequents
