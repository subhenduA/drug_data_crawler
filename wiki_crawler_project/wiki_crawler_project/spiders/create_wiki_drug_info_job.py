import scrapy

#  This is the starting point. This class is responsible for crawling the 
#  starting page and distributes the subcategories into multiple job files. 
#  Right now it creates 3 different job files in jobs directory. The job files
#  would be used by the actual crawler for crawling and processing 
class DrugDataStartingSpider(scrapy.Spider):
    name = "create_wiki_drug_info_job"
    start_urls = [
        'https://en.wikipedia.org/wiki/Category:Drugs_by_target_organ_system'
    ]

    def parse(self, response):
        # stores the first page in output directory 
        page = response.url.split("/")[-1]
        sourcefile = '%s/%s.html' % (self.output, page)
        with open(sourcefile, 'wb') as f:
            f.write(response.body)

        links = response.css("div.CategoryTreeItem")
        i = 0
        wr1 = open(''.join([self.jobfilepath, '/','job1']), 'w')
        wr2 = open(''.join([self.jobfilepath, '/','job2']), 'w')
        wr3 = open(''.join([self.jobfilepath, '/','job3']), 'w')
       	for link in links:
            category_title = link.css("div a::text").extract_first()
            next_page = response.urljoin(link.css("div a::attr(href)").extract_first())
            if (i % 3) == 0:
            	wr1.write(''.join([next_page, '\n']))
            elif (i % 3) == 1:
            	wr2.write(''.join([next_page, '\n']))
            elif (i%3) == 2:
            	wr3.write(''.join([next_page, '\n']))
            i+=1
        wr1.close()
        wr2.close()
        wr3.close()
