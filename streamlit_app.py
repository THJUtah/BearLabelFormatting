import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="Label Print Tool", layout="centered")

st.title("🐝 The Honey Jar - Label Print Tool")
st.markdown("""
Upload your PDF label below.  
The tool will rotate it 90°, duplicate it 3 times with 1/8" spacing,  
and export a 3.625\" × 1\" printable PDF.
""")

uploaded_file = st.file_uploader("Upload a single-page PDF label", type=["pdf"])

if uploaded_file:
    try:
        spacing_inches = 0.125
        dpi = 300
        output_pdf_filename = "processed_label.pdf"

        # Load the PDF from upload
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Rotate image 90° clockwise
        rotated_img = img.rotate(-90, expand=True)

        # Calculate image sizes
        img_width_in = 1.125
        img_height_in = 1.0
        spacing_px = int(spacing_inches * dpi)
        img_width_px = int(img_width_in * dpi)
        img_height_px = int(img_height_in * dpi)

        resized_img = rotated_img.resize((img_width_px, img_height_px))
        total_width_px = img_width_px * 3 + spacing_px * 2
        final_img = Image.new("RGB", (total_width_px, img_height_px), color="white")

        for i in range(3):
            x = i * (img_width_px + spacing_px)
            final_img.paste(resized_img, (x, 0))

        # Save to in-memory buffer
        output_buffer = io.BytesIO()
        final_img.save(output_buffer, "PDF", resolution=dpi)
        output_buffer.seek(0)

        # Display download link
        st.success("✅ PDF processed successfully!")
        st.download_button(
            label="📥 Download Processed PDF",
            data=output_buffer,
            file_name=output_pdf_filename,
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")
