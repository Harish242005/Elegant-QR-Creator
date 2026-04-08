import os
import qrcode
import barcode
import streamlit as st
from PIL import Image
from barcode.writer import ImageWriter

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def detect_type(value):
    value = str(value).strip()
    if not value:
        return "invalid"
    elif value.startswith("http://") or value.startswith("https://"):
        return "qr"
    elif value.isdigit() and len(value) >= 8:
        return "barcode"
    else:
        return "qr"

def generate_qr(data, filename):
    img = qrcode.make(data)
    path = os.path.join(OUTPUT_DIR, f"{filename}.png")
    img.save(path)
    return path

def generate_barcode(data, filename):
    code128 = barcode.get("code128", data, writer=ImageWriter())
    return code128.save(os.path.join(OUTPUT_DIR, filename))

st.set_page_config(
    page_title="Smart QR & Barcode Generator",
    page_icon="🌈",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f9f7ff, #e0f7fa, #fff3e0);
    }
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #6a1b9a;
        margin-bottom: 8px;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #37474f;
        margin-bottom: 24px;
    }
    .card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        margin-bottom: 18px;
    }
    .small-note {
        color: #455a64;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌈 Smart QR & Barcode Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Create QR codes, barcodes, and image-based QR actions in one colorful app.</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔳 Manual Generator", "🖼️ Image Upload Tools"])

with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔤 Enter website, number, or text")
    user_input = st.text_input("Input value")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("✨ Generate Code"):
            with st.spinner("Creating your code..."):
                code_type = detect_type(user_input)

                if code_type == "invalid":
                    st.error("Please enter a value.")
                elif code_type == "qr":
                    path = generate_qr(user_input, "generated_qr")
                    st.success("QR code generated successfully.")
                    st.image(path, caption="Generated QR Code", width=280)
                    with open(path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download QR Code",
                            data=f.read(),
                            file_name="generated_qr.png",
                            mime="image/png"
                        )
                elif code_type == "barcode":
                    path = generate_barcode(user_input, "generated_barcode")
                    st.success("Barcode generated successfully.")
                    st.image(path, caption="Generated Barcode", width=420)
                    with open(path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Barcode",
                            data=f.read(),
                            file_name=os.path.basename(path),
                            mime="image/png"
                        )

    with col2:
        st.info("💡 Smart rules:\n- Website → QR\n- Long number → Barcode\n- Other text → QR")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🖼️ Upload an image")
    uploaded_image = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Preview of uploaded image", width=300)

        saved_image_path = os.path.join(OUTPUT_DIR, uploaded_image.name)

        with open(saved_image_path, "wb") as f:
            f.write(uploaded_image.getbuffer())

        st.success(f"Image saved successfully: {saved_image_path}")

        st.markdown("### Choose what to do with the uploaded image")

        colA, colB = st.columns(2)

        with colA:
            if st.button("📁 Generate QR from Image Path"):
                with st.spinner("Generating QR from image path..."):
                    qr_path = generate_qr(saved_image_path, "image_path_qr")
                    st.success("QR generated from image path.")
                    st.code(saved_image_path)
                    st.image(qr_path, caption="QR from Image Path", width=280)
                    with open(qr_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Path QR",
                            data=f.read(),
                            file_name="image_path_qr.png",
                            mime="image/png"
                        )

        with colB:
            if st.button("📝 Generate QR from Image Filename"):
                with st.spinner("Generating QR from image filename..."):
                    qr_name_path = generate_qr(uploaded_image.name, "image_name_qr")
                    st.success("QR generated from image filename.")
                    st.code(uploaded_image.name)
                    st.image(qr_name_path, caption="QR from Image Filename", width=280)
                    with open(qr_name_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Filename QR",
                            data=f.read(),
                            file_name="image_name_qr.png",
                            mime="image/png"
                        )

        st.markdown("""
        <div class="small-note">
        ✅ Image upload options included here:
        <br>• Preview + save image
        <br>• Create QR from saved image path
        <br>• Create QR from image filename
        <br><br>
        ⚠️ Note: these QR codes store text (path or filename), not the full image itself.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)