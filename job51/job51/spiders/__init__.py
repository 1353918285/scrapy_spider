# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

def salary_range(s):
    if 0 < s and s <= 5000:
        salary = '0-5k'
        return salary
    if 5000< s and s <= 10000:
        salary = '5-10k'
        return salary
    if 10000< s and s<= 15000:
        salary = '10k-15k'
        return salary
    if 15000 < s and s <= 20000:
        salary = '15k-20k'
        return salary
    if 20000 < s and s <= 30000:
        salary = '20k-30k'
        return salary
    if 3000 < s and s <= 40000:
        salary = '30k-40k'
        return salary
    else:
        salary = '40k以上'
        return salary
