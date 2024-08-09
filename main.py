import streamlit
from openai import OpenAI
import os

client = OpenAI(
    organization='org-R2DDZN0eVGgEosD61XGShpU8',
    api_key = streamlit.secrets['OPENAI_API_KEY'],
    project='proj_fqZ8kTAr98ZSgzH5cEdb8mGW'
)

imageModificationChoice = streamlit.radio(
    "Generate an image, Upload an image, Revised Uploaded Image",
    ["***Generate Image by Text***", "***Upload Image to be posted as is***", "***Upload image to be randomly revised***"],
    index=None,
)

match imageModificationChoice:
    case "***Generate Image by Text***":
        image_request = streamlit.text_input("Enter text for the type of image you want","A cute white bunny with blue eyes")
        streamlit.session_state['image_request'] = image_request
    case "***Upload Image to be posted as is***":
        uploaded_file = streamlit.file_uploader("Choose a 1024x1024 png image",type = ['png'])
        if uploaded_file is not None:
            image_request = uploaded_file.getvalue()
            streamlit.session_state['image_request'] = image_request
    case "***Upload image to be randomly revised***":
        uploaded_file = streamlit.file_uploader("Choose a 1024x1024 png image", type=['png'])
        if uploaded_file is not None:
            image_request = uploaded_file.getvalue()
            streamlit.session_state['image_request'] = image_request

topic_request = streamlit.text_input("Enter a topic for your post","How pretty white bunnies with blue eyes are")
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
        case "***Upload Image to be posted as is***":
            uploaded_file = streamlit.file_uploader("Choose a 1024x1024 png image", type=['png'])
            if uploaded_file is not None:
                data_response = sendToOpenAI(streamlit.session_state['image_request'])
                streamlit.session_state['image'] = data_response.data[0].url
        case "***Upload image to be randomly revised***":
            uploaded_file = streamlit.file_uploader("Choose a 1024x1024 png image", type=['png'])
            if uploaded_file is not None:
                data_response = sendToOpenAI(streamlit.session_state['image_request'])
                streamlit.session_state['image'] = data_response.data[0].url



if streamlit.button("Submit", type="primary"):
    streamlit.write("We will send to Open AI Here and return the post in ",translation_request)
    text_returned = streamlit.text_area("This is the text OpenAI Returned","Text that was returned")
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