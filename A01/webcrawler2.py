import sys
import requests
import hashlib
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
               return response.text
          else:
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
          soup = BeautifulSoup(page, 'html.parser')
          return soup.text

def write_to_file(content, url):
     """
     Description:
          Writes the content to a file with hashed name.

     Parameters:
          content (str): The content to write to the file.
          url (str): The URL of the page to retrieve.
     """
     filename = hash_url(url) + '.txt'
     with open(filename, 'w') as f:
          f.write(content)

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
          write_to_file(content, url)
     else:
          print("Error. Unable to retrieve this flaming heap of garbage.")

if __name__ == "__main__":
     main()