import sys
import requests
import hashlib
import json
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

def session_handler():
     """
     Description:
          Returns a session object and sets the user agent.

     Parameters:
          None
     """
     session = requests.session()
     session.headers.update(HEADERS)
     return session

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
          return soup

def get_parsed_content(url):
     """
     Description:
          Returns the parsed content of the page at the given URL.
          
     Parameters:
          url (str): The URL of the page to retrieve.
     """
     soup = get_content(url)

     researcher_name = soup.find("div", id="gsc_prf_in").contents[0]
     researcher_caption = soup.find("div", class_="gsc_prf_il").contents[0]
     researcher_institution = soup.find("a", class_="gsc_prf_ila").contents[0]
     researcher_keywords = [keywords.get_text() for keywords in soup.find_all("a", class_="gsc_prf_inta gs_ibl")]
     researcher_imgURL = soup.find("img", id="gsc_prf_pup-img")["src"]
     researcher_citations = [citations.get_text() for citations in soup.find_all("td", class_="gsc_rsb_std")[0:2]]
     researcher_hindex = [hindex.get_text() for hindex in soup.find_all("td", class_="gsc_rsb_std")[2:4]]
     researcher_i10index = [i10index.get_text() for i10index in soup.find_all("td", class_="gsc_rsb_std")[4:6]]
     researcher_coauthors = [coauthor.find("a").get_text() for coauthor in soup.find_all("span", class_="gsc_rsb_a_desc")]
     # researcher_papers

     return researcher_name, researcher_caption, researcher_institution, \
               researcher_keywords, researcher_imgURL, researcher_citations, \
                researcher_hindex, researcher_i10index, researcher_coauthors

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

     content = get_content(url).prettify()
     if content:
          write_raw_data(content, url)
          # write_json_data(content, url)
     else:
          print("Error. Unable to retrieve this flaming heap of garbage.")

     print(get_parsed_content(url))


if __name__ == "__main__":
     main()