import scrapy
from scrapy.http.request import Request
from crawler.items import Job

from bs4 import BeautifulSoup
import string
import re
from urllib import parse

def remove_tags(html):
    if html is None:
        return ""
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
  
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
    string_list = []
    for my_string in soup.stripped_strings:
        string_list.append(my_string.strip(string.punctuation + "oO \n\t\r" ))
    # return data by retrieving the tag content
    return '. '.join(string_list)

def get_next_page(current_url: str):
    if "start=" in current_url:
        obj = re.search(r'start=(\d*)', current_url)
        count = int(obj.group(1))
        page = int(count / 10 + 1)
        return re.sub(r'start=(\d*)', lambda obj: f'start={int(obj.group(1)) + 10}', current_url), page
    else:
        match_obj = re.search("Vi%E1%BB%87c-l%C3%A0m-([\w-]*)-t%E1%BA%A1i-([\w-]*)", current_url)
        if match_obj:
            components = parse.urlsplit(current_url)
            base = current_url.replace(components.path, "")
            payload = {
                "q": match_obj.group(1).replace("-", " "),
                "l": match_obj.group(2).replace("-", " "),
                "start": 10
            }
            return f"{base}/jobs?{parse.urlencode(payload)}", 2
        return f"{current_url}&start=10", 2

class JobSpider(scrapy.Spider):
    name = "indeed_job"
    
    base_url = "https://www.indeed.com"
    jobs = []
    
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
        "ITEM_PIPELINES": {
            'crawler.pipelines.JobDuplicatesPipeline': 800,
        },
        "DOWNLOAD_DELAY": 2
    }
    # &start=10
    start_urls = [
                'https://vn.indeed.com/jobs?q=software+engineer&l=Ho+Chi+Minh+City', 
                #   'https://vn.indeed.com/jobs?q=data+engineer&l=Ho+Chi+Minh+City', 
                #   'https://vn.indeed.com/jobs?q=web%20developer&l=Ho%20Chi%20Minh%20City',
                #   'https://vn.indeed.com/jobs?q=devops&l=Ho%20Chi%20Minh%20City', 
                #   'https://vn.indeed.com/jobs?q=android%20developer&l=Ho%20Chi%20Minh%20City',
                #   'https://vn.indeed.com/jobs?q=machine%20learning&l=Ho%20Chi%20Minh%20City',
                #   'https://vn.indeed.com/jobs?q=software+qa&l=Ho+Chi+Minh+City',
                #   'https://vn.indeed.com/jobs?q=cyber%20security&l=Ho%20Chi%20Minh%20City',
                #   'https://vn.indeed.com/jobs?q=ios%20developer&l=Ho%20Chi%20Minh%20City',
                #   'https://vn.indeed.com/jobs?q=full%20stack%20engineer&l=Ho%20Chi%20Minh%20City',
                #   'https://vn.indeed.com/jobs?q=backend%20engineer&l=Ho%20Chi%20Minh%20City',
                #   'https://vn.indeed.com/jobs?q=frontend%20engineer&l=Ho%20Chi%20Minh%20City'
        ]
    
    limit_page = 3
    page = 0

    def parse(self, response, **kwargs):
        job_selectors = response.xpath('.//a[contains(@id,"job_")]')
        
        for selector in job_selectors:
            job = Job()
            job['title'] = selector.xpath('.//h2[contains(@class,"jobTitle")]/span/text()').extract_first()
            company = selector.xpath('.//a[@data-tn-element="companyName"]/text()').extract_first()
            if company is None:
                company = selector.xpath('.//span[@class="companyName"]/text()').extract_first()
            job['company_name'] = company
            job['company_location'] = selector.xpath('.//div[@class="companyLocation"]/text()').extract_first()
            bullets = selector.xpath('.//div[@class="job-snippet"]/ul/li/text()').extract()
            job['short_description'] = ". ".join([b.strip(string.punctuation + "oO \n\t\r" ) for b in bullets])
            link = selector.xpath('./@href').extract_first()
            job['link'] = f"{self.base_url}{link}"
            yield Request(url=f"{self.base_url}{link}", callback=self.parse_job, cb_kwargs={"job": job})
        
        
        # next_url, page = get_next_page(response.request.url)
        # if page <= self.limit_page:
        #     yield Request(url=next_url, callback=self.parse)
            
    def parse_job(self, response, job: Job):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        description_div = response.xpath('//div[@id="jobDescriptionText"]').get()
        job['description'] = remove_tags(description_div)        
        yield job
        

