# Drug Data Crawler project
This is a python based project intended to crawl drug data from wiki pages, process the data, stores it into a datastore. Finally there is web framework to make the data available through endpoints
## Componenets used 
A) 'Scrpay' for crawling data 
B) 'mysql' for storing data 
C) 'flask' to access data 

## Installation

### scrapy
```bash
pip3 install Scrapy 
```
In case you get blocked during installation, more details about instllation is here 
https://doc.scrapy.org/en/latest/intro/install.html
FYI in a brand new environment you may need to get the following components installed. I tried to run this code in an ubuntu compute instance in google cloud. I had to install the following packages for the full setup
```bash
sudo apt-get install libxml2-dev libxslt1-dev
sudo apt-get install -y libxml2-dev libxslt1-dev zlib1g-dev python3-pip
sudo apt-get install python3-pip
sudo pip3 install --upgrade setuptools
sudo pip3 install twisted
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
sudo pip3 install pyopenssl
sudo pip3 install cryptography
sudo pip3 install ctutlz
sudo pip3 install queuelib
```
### mysql
Download mysql from here https://dev.mysql.com/doc/refman/5.7/en/osx-installation-pkg.html
```bash
pip3 install mysqlclient
```
### flask
TODO

## Code Deployment 

1) Clone the git repository 
https://github.com/subhenduA/drug_data_crawler
2) Create an export variable called $CRAWLER_HOME pointing to the repo directory. e.g.,
```bash
$ git clone https://github.com/subhenduA/drug_data_crawler.git
$ export CRAWLER_HOME=/Users/saich/drug_data_crawler
```
3) Assuming mysql is installed properly 
```bash
$ mysql < $CRAWLER_HOME/db/schema.sql
```
## Get started

1) Create parallel crawl job
Since scrapy is not inherently multi-threaded, my approach is to distribute the work into multiple scrapy spider processes. I have considered creating 3 different scrapy job processes to crawl and process the data. This is the init crawler 'create_wiki_drug_info_job'. It crawls the index page (https://en.wikipedia.org/wiki/Category:Drugs_by_target_organ_system) and divdes the 14 subcategories into 3 different job files. The job files would be used by the actual data crawler in next step. Run the following commands

```bash
$ cd $CRAWLER_HOME
$ mkdir jobs
$ mkdir output
$ scrapy crawl create_wiki_drug_info_job -a jobfilepath=$CRAWLER_HOME/jobs -a output=$CRAWLER_HOME/output
```
The above run should create 3 different job files in jobs directory. Open the individual job files and verify the subcategories.
2) Run the following 3 crawler jobs as background processes (using nohup or screen utility) 
```bash
$ cd  $CRAWLER_HOME/wiki_crawler_project
$ scrapy crawl drugdata  -a jobfilepath=$CRAWLER_HOME/jobs/job1 -a filepath=$CRAWLER_HOME/output
$ scrapy crawl drugdata  -a jobfilepath=$CRAWLER_HOME/jobs/job2 -a filepath=$CRAWLER_HOME/output
$ scrapy crawl drugdata  -a jobfilepath=$CRAWLER_HOME/jobs/job3 -a filepath=$CRAWLER_HOME/output
```
Alternatively, if you just want to test the code run one of the above jobs. Wait for  2-3 mins. and then kill the process. 

When the above job gets finished (or executed for few minutes), the source files and drug data json files will start getting stored in '$CRAWLER_HOME\output' directory. Peek inside the output dir and validate the file structure. The 'leaf' directories contain the drug files and a json file file containing the wiki table data. Open the json and verify it. 

3) Data normalization & data loading 
In this step the data gets standardized before it gets loaded into database. This is where a lot of normalization can be done to improve the quality of data. I just went through the basic steps so that data can get loaded into mysql. 
```bash
$ cd  $CRAWLER_HOME/wiki_crawler_project
$ python3 ./wiki_crawler_project/spiders/drug_data_normalizer.py
```
After this step login to mysql and access the data. The data isstored in a 'drug_details' table in 'wiki_drug_db' schema.

4) Expose Endpoint to access the data 
TODO

# Improvements 
1) I spent some time in wikimedia REST api (api.sh) for parsing drug tables. But couldn't make it work to extract wiki data tables easily. If get some time i can check if i can make it work. Decided to write my own parser in scrapy.
2) Definitely a lot of normalization is possible to improve the quality of data. After which it would be easy to query the dataset. 


