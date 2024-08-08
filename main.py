import streamlit

image_request = streamlit.text_input("Enter text for the type of image you want","A cute white bunny with blue eyes")
topic_request = streamlit.text_input("Enter a topic for your post","How pretty white bunnies with blue eyes are")
streamlit.write(image_request)
streamlit.write(topic_request)
if streamlit.button("Submit", type="primary"):
    streamlit.write("We will send to Open AI Here")