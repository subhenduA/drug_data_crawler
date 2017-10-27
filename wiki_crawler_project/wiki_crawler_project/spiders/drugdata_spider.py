import scrapy
import time
import os
import json
import csv

# This class is responsible for actual crwawling. It recursively follows sub category 
# links, saves the source files into hierachical fiel system. Apart from that when it 
# encounters drug files it dumps the wiki table data into json file as well. 
# Category file directory starts with 'Category:'
# Drug file directory starts with 'Drug:'
class DrugdataSpider(scrapy.Spider):
    name = "drugdata"
    def start_requests(self):
        with open(self.jobfilepath) as f:
            urls = f.read().splitlines()
        # creates the next directory 
        for url in urls:
            page = url.split("/")[-1]
            directory_path = ''.join([self.filepath, '/', page])
            os.makedirs(directory_path, exist_ok=True)
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta['context_root'] = directory_path
            yield request

    def parse(self, response):
        '''
            store sthe source html in the current filepath
        '''
        dicrectory_path = response.meta['context_root']
        page = response.url.split("/")[-1]
        sourcefile = '%s/%s.html' % (dicrectory_path, page)
        with open(sourcefile, 'wb') as f:
            f.write(response.body)

        if page.startswith("Category:"):
            ''' 
            Recursive call for sub category pages linked from this page
            TODO: there may be a bug in using div.CategoryTreeItem class. Need 
            to probe more
            '''
            links = response.css("div.CategoryTreeItem")
            if len(links) > 0:
                for link in links:
                    time.sleep(1)
                    category_url = link.css("div a::attr(href)").extract_first()
                    print ("Crawling: %s" %(category_url))
                    next_page = response.urljoin(category_url)
                    next_directory_path = ''.join([dicrectory_path, '/', category_url.split("/")[-1]])
                    os.makedirs(next_directory_path, exist_ok=True)
                    request = scrapy.Request(next_page, callback=self.parse)
                    request.meta['context_root'] = next_directory_path
                    yield request

            '''
            Recursive call for drug pages linked from this page
            '''
            links = response.css("div.mw-category-group a")
            if len(links) > 0:
                for link in links:
                    time.sleep(1)
                    drug_title = link.css(' a::attr(title)').extract_first()
                    print ("Crawling: %s" %(drug_title))
                    next_page = response.urljoin(link.css(' a::attr(href)').extract_first())
                    next_directory_path = ''.join([dicrectory_path, '/Drug:', drug_title])
                    os.makedirs(next_directory_path, exist_ok=True)
                    request = scrapy.Request(next_page, callback=self.parse)
                    request.meta['context_root'] = next_directory_path
                    yield request
        else:
            '''
            extracts data out of drug page
            there is a table with class 'infobox'. All the data is inside it.
            there are rows inside id <tr> 
            Each row has <th> for key name and <td> for key vlaue 
            '''
            data_dict = {}
            rows = response.css('table.infobox tr')
            for row in rows:
                key = self.parse_key(row)
                value = self.parse_value(row)
                if key != '':
                    data_dict[key] = value
                    value_array.append(value)
            # stores the data as json inside the directory
            drug_jsonfile = '%s/%s.json' % (dicrectory_path, page)
            with open(drug_jsonfile, 'w') as outfile:  
                json.dump(data_dict, outfile)

    
    def parse_key(self, row):
        key = '/'.join(row.css('tr th a::text').extract())
        if key == '':
            key = '/'.join(row.css('tr th a::attr(title)').extract())
        if key == '':
            key = '/'.join(row.css('tr th::text').extract())
        return key.replace(" ", "_").replace('\n', '_').replace('/', '').lower()

    def parse_value(self, row):
        value = ','.join(row.css('tr td::text').extract() + row.css('tr td a::text').extract())
        return value.replace("\n", ",").replace(",,", "")
