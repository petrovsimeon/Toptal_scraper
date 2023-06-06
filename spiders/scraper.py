import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request


class ScraperSpider(scrapy.Spider):
    name = 'scraper'
    allowed_domains = ['toptal.com']
    start_urls = ['https://www.toptal.com/designers/all']  # https://www.toptal.com/finance/all

    # Parsing the skills page
    def parse(self, response):
        skills = response.xpath('//li[@class="rY5wqR2J"]/a/@href').extract()

        for skill in skills:
            profiles_page = skill
            yield Request(profiles_page, callback=self.parse_profiles)

    # Parsing all profile links
    def parse_profiles(self, response):
        profiles = response.xpath("//h3[@itemprop='name']/a/@href").extract()

        for profile in profiles:
            yield Request(profile, callback=self.parse_details)

    # Parsing all details about people
    def parse_details(self, response):
        full_name = response.xpath("//div[@class='resume_top-info_name']/text()").extract_first()
        location = response.xpath("//h1[@class='resume_top-info_location']/text()").extract_first()
        url = response.request.url
        member_since = response.xpath("//div[@class='resume_top-info_since']/text()").extract_first()
        bio = response.xpath("//div[@class='resume_top-info_bio']/text()").extract_first()
        tags = ', '.join(response.xpath("//a[@class='tag is-expert']/text()").extract())
        experience = ', '.join(
            response.xpath("//ul[@class='resume_details-list js-experience_section']/li//text()").extract()).replace(
            ",  ", " : ")

        availability = response.xpath(
            "//h2[contains(text(),'Availability')]/following-sibling::div/text()").extract_first()
        preffered_environment = response.xpath(
            "//h2[contains(text(),'Preferred Environment')]/following-sibling::div/text()").extract_first()
        most_amazing = response.xpath(
            "//h2[contains(text(),'The most amazing...')]/following-sibling::div/text()").extract_first()

        all_jobs = []
        experience_jobs = jobs = response.xpath(
            "//div[@class='resume_section js-employments']/div/div[@class='resume_section-content']/ul/li")

        for job in experience_jobs:
            all_jobs.append('\n' + '\n'.join(job.xpath("div//text()").extract()))

        all_jobs = '\n'.join(all_jobs)

        languages = ', '.join(
            response.xpath("//h3[contains(text(),'Languages')]/following-sibling::div/span/text()").extract())
        frameworks = ', '.join(
            response.xpath("//h3[contains(text(),'Frameworks')]/following-sibling::div/span/text()").extract())
        libraries = ', '.join(
            response.xpath("//h3[contains(text(),'Libraries/APIs')]/following-sibling::div/span/text()").extract())
        tools = ', '.join(response.xpath("//h3[contains(text(),'Tools')]/following-sibling::div/span/text()").extract())
        paradigms = ', '.join(
            response.xpath("//h3[contains(text(),'Paradigms')]/following-sibling::div/span/text()").extract())
        platforms = ', '.join(
            response.xpath("//h3[contains(text(),'Platforms')]/following-sibling::div/span/text()").extract())
        other = ', '.join(response.xpath("//h3[contains(text(),'Other')]/following-sibling::div/span/text()").extract())
        storage = ', '.join(
            response.xpath("//h3[contains(text(),'Storage')]/following-sibling::div/span/text()").extract())

        education_all = []
        education_rows = response.xpath(
            "//div[@class='resume_section js-educations']/div/div[@class='resume_section-content']/ul/li")

        for education in education_rows:
            education_all.append('\n' + ', '.join(education.xpath("div//text()").extract()))

        education_all = '\n'.join(education_all)

        yield {"Full name": full_name,
               "Location": location,
               "Member since": member_since,
               "Url": url,
               "Bio": bio,
               "Tags": tags,
               "Experience (years)": experience,
               "Availability": availability,
               "Preffered Environment": preffered_environment,
               "Most amazing...": most_amazing,
               "Experience (jobs)": all_jobs,
               "Languages": languages,
               "Frameworks": frameworks,
               "Libraries": libraries,
               "Tools": tools,
               "Paradigms": paradigms,
               "Platforms": platforms,
               "Other": other,
               "Storage": storage,
               "Education": education_all}
