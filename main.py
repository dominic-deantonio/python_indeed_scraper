import json
from art import show_art
from indeed_scraper import scrape
import time

"""
Main script for the user to interface with the scraping function
"""

show_art()

print('What category of job would you like to scrape?')
category = input()

print('Enter location or type "n" for none')
location = input()

if location.lower().strip() == 'n':
    print('No location selected')
    location = ""
    
# Build the scraping URL from the user input
url = f"https://www.indeed.com/jobs?q={category}&l={location}" 

# Do the scraping and advise the user
print(f'Scraping {category} jobs...')
jobs = scrape(url)
print(f'Results returned: {len(jobs)}')

if len(jobs) == 0:
    print('There were no results. Please try again with a different query.')
    exit()

# Prompt the user to check if they want to save the results
# Also manage incorrect input
should_save = ''
while should_save != 'y' and should_save != 'n':
    print('Would you like to save the results? "y" or "n"')
    should_save = input().lower().strip()
    if should_save != 'y' and should_save != 'n':
        print('Invalid input')

json_jobs = json.dumps(jobs, indent=4)

# Do the save if the user wants to save as a file
if should_save == 'y':
    file_name =  f'indeed-search-{round(time.time() * 1000)}.json'
    f = open(file_name, "w")
    f.write(json_jobs)
    f.close()
    print(f'Results saved as {file_name}')
    time.sleep(2)

print(f'Results:\n\n{json_jobs}')