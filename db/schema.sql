DROP DATABASE IF EXISTS wiki_drug_db;
CREATE DATABASE wiki_drug_db;
CREATE TABLE wiki_drug_db.drug_details (
wiki_name varchar(200),
type text,
source text,
target text,
pronunciation text,
trade_names text,
ahfs_drugs_com text,
license_data text,
pregnancy__category text,
routes_of__administration text,
atc_code text,
legal_status text,
bioavailability text,
biological_half_life text,
cas_number text,
drugbank text,
chemspider text,
unii text,
kegg text,
chembl text,
formula text,
molar_mass text,
primary key (wiki_name)
);