import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests


def search_keywords_in_text(text, keywords):
    if not isinstance(text, str): 
        text = str(text)
        
    found_keywords = []
    for keyword in keywords:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, text, flags=re.IGNORECASE):  
            found_keywords.append(keyword)
    return found_keywords


def extract_italicized_text(text):
    """Extract italicized text from the given HTML or markdown-formatted text."""
    soup = BeautifulSoup(text, 'html.parser')
    
    italic_texts = soup.find_all(['i', 'em', 'jats:italic'])
    
    italicized = [tag.get_text() for tag in italic_texts]
    
    filtered_italicized = [text for text in italicized if len(text) > 3]
    
    return filtered_italicized


def get_chapter_from_url(url, keyword):
    """
    Extracts content from a paper's webpage based on a keyword found in the chapter heading.
    
    Parameters:
        url (str): The URL of the paper.
        keyword (str): The keyword to search for within the chapter headings.
    
    Returns:
        str: The extracted chapter content if a matching heading is found, 
             or a message if no matching heading is found.
    """
    options = Options()
    options.add_argument('--headless')  
    options.add_argument('--disable-gpu') 
    options.add_argument('--no-sandbox') 
    options.add_argument('start-maximized') 
    options.add_argument('disable-infobars')  

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        content = driver.page_source

        soup = BeautifulSoup(content, 'html.parser')

        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        for heading in headings:
            if keyword.lower() in heading.get_text().lower(): 
                content = []
                for sibling in heading.find_next_siblings():
                    if sibling.name and sibling.name.startswith('h'): 
                        break
                    content.append(sibling.get_text(strip=True))
                return '\n'.join(content)

        return f"Chapter with the keyword '{keyword}' not found."
    
    except requests.RequestException as e:
        return f"Error fetching the page: {e}"
    except Exception as e:
        return f"An error occurred: {e}"
    
