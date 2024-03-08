from scripts import YOUTUBE
import json

__all__ = ["get_channel_id_by_name",
           "get_playlist_id",
           "get_video_ids_by_playlist_id", 
           "get_video_details", 
           "get_video_comments", 
           "make_video_details_comments"]

def get_channel_id_by_name(channel_name: str) -> str:
    request = YOUTUBE.search().list(
        q = channel_name, 
        type = "channel", 
        part = "id", 
        maxResults = 1
    )    
    response = request.execute()
    channel_id = response["items"][0]["id"]["channelId"]
    return channel_id

def get_playlist_id(channel_id: str) -> str:
    request = YOUTUBE.channels().list(
        part = "contentDetails", 
        id = channel_id
    )
    response = request.execute()
    return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

def get_video_ids_by_playlist_id(playlist_id: str) -> list[str]:
    full_video_details = []
    next_page_token = None
    
    while True:
        request = YOUTUBE.playlistItems().list(
            playlistId = playlist_id, 
            part = "snippet",
            maxResults = 50,
            pageToken = next_page_token
        )
        response = request.execute()
        full_video_details += response["items"]
        
        next_page_token = response.get("nextPageToken")
        if next_page_token is None:
            break
        
    video_ids = []
    for video in full_video_details:
        id = video["snippet"]["resourceId"]["videoId"]
        video_ids.append(id)
        
    return video_ids

def get_video_details(video_id: str):
    request = YOUTUBE.videos().list(
        part = "snippet, contentDetails, statistics", 
        id = video_id
    )
    response = request.execute()
    return response

def get_video_comments(video_id: str):
    request = YOUTUBE.commentThreads().list(
        part = "snippet", 
        videoId = video_id,
        textFormat = "plainText",
        maxResults = 10
    )
    response = request.execute()
    return response

def make_video_details_comments(name_od_id: str, streamlit_option: str):
    
    if streamlit_option == "channel name":
        channel_id = get_channel_id_by_name(name_od_id)
    else:
        channel_id = name_od_id
    
    playlist_id = get_playlist_id(channel_id)
    video_ids = get_video_ids_by_playlist_id(playlist_id)
    
    request = YOUTUBE.channels().list(
        id = channel_id, 
        part = "snippet, statistics"    
    )
    response = request.execute()
    
    channel_details = {
        "channel_name": response["items"][0]["snippet"]['title'], 
        "channel_id": response["items"][0]["id"], 
        "subscription_count": response["items"][0]["statistics"]["subscriberCount"], 
        "channel_views": response["items"][0]["statistics"]["viewCount"],
        "channel_description": response["items"][0]["snippet"]["description"]
    }
    
    video_details = []
    for index, id in enumerate(video_ids):
        data = get_video_details(id)
        
        comments_data = []
        if ("commentCount" not in data["items"][0]["statistics"]) or (data["items"][0]["statistics"]["commentCount"] == "0"):
            comment = "comment disabled"
        else:
            comment_request = YOUTUBE.commentThreads().list(
                part = "snippet", 
                videoId = id,
                textFormat = "plainText",
                maxResults = 10
            )
            comment_response = comment_request.execute()
            
            for number, comment in enumerate(comment_response["items"]):
                single_comment = {
                    f"comment_{number}": {
                        "comment_id": comment["id"],
                        "comment_text": comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
                        "comment_author": comment["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                        "published_at": comment["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                    }
                }
                comments_data.append(single_comment)       
        appending_video_data = {
            f"video_{index}": {
                "video_id": data["items"][0]["id"], 
                "video_name": data["items"][0]["snippet"]['title'], 
                "video_description": data["items"][0]["snippet"]['description'],
                "pubilished_at": data["items"][0]["snippet"]['publishedAt'], 
                "view_count": data["items"][0]["statistics"]["viewCount"], 
                "like_count": data["items"][0]["statistics"]["likeCount"],
                "comment_count": data["items"][0]["statistics"]["commentCount"],
                "duration": data["items"][0]["contentDetails"]["duration"], 
                "thumbnail": data["items"][0]["snippet"]["thumbnails"]["default"]['url'],
                "comments": comments_data
            }
        }
        video_details.append(appending_video_data)

    total_video_and_comments_details = {
        "channel_details": channel_details, 
        "video_details": video_details
    }
        
    return total_video_and_comments_details

