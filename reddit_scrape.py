import re
from bs4 import BeautifulSoup
import lxml
import os
from mongoRUN import GuildData

my_cookies = '<INSERT COOKIES HERE>'
my_user_agent = '<INSERT USER AGENT HERE>'


class RedditPost(GuildData):
    def __init__(self, url):
        """
        @param url: URL of the reddit post
        @type url: str
        """
        self.url = url

    def post_info(self, html_file):
        """
        scrape_image_url scrapes the image url from the reddit post
        """
        self.image_info = {}
        soup = BeautifulSoup(html_file, 'lxml')
        self.data = soup.find(
            "div", {
                "class":
                "_1poyrkZ7g36PawDueRza-J _11R7M_VOgKO1RJyRSRErT3 _1Qs6zz6oqdrQbR7yE_ntfY"
            })

        self.temp_data = self.data
        pattern = "https://preview.redd.it/(.\w+)+|https://i.redd.it/(.\w+)+"
        try:
            match = re.search(pattern, str(self.temp_data))
            self.image_url = match.group().replace("amp;", "")
            self.image_info = {
					"Image URL": self.image_url,
					"Title": self.scrape_title(),
					"Timestamp": self.scrape_timestamp()
				}
            return self.image_info
        except:
            return False

    def scrape_timestamp(self):
        """
        scrape_timestamp scrapes the timestamp of the reddit post
        """
        self.time_stamp = self.temp_data.find("span", {
            "data-testid": "post_timestamp"
        }).text
        return self.time_stamp

    def scrape_title(self):
        """
        scrape_title scrapes the title of the reddit post
        """
        title = self.temp_data.find(
            "h3", {"class": "_eYtD2XCVieq6emjKBH3m"}).text
        return title
    
    @staticmethod
    def check_repeat(reddit_url, image_url, guild_id):
        """
        check_repeat checks if the image url is already in the database
        """
        guild_data = GuildData(guild_id)
        if guild_data._get_link(reddit_url=reddit_url, image_url=image_url) is not None:
            return True
        else:
            return False