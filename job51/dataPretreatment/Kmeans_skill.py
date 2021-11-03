import time
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MiniBatchKMeans
import pymysql


# 读取Mysql数据库
def get_dbdata():
    conn_read = pymysql.connect("localhost", "root", "123456", "zhaopin", charset="utf8mb4")
    dataset = []
    sql = "select job_name from job51"
    cursor = conn_read.cursor()
    cursor.execute(sql)
    data_count = 0
    for line in cursor:
        data_count += 1
        dataset.append(line[0])
    cursor.close()
    conn_read.close()
    print(dataset)
    return dataset


def transform(dataset, n_features=200):
    vectorizer = TfidfVectorizer(max_df=0.5, max_features=n_features, min_df=2, use_idf=True)
    X = vectorizer.fit_transform(dataset)
    return X, vectorizer


def train(X, vectorizer, true_k=6, minibatch=False, showLable=False):
    # 使用采样数据还是原始数据训练k-means，
    if minibatch:
        km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=1,
                             init_size=1000, batch_size=300, verbose=False)
    else:
        km = KMeans(n_clusters=true_k, init='k-means++', max_iter=300, n_init=1,
                    verbose=False)
    km.fit(X)
    if showLable:
        print("Top terms per cluster:")
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()
        print(vectorizer.get_stop_words())
        for i in range(true_k):
            print("Cluster %d:" % i, end='')
            for ind in order_centroids[i, :10]:
                print(' %s' % terms[ind], end='')
            print()
    result = list(km.predict(X))
    print('Cluster distribution:')
    print(dict([(i, result.count(i)) for i in result]))
    return -km.score(X)


# 指定簇的个数k
def k_determin():
    '''测试选择最优参数'''
    dataset = get_dbdata()
    print("%d documents" % len(dataset))
    X, vectorizer = transform(dataset, n_features=500)
    true_ks = []
    scores = []
    # 中心点的个数从3到200(根据自己的数据量改写)
    for i in range(3, 100, 1):
        score = train(X, vectorizer, true_k=i) / len(dataset)
        print(i, score)
        true_ks.append(i)
        scores.append(score)
    plt.figure(figsize=(8, 4))
    plt.plot(true_ks, scores, label="error", color="red", linewidth=1)
    plt.xlabel("n_features")
    plt.ylabel("error")
    plt.legend()
    plt.show()


def main():
    '''在最优参数下输出聚类结果'''
    dataset = get_dbdata()
    X, vectorizer = transform(dataset, n_features=500)
    score = train(X, vectorizer, true_k=6, showLable=True) / len(dataset)
    print(score)


if __name__ == '__main__':
    start = time.time()
    k_determin()#先确定k值
    main()
    end = time.time()
    print('程序运行时间', end - start)
