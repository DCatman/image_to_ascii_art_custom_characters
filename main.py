import streamlit as st
from PIL import Image, ImageEnhance, ImageOps
import numpy as np


def image_to_ascii(image, width=100, custom_chars="@%#*+=-:. "):
    # Konwertuj obraz do odcieni szarości
    image = image.convert("L")
    aspect_ratio = image.height / image.width
    new_height = int(aspect_ratio * width * 0.55)
    image = image.resize((width, new_height))

    # Jeśli custom_chars jest pusty, ustaw domyślne znaki
    if not custom_chars:
        custom_chars = "@%#*+=-:. "

    # Konwertuj piksele na ASCII znaki
    pixels = np.array(image.getdata())
    interval = 255 // (len(custom_chars) - 1)
    ascii_str = "".join([custom_chars[pixel // interval] for pixel in pixels])
    ascii_str_len = len(ascii_str)

    # Podziel na linie
    ascii_image = "\n".join([ascii_str[index:index + width] for index in range(0, ascii_str_len, width)])
    return ascii_image


def enhance_image(image, brightness, contrast, saturation, grayscale, invert_colors):
    if grayscale:
        image = ImageOps.grayscale(image)
    if invert_colors:
        image = ImageOps.invert(image)
    image = ImageEnhance.Brightness(image).enhance(brightness)
    image = ImageEnhance.Contrast(image).enhance(contrast)
    image = ImageEnhance.Color(image).enhance(saturation)
    return image


# Główna funkcja aplikacji
def main():
    st.set_page_config(layout="wide")
    st.title("ASCII Art Creator")

    # Układ kolumn
    col1, col2 = st.columns([1, 3])

    with col1:
        st.header("Import Image")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image.', use_column_width=True)

            st.header("Adjust Image")
            width = st.slider("Width", min_value=50, max_value=300, value=100)
            brightness = st.slider("Brightness", min_value=0.1, max_value=3.0, value=1.0)
            contrast = st.slider("Contrast", min_value=0.1, max_value=3.0, value=1.0)
            saturation = st.slider("Saturation", min_value=0.0, max_value=3.0, value=1.0)
            grayscale = st.checkbox("Grayscale")
            invert_colors = st.checkbox("Invert Colors")

            custom_chars = st.text_input("Custom Characters", value="@%#*+=-:. ")

            enhanced_image = enhance_image(image, brightness, contrast, saturation, grayscale, invert_colors)
            ascii_art = image_to_ascii(enhanced_image, width, custom_chars)

            with col2:
                st.code(ascii_art, language="plaintext")
        else:
            st.write("Please upload an image to get started.")

    with col2:
        if uploaded_file is None:
            st.write("ASCII Art will be displayed here after conversion.")
        else:
            st.write("No image uploaded yet.")


if __name__ == "__main__":
    main()
