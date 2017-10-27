Componenets used : 
A) Scrpay for crawling data 
B) mysql for storing data 
C) flask to access data 

Scrapy installation :- 

```bash
pip3 install Scrapy 
```
In case you get blocked during installation, more details about instllation is here 
https://doc.scrapy.org/en/latest/intro/install.html

mysql installation :-
```bash
pip3 install mysqlclient
```
flask installation :- 

drug_data_crawler installation :- 

Clone the git repository 
https://github.com/subhenduA/drug_data_crawler.git
This is a public repo should be easily accessible.

Create an export variable called $CRAWLER_HOME pointing to the repo directory. e.g.,
```bash
$ export CRAWLER_HOME=/Users/saich/drug_data_crawler
```

Running drug_data_crawler code :

1) Parallelize the crawling work
Since scrapy is not inhereently multi-threaded, the current approach is to distribute the work into multiple scrapy spider processes. I have considered creating 3 different scrapy job processes to crawl and process the data. This is the init crawler 'create_wiki_drug_info_job'. It crawls the index page (https://en.wikipedia.org/wiki/Category:Drugs_by_target_organ_system) and divdes the 14 subcategories into 3 different job files.
```bash
$ cd $CRAWLER_HOME
scrapy crawl create_wiki_drug_info_job -a jobfilepath=$CRAWLER_HOME/jobs -a output=$CRAWLER_HOME/output
```
The above run should create 3 different job files in jobs directory. Open the individual job files and verify the subcategories.
2) 
scrapy crawl drugdata  -a jobfilepath=$CRAWLER_HOME/jobs/job1 -a filepath=$CRAWLER_HOME/output
scrapy crawl drugdata  -a jobfilepath=$CRAWLER_HOME/jobs/job2 -a filepath=$CRAWLER_HOME/output
scrapy crawl drugdata  -a jobfilepath=$CRAWLER_HOME/jobs/job3 -a filepath=$CRAWLER_HOME/output
```
Considered wikimedia api for parsing drug tables. But couldn't get easy parser to parse the wiki datatables. Decided to write my own parser in scrapy.

