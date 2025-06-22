import requests
import random
from duckduckgo_search import DDGS
from PIL import Image
from io import BytesIO
import streamlit as st

# Set your Pexels API key here
PEXELS_API_KEY = 'Cq9mU0J9TEzIEquCTOSdFt5pXsJBMItWgJxthwUbzx7jMw1uD8OdPBUa'

# Function to fetch one image from DuckDuckGo using the duckduckgo_search library
def fetch_duckduckgo_image(query):
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.images(query, max_results=1)]
        if results:
            return results[0]['image']
    except Exception as e:
        print(f"DuckDuckGo error: {e}")
    return None

# Function to fetch one image from Pexels
def fetch_pexels_image(query):
    url = f'https://api.pexels.com/v1/search?query={query}&per_page=1'
    headers = {'Authorization': PEXELS_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        photos = data.get('photos', [])
        if photos:
            return photos[0]['src']['original']
    return None

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Download error: {e}")
    return None

def show_images_grid(img1, img2):
    # Resize images to the same height
    if img1.height != img2.height:
        new_height = min(img1.height, img2.height)
        img1 = img1.resize((int(img1.width * new_height / img1.height), new_height))
        img2 = img2.resize((int(img2.width * new_height / img2.height), new_height))
    # Create grid
    grid = Image.new('RGB', (img1.width + img2.width, img1.height))
    grid.paste(img1, (0, 0))
    grid.paste(img2, (img1.width, 0))
    grid.show()

def main():
    st.set_page_config(page_title="Neptune AI", layout="centered")
    st.markdown(
        """
        <style>
        .liquid-glass {
            background: rgba(255, 255, 255, 0.15);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.18);
            padding: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
    st.title("🧊 Neptune AI")
    prompt = st.text_input("Enter the image you want  to generate with Neptune AI using (duckduckgo ,pexels)")
    if st.button("Generate Images") and prompt:
        with st.spinner('Generating images...'):
            duck_url = fetch_duckduckgo_image(prompt)
            pexel_url = fetch_pexels_image(prompt)
        if duck_url and pexel_url:
            img1 = download_image(duck_url)
            img2 = download_image(pexel_url)
            if img1 and img2:
                col1, col2 = st.columns(2)
                with col1:
                    img1_bytes = BytesIO()
                    img1.save(img1_bytes, format='PNG')
                    st.image(img1, caption="Neptune AI", use_container_width=True)
                    st.download_button(
                        label="Download Image ",
                        data=img1_bytes.getvalue(),
                        file_name="Neptune_image_duckduckgo.png",
                        mime="image/png"
                    )
                with col2:
                    img2_bytes = BytesIO()
                    img2.save(img2_bytes, format='PNG')
                    st.image(img2, caption="Neptune AI", use_container_width=True)
                    st.download_button(
                        label="Download Image",
                        data=img2_bytes.getvalue(),
                        file_name="Neptune_image_pexels.png",
                        mime="image/png"
                    )
            else:
                st.error('Could not capable for  advance images.')
        else:
            st.error('Could not capable for  advance images.')
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
