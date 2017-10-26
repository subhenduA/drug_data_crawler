import scrapy
import time
import os
import json

class DrugdataSpider(scrapy.Spider):
    name = "drugdata"

    def start_requests(self):
        urls = [
            #'https://en.wikipedia.org/wiki/Category:Drugs_by_target_organ_system'
            #'https://en.wikipedia.org/wiki/Category:Osteoporosis_drugs'
             'https://en.wikipedia.org/wiki/Omeprazole'
        ]
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta['context_root'] = self.filepath
            yield request

    def parse(self, response):
        '''
            first store the source html in the current filepath
        '''
        dicrectory_path = response.meta['context_root']
        page = response.url.split("/")[-1]
        sourcefile = '%s/%s.html' % (dicrectory_path, page)
        with open(sourcefile, 'wb') as f:
            f.write(response.body)

        if page.startswith("Category:"):
            ''' 
            crawls subcategory pages, 
            TODO: may contain the same bug as drug pages on group fix it 
            '''
            links = response.css("div.CategoryTreeItem")
            if len(links) > 0:
                for link in links:
                    time.sleep(1)
                    category_title = link.css("div a::text").extract_first()
                    print ("Crawling: %s" %(category_title))
                    next_page = response.urljoin(link.css("div a::attr(href)").extract_first())
                    next_directory_path = ''.join([dicrectory_path, '/', category_title])
                    os.makedirs(next_directory_path, exist_ok=True)
                    request = scrapy.Request(next_page, callback=self.parse)
                    request.meta['context_root'] = next_directory_path
                    yield request

            '''
            crawls durg pages
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
                key = '/'.join(row.css('tr th a::text').extract())
                #value = ' '.join(rows.css('tr td::text').extract() + rows.css('tr td a::text').extract())
                if key != None:
                    data_dict[key] = "my value"
            drugfile = '%s/%s.json' % (dicrectory_path, page)
            with open(drugfile, 'w') as outfile:  
                json.dump(data_dict, outfile)



        '''
        Next steps :  
                     C) work on extracting data out for each drug page, json, csv 
                     D) work on creating schema 
        '''
