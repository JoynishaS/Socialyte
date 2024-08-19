import streamlit
import requests
import json

def getAuthorID():
    url = "https://api.linkedin.com/v2/me"
    response = requests.get(
        url
    )
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    return data['id']

def postToLinkedIn(postText,accessToken):
    authorID = getAuthorID()
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    body = json.dumps({
      "author": "urn:li:organization:%s"%(authorID),
      "commentary": "%s"%(postText),
      "visibility": "PRIVATE",
      "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
      },
      "lifecycleState": "PUBLISHED",
      "isReshareDisabledByAuthor": False
})
    headers = {
        'Authorization': 'Bearer %s'%(accessToken),
        'X-Restli-Protocol-Version': '2.0.0',
        'LinkedIn-Version': '202304',
        'Content-Type': 'application/json'
    }
    response = requests.post(
        url,
        headers=headers,
        data=body
    )
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    return data.text

streamlit.write(postToLinkedIn())

