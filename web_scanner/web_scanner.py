import streamlit as st
import requests
import os
from openai import OpenAI
from bs4 import BeautifulSoup  # Thêm BeautifulSoup


client = OpenAI(
    api_key='sk-iINMXEGFa7FZDdNPriY314w40j02O0d3j0JdbZzIDqT3BlbkFJiqBmh6A0KW5RrssJifE9W4h6GLzN3lhsbWBnpTYR8A'
)

# Title of the app
st.title("Web Content Analyzer with GPT")

# Input for user to enter URL
url = st.text_input("Enter a URL to analyze:", placeholder="https://example.com")

# Button to start processing
if st.button("Analyze URL"):
    if url:
        try:
            # Fetch content from the URL
            st.info("Fetching content from the URL...")
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors
            content = response.text

            soup = BeautifulSoup(content, "html.parser")
            
            # Loại bỏ các thẻ CSS và Javascript
            for script_or_style in soup(['style', 'script']):
                script_or_style.decompose()  # Loại bỏ các thẻ style và script

            # Lấy văn bản thuần túy
            text_content = soup.get_text(separator="\n", strip=True)

            # Hiển thị văn bản thuần túy (bỏ qua CSS, JS)
            #st.subheader("Processed Content (Text only):")
            #st.text(text_content)  # Hiển thị nội dung văn bản thuần túy
            
            # Check the length of content
            if len(text_content) > 10000:  # Limit content length for GPT
                st.warning("The webpage content is too large, truncating it to 10,000 characters.")
                text_content = text_content[:10000]
            
            # Send content to OpenAI GPT for analysis
            st.subheader("Processed Content (via GPT):")
            with st.spinner("Processing content with GPT..."):
                try:
                    # Create a chat completion request
                    response = client.chat.completions.create(
                        model="gpt-4o",  # Use the appropriate model
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant that summarizes webpage content."},
                            {"role": "user", "content": text_content}
                        ]
                    )
                    summary = response.choices[0].message.content
                    st.success("Content processed successfully!")
                    st.write(summary)
                except Exception as e:
                   st.error(f"Error processing with GPT: {str(e)}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while fetching the URL: {str(e)}")
    else:
        st.warning("Please enter a valid URL.")
