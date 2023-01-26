import sys
import requests
import hashlib
import json
from time import sleep 
from bs4 import BeautifulSoup

HEADERS = { 
     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

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
     
     researcher_coauthor_name = [coauthor.find("a").get_text() for coauthor in soup.find_all("span", class_="gsc_rsb_a_desc")]
     researcher_coauthor_title = [coauthor.get_text() for coauthor in soup.find_all("span", class_="gsc_rsb_a_ext")]
     researcher_coauthor_link = [coauthor.find("a", href=True)["href"] for coauthor in soup.find_all("span", class_="gsc_rsb_a_desc")]
     researcher_coauthor_dict = []
     for i in range(len(researcher_coauthor_name)):
          researcher_coauthor_dict.append({
               "coauthor_name": researcher_coauthor_name[i], 
               "coauthor_title": researcher_coauthor_title[i], 
               "coauthor_link": researcher_coauthor_link[i]
          })
    
    # TODO: Need to fix coauthor title - pulling extra data into list
    # Add error handling for NoneType error

     researcher_paper_title = [paper.get_text() for paper in soup.find_all("a", class_="gsc_a_at")]
     researcher_paper_authors = [paper.find("div", class_="gs_gray").get_text() for paper in soup.find_all("td", class_="gsc_a_t")]
     researcher_paper_journal = [paper.find("div", class_="gs_gray").get_text() for paper in soup.find_all("td", class_="gsc_a_t")]
     researcher_paper_citedby = [paper.find("a", class_="gsc_a_ac gs_ibl").get_text() for paper in soup.find_all("td", class_="gsc_a_c")]
     researcher_paper_year = [paper.find("span", class_="gsc_a_h gsc_a_hc gs_ibl").get_text() for paper in soup.find_all("td", class_="gsc_a_y")]
     researcher_paper_dict = []
     for i in range(len(researcher_paper_title)):
          researcher_paper_dict.append({
               "paper_title": researcher_paper_title[i], 
               "paper_authors": researcher_paper_authors[i], 
               "paper_journal": researcher_paper_journal[i],
               "paper_citedby": researcher_paper_citedby[i],
               "paper_year": researcher_paper_year[i]
          })

     return researcher_name, researcher_caption, researcher_institution, \
          researcher_keywords, researcher_imgURL, researcher_citations, \
          researcher_hindex, researcher_i10index, researcher_coauthor_dict, researcher_paper_dict

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

def write_json_data(content, url):
     """
     Description:
          Writes the content to a file with hashed name.
     
     Parameters:
          content (str): The content to write to the file.
          url (str): The URL of the page to retrieve.
     """
     parsed_content = get_parsed_content(url)
     content_dict = {
          "researcher_name": parsed_content[0],
          "researcher_caption": parsed_content[1],
          "researcher_institution": parsed_content[2],
          "researcher_keywords": parsed_content[3],
          "researcher_imgURL": parsed_content[4],
          "researcher_citations": {"all": parsed_content[5][0], "since2018": parsed_content[5][1]},
          "researcher_hindex": {"all": parsed_content[6][0], "since2018": parsed_content[6][1]},
          "researcher_i10index": {"all": parsed_content[6][0], "since2018": parsed_content[6][1]},
          "researcher_coauthors": parsed_content[8],
          "researcher_papers": parsed_content[9]
     }

     filename = 'data/' + hash_url(url) + '.json'
     with open(filename, 'w') as f:
          f.write(json.dumps(content_dict, indent=4))

def hash_url(url):
     """
     Description:
          Returns the SHA256 hash of the given URL.

     Parameters:
          url (str): The URL to hash.
     """
     return hashlib.sha256(url.encode()).hexdigest()
          
def loading(iter, total, prefix='', suffix='', decimals=1, length=100, fill='>'):
     """
     Description:
          A loading bar for the command line. Yes, I have time on my hands.

     Parameters:
          iter (int): The current iteration.
          total (int): The total number of iterations.
          prefix (str): The prefix to display before the loading bar.
          suffix (str): The suffix to display after the loading bar.
          decimals (int): The number of decimals to display.
          length (int): The length of the loading bar.
          fill (str): The character to use to fill the loading bar.
     """
     percent = ("{0:." + str(decimals) + "f}").format(100 * (iter / float(total)))
     filled_len = int(length * iter // total)
     bar = fill * filled_len + '-' * (length - filled_len)
     
     print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = '\r')
     
     if iter == total:
          print()

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

     items = list(range(0, 50))
     l = len(items)
          

     print(r"""

                                   ._ o o
                                   \_`-)|_
                                ,""       \ 
                              ,"  ## |   ಠ ಠ. 
                            ," ##   ,-\__    `.
                          ,"       /     `--._;)
                        ,"     ## /
                      ,"   ##    /
     """)

     loading(0, l, prefix='Progress:', suffix='Complete', length=l)
     for i, item in enumerate(items):
          sleep(0.09)
          loading(i + 1, l, prefix='Progress:', suffix='Complete', length=l)

     content = get_content(url).prettify()

     if content:
          write_raw_data(content, url)
          write_json_data(content, url)
     else:
          print("Error. Unable to retrieve this flaming heap of garbage.")

if __name__ == "__main__":
     main()