from pymongo import MongoClient

# database details
client = MongoClient("mongodb://localhost:27017")
database = client["youtubeData"]

def push_to_mongodb(data):
    collection_name = data["channel_details"]["channel_name"]
    collection = database[collection_name]
    result = collection.insert_one(data)
    client.close()
    
def check_if_exists(channel_name: str):
    """
    this function checks whether the scraped data the particular youtube channell
    already exists if exists delete the older one and insert the new one in case 
    of update if not then proceed with pushing the scraped data to mongodb
    """
    collections_list = database.list_collection_names()
    if channel_name in collections_list:
        database[channel_name].drop()
        
        

    