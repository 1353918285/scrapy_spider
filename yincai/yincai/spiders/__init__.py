# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

def transform(str):
    id = ''.join(str).strip()
    return id
t = transform(['\n            \n        Software Engineer Intern\n      \n          '])
print(t)

