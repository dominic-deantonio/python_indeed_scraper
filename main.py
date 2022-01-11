import json

from indeed_scraper import scrape as indeed

url = "https://www.indeed.com/jobs?q=software%20developer&vjk=26d8d5d099e6295b"
jobs = indeed.scrape(url)
json_jobs = json.dumps(jobs, indent=4)

print(json_jobs)