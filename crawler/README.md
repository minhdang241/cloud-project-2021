# Crawler

Simple scrapy project to crawl data of RMIT courses 

'dataset.csv' contains 96 courses from IT and software. Fields:
- Course code
- Course title
- Course description
- Course outcome

## Start guide
```
1. Install scrapy
pip install scrapy

2. Run
scrapy crawl rmit_courses -t csv -o dataset.csv
```