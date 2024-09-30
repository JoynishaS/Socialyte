import streamlit
import requests
import json


#Get Access Token For LinkedIn
def getAccessTokenLinkedIn():
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    body = 'grant_type=authorization_code&code=%s&client_id=%s&client_secret=%s&redirect_uri=https://socialyte.streamlit.app/app'%(streamlit.query_params.code,streamlit.secrets['LINKEDIN_CLIENT_ID'],streamlit.secrets['LINKEDIN_CLIENT_SECRET'])
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.post(
        url,
        headers=headers,
        data=body
    )
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    return data['access_token']

#Get Author ID
def getAuthorID():
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {
        'Authorization': 'Bearer %s'%(streamlit.session_state['linkedInToken']),
    }
    body = {}
    response = requests.get(
        url,
        headers = headers,
        data = body
    )
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    return data['sub']

#Refresh Token since Streamlit reload scripts everytime a user interacts
def refreshToken():
    url = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={}&redirect_uri={}&state=magentosDomingo&scope=openid%20email%20profile%20w_member_social".format(
        streamlit.secrets['LINKEDIN_CLIENT_ID'], streamlit.secrets['LINKEDIN_REDIRECT_URL'])
    nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
    """ % (url)
    streamlit.write(nav_script, unsafe_allow_html=True)

#Post to LinkedIn
def postToLinkedIn():
    authorID = getAuthorID()
    if 'authorID' not in streamlit.session_state:
        streamlit.session_state['authorID'] = authorID

        imageData = initializeImageUpload()

        streamlit.session_state['uploadURL'] = imageData['value']['uploadUrl']
        streamlit.session_state['imageURN'] = imageData['value']['image']

        uploadImage()

    url = "https://api.linkedin.com/rest/posts"
    body = json.dumps({
      "author": "urn:li:person:%s"%(authorID),
      "commentary": "%s"%(streamlit.session_state['key']),
      "visibility": "PUBLIC",
      "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
      },
        "content": {
            "media": {
                "title": "",
                "id": "%s"%streamlit.session_state['imageURN']
            }
        },
      "lifecycleState": "PUBLISHED",
      "isReshareDisabledByAuthor": False
})
    headers = {
        'Authorization': 'Bearer %s'%(streamlit.session_state['linkedInToken']),
        'X-Restli-Protocol-Version': '2.0.0',
        'LinkedIn-Version': '202409',
        'Content-Type': 'application/json'
    }
    response = requests.post(
        url,
        headers=headers,
        data=body
    )
    if response.status_code != 201:
         streamlit.error(response.text)

    if response.status_code == 201:
        streamlit.success("Completed")
        refreshToken()

    data = response
    return data.text

#Initialize Image Upload
def initializeImageUpload():
    url = "https://api.linkedin.com/rest/images?action=initializeUpload"
    body = json.dumps({
    "initializeUploadRequest": {
        "owner": "urn:li:person:%s"%(streamlit.session_state['authorID'])
    }
})
    headers = {
        'Authorization': 'Bearer %s'%(streamlit.session_state['linkedInToken']),
        'X-Restli-Protocol-Version': '2.0.0',
        'LinkedIn-Version': '202307',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(
        url,
        headers=headers,
        data=body
    )

    data = response.json()
    return data

def uploadImage():
    url = streamlit.session_state['uploadURL']
    if streamlit.session_state['uploadMyOwnImage'] == False:
        download_image(streamlit.session_state['image'])
        image = open("image.jpg","rb").read()
    if streamlit.session_state['uploadMyOwnImage'] == True:
        image = open(streamlit.session_state['uploaded_image_url'], "rb").read()
    headers = {
        'Authorization': 'Bearer %s'%(streamlit.session_state['linkedInToken']),
    }
    if "uploadURL" in streamlit.session_state and 'imageURN' in streamlit.session_state:
        response = requests.put(
            url,
            headers=headers,
            data=image
        )
        data = response

#images have to be local for linkedin api so had to add this
def download_image(url):
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to download image!")
        exit()

    filename = "image.jpg"
    with open(filename, 'wb') as file:
        file.write(response.content)

    streamlit.success("Image uploaded successfully!")

