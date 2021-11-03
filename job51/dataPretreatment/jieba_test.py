import sys
sys.path.append("../")
import jieba
jieba.load_userdict("../jieba/customWords.txt")
import jieba.posseg as pseg

jieba.add_word('石墨烯')
jieba.add_word('凱特琳')
jieba.del_word('自定义词')
jieba.suggest_freq('.net',True)
test_sent = (
"Sql Java Java Java Java Java Java Java Springboot Spring Cloud Spring Springmvc Mybatis Linux Unix\n"
"Tomcat Mysql Orcale 数据库 Sql 数据库 Javascript\n"
"Javascript Html Jquery Css Vue 分布式 架构设计。"
)
words = jieba.cut(test_sent)
print('/'.join(words))

print("="*40)

result = pseg.cut(test_sent)

for w in result:
    print(w.word, "/", w.flag, ", ", end=' ')
s = '.net工程师asdsa,Python mysql djangoflaskdockerpostgresqlodoo'
sent = jieba.lcut(s)
for s in sent:
   print(s.strip().capitalize())