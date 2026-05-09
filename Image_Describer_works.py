import ollama
import streamlit as st
from io import BytesIO

st.set_page_config(page_title="AI Image Describer", layout="centered")
st.title("📸 Image Describer (Local AI)")

# 1. File Uploader
uploaded_files = st.file_uploader(
    "Choose images to describe", 
    accept_multiple_files=True, 
    type=["jpg", "jpeg", "png"]
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Display the image in the UI
        st.image(uploaded_file, caption=f'Processing: {uploaded_file.name}', use_container_width=True)
        
        with st.spinner(f"Analyzing {uploaded_file.name}..."):
            try:
                # 2. Convert the uploaded file into BYTES
                # This bypasses the need for the file to exist on your hard drive
                image_bytes = uploaded_file.getvalue()

                # 3. Send bytes directly to Ollama
                # We use llava (ensure you have run: ollama pull llava)
                response = ollama.chat(
                    model='llava:7b', 
                    messages=[
                        {
                            'role': 'user',
                            'content': 'Describe this image in detail.',
                            'images': [image_bytes] # Passing bytes instead of a filename string
                        }
                    ]
                )

                # 4. Show the result
                st.subheader(f"Description for {uploaded_file.name}:")
                st.write(response['message']['content'])
                st.divider()

            except Exception as e:
                st.error(f"Error analyzing {uploaded_file.name}: {e}")
                st.info("Make sure you have the 'llava' model installed: run 'ollama pull llava' in terminal.")
else:
    st.info("Upload one or more images to get started.")