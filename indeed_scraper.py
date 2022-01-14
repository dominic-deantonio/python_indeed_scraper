import requests
from bs4 import BeautifulSoup

"""Contains the main scraping function"""

def _safe_extract_text(obj):
    # Safely extracts text by checking HTML element for None

    return getattr(obj, 'text', '').strip()


def _safe_extract_location(obj):
    # Safely extracts locations by checking HTML element for None

    out = []
    for loc in obj.contents:
        out.append(_safe_extract_text(loc))

    return out


def _extract_from_job_element(job_element):
    # Extract the elements from the main job_element and return the result
    title_element = job_element.find("h2", class_="jobTitle")
    company_element = job_element.find("span", class_="companyName")
    company_location_element = job_element.find("div", class_="companyLocation")
    salary_range_element = job_element.find("div", class_="metadata salary-snippet-container")
    job_snippet_element = job_element.find("div", class_="job-snippet")

    # Extract the text from the children elements and return from function
    return {        
        "title": _safe_extract_text(title_element.contents[-1]), # Sometimes has multiple children, so we extract the last one
        "company": _safe_extract_text(company_element),
        "location": _safe_extract_location(company_location_element),
        "salary_range": _safe_extract_text(salary_range_element),
        "job_snippet": _safe_extract_text(job_snippet_element),
        "link": "https://indeed.com" + job_element['href'],
        "source_id": job_element['id']
    }


def scrape(url):
    # Main scraping function

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # This holds the job elements
    results = soup.find(id="mosaic-provider-jobcards")

    if results is None:
        print('Unable to get results :(')
        return []

    # Gets the HTML Elements containing jobs
    job_elements = results.find_all("a")

    jobs = []

    # Loop over all the extracted job elements to extract the text
    for job_element in job_elements:

        # Do a test to make sure the the title is available
        title_element = job_element.find("h2", class_="jobTitle")
        if title_element is None:
            continue

        jobs.append(_extract_from_job_element(job_element))

    if(len(jobs) == 0):
        print(
            f'Unable to get jobs. There may have been a problem with the raw HTML:\n\n{page.content}')

    return jobs
