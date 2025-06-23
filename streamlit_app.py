import streamlit as st
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="Label Print Tool", layout="centered")

st.title("🐝 The Honey Jar - Label Print Tool")
st.markdown("""
Upload your **vector-based PDF label** below.  
This tool will rotate it 90°, duplicate it 3× with 1/8" spacing,  
and export a print-ready PDF (3.625" × 1").
""")

uploaded_file = st.file_uploader("Upload a single-page vector PDF label", type=["pdf"])

if uploaded_file:
    try:
        spacing_in = 0.125
        label_width_in = 1.125
        label_height_in = 1.0
        dpi = 300

        # Calculate dimensions in points (1 inch = 72 points)
        spacing_pt = spacing_in * 72
        label_width_pt = label_width_in * 72
        label_height_pt = label_height_in * 72
        total_width_pt = (label_width_pt * 3) + (spacing_pt * 2)
        total_height_pt = label_height_pt

        # Load original PDF
        src_pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        if len(src_pdf) != 1:
            st.error("Please upload a single-page PDF.")
            st.stop()

        # Create new PDF
        new_pdf = fitz.open()
        new_page = new_pdf.new_page(width=total_width_pt, height=total_height_pt)

        for i in range(3):
            x_offset = i * (label_width_pt + spacing_pt)
            # Use rotation argument instead of transformation matrix
            new_page.show_pdf_page(
                fitz.Rect(x_offset, 0, x_offset + label_width_pt, label_height_pt),
                src_pdf,
                0,
                rotate=90
            )

        # Save to buffer
        output_buffer = io.BytesIO()
        new_pdf.save(output_buffer)
        output_buffer.seek(0)

        st.success("✅ PDF processed successfully!")
        st.download_button(
            label="📥 Download Processed PDF",
            data=output_buffer,
            file_name="processed_label.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
