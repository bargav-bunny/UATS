import os
import requests
import uuid
import json




endpoint = "https://projread.cognitiveservices.azure.com/"
subscription_key = os.getenv("IMAGE_RECO_KEY")


def getJSON(image_data):
    text_recognition_url = endpoint + "/vision/v3.0/read/analyze"
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    response = requests.post(text_recognition_url,
                             headers=headers, data=image_data)
    response.raise_for_status()
    operation_url = response.headers["Operation-Location"]
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
        if ("analyzeResult" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'failed'):
            poll = False
    return analysis
