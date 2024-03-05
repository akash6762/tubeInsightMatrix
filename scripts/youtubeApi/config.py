import json
from googleapiclient.discovery import build

API_KEY: str = "AIzaSyAgwzSCHzY0_nLZPzOzQ3jSoWatEI6Njsk"
YOUTUBE = build("youtube", "v3", developerKey=API_KEY)