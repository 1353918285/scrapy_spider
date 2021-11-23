import pymysql
import jieba
from job51.job51.settings import *

def connectMysql(sql):
    #连接数据库
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PWD,
        db=MYSQL_DB,
        charset=MYSQL_CHARSET
    )
    #创建游标，执行sql语句
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    resultList = cur.fetchall()
    cur.close()
    conn.close()
    return resultList

def job_count():
    connectMysql("truncate table job_count")
    # 转换词
    synonymWords = {'自然语言': "Nlp", 'Ai': '人工智能', 'Boot': 'Springboot', 'Node': 'Nodejs', 'Web': '前端开发','Web前端开发': '前端开发', '安卓': 'Android',
                    '嵌入式':'嵌入式软件','Net': '.net', 'Js':'Javascript'
                    }
    keys = list(synonymWords.keys())
    #加载停用词文件
    stopwords = open('../jieba/stopWords.txt', encoding='utf-8').read()
    #添加不被分词的单词
    jieba.load_userdict("../jieba/customWords.txt")
    words = []
    for res in connectMysql("select job_name from job51"):
        k,=res
        wordList = jieba.lcut(k)
        for word in wordList:
            word = word.strip().capitalize()
            if word not in stopwords:
                if word in keys:
                    word = synonymWords[word]
                    words.append(word)
                else:
                    words.append(word)
    wordcount = {}
    for word in words:
        wordcount[word] = wordcount.get(word, 0)+1
    #对单词进行词频统计，输出词频最多的10
    word_sort = sorted(wordcount.items(), key=lambda x: x[1], reverse=True)[:15]
    print(word_sort)
    for word in word_sort:
        sql = "insert into job_count (job_name,j_count) values {} ".format(word)
        print(sql)
        connectMysql(sql)

if __name__ == '__main__':
    job_count()









