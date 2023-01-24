import sys
import requests
import hashlib
import json
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

def get_page(url):
     """
     Description:
          Returns the HTML of the page at the given URL.
     
     Parameters:
          url (str): The URL of the page to retrieve.
     """
     try:
          response = requests.get(url, headers=HEADERS)
          if response.status_code == 200:
               return response
          else:
               print(response.status_code)
               return None
     except:
          return None
          
def get_content(url):
     """
     Description:
          Returns the text content of the page at the given URL.

     Parameters:
          url (str): The URL of the page to retrieve.
     """
     page = get_page(url)
     if page:
          soup = BeautifulSoup(page.content, 'html.parser')
          return soup.prettify()

def get_parsed_content(url):
     """
     Description:
          Returns the parsed content of the page at the given URL.
          
     Parameters:
          url (str): The URL of the page to retrieve.
     """
     soup = get_content(url)
     researcher_name = soup.find('div', id='gsc_prf_in')
     print(researcher_name)

     return researcher_name

def write_raw_data(content, url):
     """
     Description:
          Writes the content to a file with hashed name.

     Parameters:
          content (str): The content to write to the file.
          url (str): The URL of the page to retrieve.
     """
     filename = 'data/' + hash_url(url) + '.txt'
     with open(filename, 'w') as f:
          f.write(content)

def write_json_data():
     """
     Description:
          Writes the content to a file with hashed name.
     
     Parameters:
          content (str): The content to write to the file.
          url (str): The URL of the page to retrieve.
     """
     pass

def hash_url(url):
     """
     Description:
          Returns the SHA256 hash of the given URL.

     Parameters:
          url (str): The URL to hash.
     """
     return hashlib.sha256(url.encode()).hexdigest()
          
def main():
     """
     Description:
          Main function.
     
     Usage:
          python webcrawler2.py <url>
     """
     try:
          url = sys.argv[1]
     except:
          print("Error. No URL argument provided.")

     content = get_content(url)
     if content:
          write_raw_data(content, url)
          write_json_data(content, url)
     else:
          print("Error. Unable to retrieve this flaming heap of garbage.")

if __name__ == "__main__":
     main()