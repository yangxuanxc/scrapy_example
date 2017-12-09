# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import join,basename,dirname

class MatplotlibExamplesPipeline(object):
    def process_item(self, item, spider):
        return item

#path = "https://matplotlib.org/mpl_examples/api/barchart_demo.py"

class MotplotlibFilesPipeLine(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        path = urlparse(request.url).path
        return join(basename(dirname(path)),basename(path))