import streamlit as st
import pandas as pd 
import time 
from PIL import Image 
import os
from Home import add_logo


add_logo()
# st.title("Rhett Palmore's Treehouse")

st.markdown('''
### If you want, let's start by taking a commemorative photo together! (I promise it's innocent)
''')

if "photo" not in st.session_state:
    st.session_state["photo"] = "Not Done"

def change_photo_state():
    st.session_state["photo"] = "Done"

camera_photo = st.camera_input("Say Cheese", on_change=change_photo_state)

image_path = '/Users/rp/Desktop/Python Projects  (VS Code)/StreamLit/my_image.jpeg'
my_image = Image.open(image_path)

def concatenate_images(image1, image2):
    img1 = image1
    img2 = Image.open(image2)

    # Concatenate images horizontally
    concatenated_image = Image.new("RGB", (img1.width + img2.width, img1.height))
    concatenated_image.paste(img1, (0, 0))
    concatenated_image.paste(img2, (img1.width, 0))

    return concatenated_image

if st.session_state["photo"] == "Done":
    if camera_photo is not None:
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)

        # Save the uploaded file temporarily
        uploaded_file_path = "temp_uploaded_file.jpg"
        with open(uploaded_file_path, "wb") as f:
            f.write(camera_photo.getvalue())

        # Concatenate images
        result_image = concatenate_images(my_image, uploaded_file_path)

        # Display concatenated image with adjusted width
        st.image(result_image, use_column_width=True)

        # Save the result image temporarily for download
        result_image_path = "temp_result_image.jpg"
        result_image.save(result_image_path)

        st.download_button(
            label="You can download and frame it!",
            data=open(result_image_path, "rb").read(),
            file_name="Me_and_Rhett.jpg",
            key="download_button",
        )

        # Remove the temporary files
        st.session_state["photo"] = "Not Done"
        st.success("Photo Uploaded Successfully!")
        st.balloons()
        os.remove(uploaded_file_path)
        os.remove(result_image_path)
        st.write("That's all I've got for now. Website is a work in progress, please come back...")