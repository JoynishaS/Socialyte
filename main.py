import streamlit
from openai import OpenAI
import os
from io import StringIO

client = OpenAI(
    organization='org-R2DDZN0eVGgEosD61XGShpU8',
    api_key = streamlit.secrets['OPENAI_API_KEY'],
    project='proj_fqZ8kTAr98ZSgzH5cEdb8mGW'
)

imageModificationChoice = streamlit.radio(
    "Generate an image, Upload your own image",
    ["***Generate Image by Text***", "***Upload your own Image***"],
    index=None,
)

match imageModificationChoice:
    case "***Generate Image by Text***":
        image_request = streamlit.text_input("Enter text for the type of image you want","A cute white bunny with blue eyes")
        streamlit.session_state['image_request'] = image_request
    case "***Upload your own Image***":
        uploaded_file = streamlit.file_uploader("Choose a 1024x1024 png image",type = ['png'])
        if uploaded_file is not None:
            streamlit.session_state['image'] = uploaded_file

topic_request = streamlit.text_input("Enter a topic for your post","Write a post for Twitter about the history of White Bunnies with Blue Eyes")
translation_request = streamlit.selectbox("What Language should the post be in?", ("EN", "ES"))
streamlit.write(topic_request)

def sendToOpenAI(description):
    return client.images.generate(
        model = "dall-e-3",
        prompt =description,
        n=1,
        size ="1024x1024"
    )

def imageWorkFlow():
    match imageModificationChoice:
        case "***Generate Image by Text***":
            data_response = sendToOpenAI(streamlit.session_state['image_request'])
            streamlit.session_state['image'] = data_response.data[0].url

def sendTextToOpenAI(userRequest):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": userRequest}
                ]
    )

if streamlit.button("Submit", type="primary"):
    streamlit.write("We will send to Open AI Here and return the post in ",translation_request)
    text_returned = sendTextToOpenAI(topic_request).choices[0].message.content
    streamlit.text_area("This is the text OpenAI Returned", text_returned)
    imageWorkFlow()
    #keeping this here for testing purposes right now
    streamlit.write(streamlit.session_state['image'])
    streamlit.session_state['key'] = text_returned


if 'key' in streamlit.session_state:
    platform_request = streamlit.selectbox("Which platform do you want to post on?", ("LINKEDIN", "TWITTER"))
    if streamlit.button("Post", type="primary"):
        streamlit.write("We Posted the content on ",platform_request)
        streamlit.write(streamlit.session_state['key'])

if 'image' in streamlit.session_state:
    streamlit.image(streamlit.session_state['image'])