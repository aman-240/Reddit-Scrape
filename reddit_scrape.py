import requests, re
from bs4 import BeautifulSoup
import lxml, json

class RedditPost:
    def __init__(self, url):
        """
        @param url: URL of the reddit post
        @type url: str
        
        init contains:
        1. url
        2. timestamp
        3. image url
        4. uploaded image url
        """
        self.url = url
        self.headers = {
                        'User-Agent': '',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Upgrade-Insecure-Requests': '1',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'none',
                        'Sec-Fetch-User': '?1',
                        'Connection': 'keep-alive',
                        'Cookie': '<INSERT HERE>',
                        'TE': 'trailers'
                    }
                
    def post_info(self):
        """
        scrape_image_url scrapes the image url from the reddit post
        """
        self.image_info = {}
        response = requests.request("GET", self.url, headers=self.headers)
        soup = BeautifulSoup(response.text,'lxml')
        self.data = soup.find_all("div", {"class": "_1poyrkZ7g36PawDueRza-J _11R7M_VOgKO1RJyRSRErT3 _1Qs6zz6oqdrQbR7yE_ntfY"})
        
        self.temp_data = self.data
        pattern = "https://preview.redd.it/(.\w+)+|https://i.redd.it/(.\w+)+"
        match = re.search(pattern, str(self.temp_data))
        self.image_url = match.group().replace("amp;","")
        self.image_info = {"Image URL":self.image_url, "Title":self.scrape_title(), "Timestamp":self.scrape_timestamp()}
            
        return self.image_info
    
    def scrape_timestamp(self):
        """
        scrape_timestamp scrapes the timestamp of the reddit post
        """
        self.time_stamp = self.temp_data.find("span", {"data-testid": "post_timestamp"}).text.replace(" ","")
        return self.time_stamp
    
    def scrape_title(self):
        """
        scrape_title scrapes the title of the reddit post
        """
        title = self.temp_data.find("h3", {"class": "_eYtD2XCVieq6emjKBH3m"}).text
        return title
    
url = "https://www.reddit.com/r/marvelmemes/new/"
marvel = RedditPost(url=url)
print(marvel.post_info())