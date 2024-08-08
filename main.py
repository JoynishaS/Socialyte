import streamlit

image_request = streamlit.text_input("Enter text for the type of image you want","A cute white bunny with blue eyes")
streamlit.write(image_request)