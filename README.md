# Drug Data Crawler project
This is a python based project intended to crawl drug data from wiki pages, process the data, stores it into a datastore. Finally there is web framework to make the data available through endpoints
## Componenets used 
A) 'Scrpay' for crawling data 
B) 'pandas' for wrangling data 
C) 'flask' for accessing data
D) 'mysql' for storing data (optional) 

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
### pandas
sudo pip3 install pandas
### flask
sudo pip3 install Flask

### mysql (optional)
Download mysql from here https://dev.mysql.com/doc/refman/5.7/en/osx-installation-pkg.html
```bash
sudo pip3 install mysqlclient
```

## Code Deployment 

1) Clone the git repository 
https://github.com/subhenduA/drug_data_crawler
2) Create 2 export variables called CRAWLER_HOME & FLASK_APP with respect to the repo. location
```bash
$ git clone https://github.com/subhenduA/drug_data_crawler.git
$ export CRAWLER_HOME=/Users/saich/drug_data_crawler
$ export FLASK_APP=$CRAWLER_HOME/web/drug_api.py
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

When the above job gets finished (or executed for few minutes), the source files and drug data json files will start getting stored in '$CRAWLER_HOME\output' directory. Peek inside the output dir and validate the file structure. The 'leaf' directories contain the drug files and a json file containing the wiki table data. Open the json and verify it. 

3) Data normalization  
In this step raw drug data stored in json files gets normalized and gets saved in a separate normalized file. This is where a lot of standardization can be done to improve the quality of data. Ideally each of the fields in wiki table should pass through normalize function so that data can be cleaned up for further analytics downstream. I did some basic preprocessing with 'biological_half_life' , extracted min & max out of the 'biological_half_life' field. Run the following command to execute the normalizer.
```bash
$ cd  $CRAWLER_HOME/wiki_crawler_project
$ python3 ./wiki_crawler_project/normalizer/drug_data_df_normalizer.py
```
The output of the above command is a normalized drug file stored in $CRAWLER_HOME/output directory. THe name of the file is 'drug_data_normalized.json'. This file structure is like the following 
```
{"Acetazolamide": {"type": "", "target": "", "source": "", "pronunciation": "", "trade_names": "Diamox, Diacarb, others", "ahfs_drugs_com": "", "license_data": "", "pregnancy__category": "", "routes_of__administration": "", "atc_code": "S01EC01,WHO", "legal_status": "S4,\u211e-only,POM,\u211e-only", "bioavailability": "", "biological_half_life": "2\u20134 hours,[1]", "cas_number": "216665-38-2", "drugbank": "DB00819", "chemspider": "1909", "unii": "SW1TF3RGAH", "kegg": "D00218", "chembl": "CHEMBL20", "formula": "", "molar_mass": "222.245 g/mol", "biological_half_life_min": "2", "biological_half_life_max": "4"}, 
"Bendroflumethiazide": {"type": "", "target": "", "source": "", "pronunciation": "", "trade_names": "", "ahfs_drugs_com": "", "license_data": "", "pregnancy__category": "", "routes_of__administration": "", "atc_code": "C03AA01,WHO", "legal_status": "POM", "bioavailability": "100%", "biological_half_life": "3-4 hours,[2]", "cas_number": "73-48-3", "drugbank": "DB00436", "chemspider": "2225", "unii": "5Q52X6ICJI", "kegg": "D00650", "chembl": "CHEMBL1684", "formula": "", "molar_mass": "421.415 g/mol", "biological_half_life_min": "3", "biological_half_life_max": "4"},
...
}
```
the key is the wiki_drug_name and value is the json containing normalized values. Notice the normalized fields 'biological_half_life_min' & 'biological_half_life_max' in the sample data. This data would be exposed through flask endpoint in next step. 

4) Expose Endpoint to access the data 
In this stage, normalized data would be made available through flask endpoints. Run flask app using the following command 
```bash
$ cd $CRAWLER_HOME/web
$ flask run 
```
Use nohup if you want to keep flask running. There are 2 different endpoints :- 
A) Access raw drug data : http://<host_name>:5000/drug_info/<drug_name>
It returns you the raw content of the drug data. Sample useage 
```bash
$ curl 'http://127.0.0.1:5000/drug_info/Pedunculagin'
```
B) Access normalized drug data : 
TODO :

# Improvements 
1) I spent some time in wikimedia REST api (api.sh) for parsing drug tables. But couldn't make it work to extract wiki data tables easily. If get some time i can check if i can make it work. Decided to write my own parser in scrapy.
2) Definitely a lot of normalization is possible to improve the quality of data. I just coded the basic framework which uses pandas dataframe parallel processing package to wrangle the data. Ideally we need to write normalizer for each field. 
3) File path is hard coded in few places. Need to pass it through parameter or make it set environment variables.
4) Some of the processing parameters are hard coded , e.g., num_cores, num_partitions in data wrangling. The code should read these variables through a congiguration framework. 


