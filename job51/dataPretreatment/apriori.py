import pymysql
import itertools
import pandas as pd
from job51.job51.settings import *


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
    cur.execute("select job_name,address,work_year,education from job51")
    resultList = cur.fetchall()
    return resultList


def load_data():
    result = []
    resultList = connectMysql()
    for res in resultList:
        result.append(list(res))
    return result


dataset = load_data()[:3000]
# for i in range(10):
#     print(i+1,dataset[i],sep="-》")
items = set(itertools.chain(*dataset))
# 用来保存字符串到编号的映射
str_to_index = {}
# 用来保存编号到字符串的映射
index_to_str = {}
for index, item in enumerate(items):
    str_to_index[item] = index
    index_to_str[index] = item
# print("字符串到编号：", list(str_to_index.items())[:5])
# print("编号到字符串：", list(index_to_str.items())[:5])
for i in range(len(dataset)):
    for j in range(len(dataset[i])):
        dataset[i][j] = str_to_index[dataset[i][j]]
for i in range(10):
    print(i + 1, dataset[i], sep="-》")


def buildC1(dataset):
    """
    :param dataset:
    创建并返回频繁项集
    :return:
    c1 : list
    频繁1项集列表
    """
    item1 = set(itertools.chain(*dataset))
    return [frozenset([i]) for i in item1]


c1 = buildC1(dataset)


def ck_to_lk(dataset, ck, min_support):

    """
    :param dataset: 数据集对象dataset
    :param ck: set/list
    所有候选k项集构成的set / list
    最小支持度。如果一个候选k项集的支持度大于等于最小支持度，则该候选k项集就是频繁k项集
    :return: lk：dict
    所有频繁k项集构成的字典。字典的key为频繁k项集，字典的value为频繁k项集对应的支持度
    """
    total = len(dataset)
    # 定义项集-频繁字典，用来存储每个项集的（key）与其对应的频数（value）
    support = {}
    for row in dataset:
        for item in ck:
            # 判断项集是否在记录（row）种出现
            if item.issubset(row):
                support[item] = support.get(item, 0) + 1
    return {k: v / total for k, v in support.items() if v / total >= min_support}


L1 = ck_to_lk(dataset, c1, 0.05)


def lk_to_ck(lk_list):
    ck = set()
    """
    根据频繁k项集，生成候选k+1项集
    :param lk_list: list
        所有频繁k项集构成的列表
    :return:
    ck : set
        返回所有候选k+1项集构成的set
    """
    # 保存所有组合之后的候选k+1项集
    li_size = len(lk_list)
    # 如果频繁k项集的数量小于1，则不可能通过组合生成候选k+1项集
    # 直接返回空set即可
    if li_size > 1:
        # 获取频繁k项集k的值
        k = len(lk_list[0])
        # 获取任意两个元素序号的索引组合
        for i, j in itertools.combinations(range(li_size), 2):
            t = lk_list[i] | lk_list[j]
            if len(t) == k + 1:
                ck.add(t)
    return ck


c2 = lk_to_ck(list(L1.keys()))

L2 = ck_to_lk(dataset, c2, 0.05)


# print("L2----------------",L2)


def get_L_all(dataset, min_support):
    c1 = buildC1(dataset)
    L1 = ck_to_lk(dataset, c1, min_support)
    # 定义字典，保存所有的频繁k项集
    L_all = L1
    Lk = L1
    # 当频繁项集中的元素（键值对）数量大于1时，才有可能生成候选k+1项集
    while len(Lk) > 1:
        lk_key_list = list(Lk.keys())
        # 由频繁k项集生成候选k+1项集
        ck = lk_to_ck(lk_key_list)
        # 由候选k+1项集生成频繁k+1项集
        Lk = ck_to_lk(dataset, ck, min_support)
        # 如果频繁k+1项字典不为空，则将所有频繁k+1项集加入到L_all中
        if len(Lk) > 0:
            L_all.update(Lk)
        else:
            break
    return L_all


L_all = get_L_all(dataset, 0.05)
# print("L_all---------------------", L_all)


def rules_from_item(item):
    left = []
    for i in range(1, len(item)):
        left.extend(itertools.combinations(item, i))
    return [(frozenset(le), frozenset(item.difference(le))) for le in left]


def rules_from_L_all(L_all, min_confidence):
    """
    :param L_all: dict
        所有频繁项集
    :param min_confidence: float
        最小置信度。当关联规则置信度大于等于最小置信度时，保留关联规则
    :return:
    result: 所有满足最小置信度的关联规则
    """
    rules = []
    for Lk in L_all:
        if len(Lk) > 1:
            rules.extend(rules_from_item(Lk))
    result = []
    for left, right in rules:
        support = L_all[left | right]
        confidence = support / L_all[left]
        lift = confidence / L_all[right]
        if confidence >= min_confidence:
            result.append({"左侧": left, "": right, "支持度": support, "置信度": confidence, "提升度": lift})

    return result


def Apriori(dataset, min_support, min_confidence):
    L_all = get_L_all(dataset, min_support)
    rules = rules_from_L_all(L_all, min_confidence)
    return rules


rules = Apriori(dataset, 0.05, 0.3)
print(rules)

def Apriori_change(item):
    li = list(item)
    for i in range(len(li)):
        if not li[i] is None:
            li[i] = index_to_str[li[i]]
    return li


df = pd.DataFrame(rules)

df = df.reindex(["左侧", "右侧", "支持度", "置信度", "提升度"], axis=1)
df["右侧"] = df["左侧"].apply(Apriori_change)
# df["左侧"] = df["右侧"].apply(Apriori_change)
print(df)
