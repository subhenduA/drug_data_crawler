import scrapy
import time
import os

class DrugdataSpider(scrapy.Spider):
    name = "drugdata"

    def start_requests(self):
        urls = [
            #'https://en.wikipedia.org/wiki/Category:Drugs_by_target_organ_system'
            'https://en.wikipedia.org/wiki/Category:Osteoporosis_drugs'
        ]
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta['context_root'] = self.filepath
            yield request

    def parse(self, response):
        '''
            first store the source in the current filepath
        '''
        dicrectory_path = response.meta['context_root']
        page = response.url.split("/")[-1]
        filename = '%s/%s.html' % (dicrectory_path, page)
        with open(filename, 'wb') as f:
            f.write(response.body)

        ''' 
        crawls subcategory pages, 
        TODO: may contain the same bug as drug pages on group fix it 
        '''
        links = response.css("div.CategoryTreeItem")
        if len(links) > 0:
            for link in links:
                time.sleep(1)
                print ("Crawling: %s" %(link.css("div a::text").extract_first()))
                next_page = response.urljoin(link.css("div a::attr(href)").extract_first())
                request = scrapy.Request(next_page, callback=self.parse)
                request.meta['context_root'] = self.filepath
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
                new_context_root = ''.join([dicrectory_path, '/Drug:', drug_title])
                os.makedirs(new_context_root, exist_ok=True)
                request = scrapy.Request(next_page, callback=self.parse)
                request.meta['context_root'] = new_context_root
                yield request

        '''
        Next steps :
                     B) Work on creating directories for each separate page  
                     C) work on extracting data out for each drig page , json , csv 
                     D) work on creating schema 
        '''
