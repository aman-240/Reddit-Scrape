from pymongo import MongoClient
import base64

client = MongoClient('<URL>')

# create new database named "court_cases"
mydb = client["reddit_db"]

# create new collection named "case_data"
guild_data = mydb["per_guild_data"]
reddit_data = mydb["reddit_data"]

class GuildData:
    def __init__(self, guild_id):
        self.guild_id = guild_id
    
    def insert_guild_data(self, reddit_url:str, channel_id:str):
        guild_data.insert_one({"guild_id": self.guild_id, "channel_id": channel_id, "reddit_url": [reddit_url]})
    
    def update_guild_data(self, reddit_url:str, channel_id:str):
        guild_data.update_one({"guild_id": self.guild_id, "channel_id": channel_id}, {"$addToSet": {"reddit_url": reddit_url}})
        
    def delete_reddit_url(self, reddit_url:str):
        try:
            guild_data.update_one({"guild_id": self.guild_id}, {"$pull": {"reddit_url": reddit_url}})
        except Exception as e:
            print(e)
            return e
    
    def find_guild_data(self):
        return True if guild_data.find_one({"guild_id": self.guild_id}) else False
    
    def fetch_reddit_urls(self):
        return guild_data.find_one({"guild_id": self.guild_id})["reddit_url"]
    
    @staticmethod
    def find_channel_id(guild_id):
        return guild_data.find_one({"guild_id": guild_id})["channel_id"]
    
    # for reddit data to check if previous link is same with new link
    def insert_reddit_data(self, reddit_url, image_url):
        encoded_key = base64.b64encode(reddit_url.encode()).decode()
        reddit_data.insert_one({f"guild_id":self.guild_id,"data":{f"{encoded_key}": image_url}})
    
    def update_in_insert(self, reddit_url):
        encoded_key = base64.b64encode(reddit_url.encode()).decode()
        reddit_data.update_one({"guild_id": self.guild_id}, {"$set": {f"data.{encoded_key}": ""}})
    
    @staticmethod    
    def update_reddit_data(guild_id, reddit_url, image_url):
        encoded_key = base64.b64encode(reddit_url.encode()).decode()
        query = {"guild_id": guild_id}
        new_values = {"$set": {f"data.{encoded_key}": image_url}}
        reddit_data.update_one(query, new_values)
        
    def delete_reddit_data(self, reddit_url):        
        encoded_key = base64.b64encode(reddit_url.encode()).decode()
        values = reddit_data.find_one({"guild_id": self.guild_id})['data'][f'{encoded_key}']
        reddit_data.update_one({f"data.{encoded_key}": values}, {"$unset": {f"data.{encoded_key}": ""}})
    
    def _get_link(self, reddit_url, image_url):
        encoded_key = base64.b64encode(reddit_url.encode()).decode()
        return reddit_data.find_one({"guild_id": self.guild_id, f"data.{encoded_key}": image_url})