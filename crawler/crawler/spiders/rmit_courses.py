from typing import Counter
import scrapy
from crawler.items import Course
import string

class QuotesSpider(scrapy.Spider):
    name = "rmit_courses"

    def start_requests(self):
        urls = [
            'https://www.rmit.edu.au/study-with-us/levels-of-study/undergraduate-study/bachelor-degrees/bachelor-of-information-technology-bp162/bp162opn9auscy',
            'https://www.rmit.edu.au/study-with-us/levels-of-study/undergraduate-study/bachelor-degrees/bachelor-of-software-engineering-bp096/bp096p8auscy',
            'https://www.rmit.edu.au/study-with-us/levels-of-study/undergraduate-study/bachelor-degrees/bachelor-of-software-engineering-bp096/bp096p21auscy'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Loop through each row in page
        for idx, selector in enumerate(response.css("tr.courseLine td")):
            if idx % 4 == 0: # first column is course title
                course = Course(title=selector.css("a::text").extract_first())
                current_url = selector.css("a::attr(href)").get()
            if (idx - 2) % 4 == 0: # third colum is course code
                course["code"] = selector.css("::text").extract_first()
                yield scrapy.Request(current_url, callback=self.parse_detail, cb_kwargs={"course": course})
    
    def parse_detail(self, response, **kwargs):
        course = kwargs.get("course")
        essential_info = {
            "Course Description": "description", 
            "Objectives/Learning Outcomes/Capability Development": "outcome", 
            "Course Learning Outcomes": "outcome"
        }
        inserting_info = None
        for paragraph in response.css("div.contentArea *"):
            strong_text = paragraph.css("strong::text")
            texts = paragraph.css("::text").getall()
            
            # If detect the header 
            if strong_text:
                header = strong_text.get().strip(string.punctuation + " ")
                
                # If it is info we need, add
                if header in essential_info:
                    inserting_info = header
                    # Initialize variable if not exist
                    if not course.get(essential_info.get(inserting_info)):
                        course[essential_info.get(inserting_info)] = ""
            
                if header == "Overview of Learning Activities":
                    yield course
                    return             
            elif inserting_info:
                for text in texts:
                    course[essential_info.get(inserting_info)] += (text + " ")

            