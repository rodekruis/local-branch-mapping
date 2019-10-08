# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import json
from scrapy.exceptions import DropItem
from pilot_scraping import settings
import base64
count=0
def write_to_csv(item):
    writer = csv.writer(open(settings.csv_file_path, 'a'), lineterminator='\n')
    writer.writerow([item[key] for key in item.keys()])
def write_as_separate_file(item):
    global count
    with open(settings.corpus_path+str(count),"wb") as f:
        writer = csv.writer(open(settings.corpus_path+"mapping", 'a'), lineterminator='\n')
        writer.writerow([str(count)+item['link']])
        f.write(item['link_text'].encode('utf-8'))
        count+=1
    with open(settings.corpus_path+str(count)+'_html',"wb") as f:
        f.write(item['full_html'].encode('utf-8'))
class PilotScrapingPipeline(object):
    def __init__(self):
        # self.file = open('result.jl', 'w')
        self.seen = set()

    def process_item(self, item, spider):
        if item['link'] in self.seen:
            raise DropItem('Duplicate link %s' % item['link'])
        self.seen.add(item['link'])
        # write_to_csv(item)
        if item['link_text'] != None:
            write_as_separate_file(item)
            return item
