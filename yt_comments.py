# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from utils.comments import process_comments,make_csv

load_dotenv()

API_KEY =os.getenv("API_KEY")
MAX_RESULTS = 200
DEVELOPER_KEY = "YOUR_API_KEY"
youtube = build(
    "youtube", "v3", developerKey = API_KEY)

def comment_threads(channelID,to_csv=False):
    comments_list = []

    request = youtube.commentThreads().list(
        part="id,snippet",
        # allThreadsRelatedToChannelId="UCNmgKwY9b4MoE04ZFrIWGVw",
        maxResults=200,
        order="time",
        videoId = channelID
    )
    response = request.execute()
    # print(response)

    comments_list.extend(process_comments(response['items']))

    while response.get('nextPageToken',None):
        request = youtube.commentThreads().list(
            part="id,snippet",
            # allThreadsRelatedToChannelId="UCNmgKwY9b4MoE04ZFrIWGVw",
            maxResults=200,
            order="time",
            videoId = channelID,
            pageToken=response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comments(response['items']))
    
    print(f'Finished fetching comments for {channelID}..{len(comments_list)} comments found..')

    # print(len(response['items']))
    # print(comments_list)


    if to_csv:
        make_csv(comments_list,channelID)

    return comments_list

def main():
    # comment_threads('UCNmgKwY9b4MoE04ZFrIWGVw')
    comment_threads('H0WaRIMzZQU',to_csv=True)

if __name__ == "__main__":
    main()