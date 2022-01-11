import requests
from bs4 import BeautifulSoup

def _safe_extract_text(obj):
    return getattr(obj, 'text', '').strip()

def _safe_extract_location(obj):
    out = []
    for loc in obj.contents:
        out.append(_safe_extract_text(loc))

    return out

def scrape(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="mosaic-provider-jobcards")
    job_elements = results.find_all("a")        

    jobs = []

    for job_element in job_elements:
        title_element = job_element.find("h2", class_="jobTitle")

        if title_element is None:
            continue

        # Extract the elements from the main job_element
        company_element = job_element.find("span", class_="companyName")
        company_location_element = job_element.find( "div", class_="companyLocation")
        salary_range_element = job_element.find("div", class_="metadata salary-snippet-container")
        job_snippet_element = job_element.find("div", class_="job-snippet")

        # Extract the text from the children elements and append it to the list
        jobs.append({        
            "title": _safe_extract_text(title_element.contents[-1]), # Sometimes has multiple children
            "company": _safe_extract_text(company_element),        
            "location": _safe_extract_location(company_location_element), # Sometimes has multiple children
            "salary_range": _safe_extract_text(salary_range_element),
            "job_snippet": _safe_extract_text(job_snippet_element),
            "link": "https://indeed.com" + job_element['href'],
            "source_id" : job_element['id']
        })

    return jobs