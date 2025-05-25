#Plant identifier web application
#Built using streamlit and plant.id API
import streamlit as st
import requests #Allows your Python app to send HTTP requests (like GET, POST) to APIs.
from PIL import Image #Pillow (PIL) is a library for opening, manipulating, and saving images. And Image is the core module for handling image files.
import io #Provides tools for handling byte streams (useful for converting images/data into bytes).
import time #provides time functions 
import base64

# Set page config
st.set_page_config(
    page_title="Vanaspati Vigyan - Plant Identifier",
    page_icon="🌿",
    layout="centered",
)

# Custom CSS for the entire application
st.markdown(
    """
    <style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(rgba(5, 25, 15, 0.95), rgba(5, 25, 15, 0.95)), 
                    url('https://images.unsplash.com/photo-1534710961216-75c88202f43e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: #f0f0f0;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #2E8B57, #3CB371);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #3CB371, #2E8B57);
    }
    
    /* File uploader styling */
    .stFileUploader>div>div {
        background: rgba(255, 255, 255, 0.1);
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px;
        padding: 2rem;
    }
    
    /* Custom classes for plant info */
    .plant-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #3CB371;
        margin-bottom: 0.5rem;
    }
    
    .scientific-name {
        font-size: 1.2rem;
        font-style: italic;
        color: #98FB98;
        margin-bottom: 1.5rem;
    }
    
    .confidence-badge {
        background: rgba(46, 139, 87, 0.3);
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 1rem;
        display: inline-block;
    }
    
    .detail-card {
        background: rgba(30, 60, 40, 0.6);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .detail-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #98FB98;
        margin-bottom: 0.5rem;
    }
    
    /* Footer styling */
    .footer {
        padding: 2rem 0;
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem;
        margin-top: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main content
st.markdown("""
    <h1 style='color: white; margin-bottom: 0;'>Vanaspati Vigyan</h1>
    <div style='color: #98FB98; font-size: 1.1rem; margin-bottom: 2rem;'>
        Discover the secrets of the plant world
    </div>
""", unsafe_allow_html=True)

st.markdown("""
### 🌿 What is Vanaspati Vigyan?

Vanaspati Vigyan is a plant identification tool that helps users discover and learn about various plant species.
Simply upload an image of a plant, and the system provides its name, scientific classification, common names, and key details.
Designed for nature enthusiasts, gardeners, and botanists, it offers an easy way to explore the fascinating world of plants. 
The tool combines botanical knowledge with technology to deliver accurate and informative results.
""")

st.markdown("""
<div style="background: rgba(30, 60, 40, 0.6); padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem;">
    <p style="line-height: 1.6;">
        Upload an image of a plant to identify its species and learn more about it.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* Target the file uploader label */
    .stFileUploader label {
        color: white !important;
        font-size: 1rem;
    }
    
    /* Optional: Style the help text too */
    .stFileUploader .stTooltipIcon {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Image upload section
uploaded_file = st.file_uploader(
    "Upload a plant image",
    type=["jpg", "jpeg", "png", "webp"],
    help="Upload a clear image of a plant for identification"
)

# If image is uploaded, process it
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    st.markdown("""
    <div style="margin: 1.5rem 0;">
        <h3 style="color: #98FB98;">Your Plant Image</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.image(image, use_container_width=True, caption="Uploaded Plant Image")

    # Show loading spinner while processing
    with st.spinner("Analyzing plant characteristics..."):
        # Prepare API Request
        api_key = "R4zprk0cN6u9KiDiSe8y4hrUeJvKtP73dM0FY0oCM6ASP5oxj3"
        api_url = "https://api.plant.id/v2/identify"
        
        # Convert image to bytes
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()
        base64_image = base64.b64encode(img_bytes).decode("utf-8")
        
        # Prepare request data
        headers = {
            "Content-Type": "application/json",
            "Api-Key": api_key
        }
        data = {
            "images": [base64_image],
            "similar_images": True,
            "plant_details": ["common_names", "url", "wiki_description", "taxonomy"]
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            
            # Extract plant name & confidence
            data = response.json()
            if data["suggestions"]:
                best_match = data["suggestions"][0]
                plant_name = best_match["plant_name"]
                confidence = best_match["probability"] * 100
                
                # Display Results
                st.markdown(f"""
                <div style="background: rgba(20, 50, 30, 0.7); padding: 1.5rem; border-radius: 12px; margin: 1.5rem 0;">
                    <div class="plant-header">🌿 {plant_name}</div>
                    <div class="scientific-name">
                        {best_match["plant_details"]["scientific_name"] if "plant_details" in best_match and "scientific_name" in best_match["plant_details"] else "Scientific name not available"}
                    </div>
                    <div style="margin: 1rem 0;">
                        <span class="confidence-badge">Confidence: {confidence:.1f}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Create two columns for details
                col1, col2 = st.columns(2)
                
                with col1:
                    # Description card
                    if "plant_details" in best_match and "wiki_description" in best_match["plant_details"]:
                        description = best_match["plant_details"]["wiki_description"]["value"] if isinstance(best_match["plant_details"]["wiki_description"], dict) else best_match["plant_details"]["wiki_description"]
                        st.markdown(f"""
                        <div class="detail-card">
                            <div class="detail-title">📝 Description</div>
                            <p>{description[:500]}{'...' if len(description) > 500 else ''}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Taxonomy card
                    if "plant_details" in best_match and "taxonomy" in best_match["plant_details"]:
                        taxonomy = best_match["plant_details"]["taxonomy"]
                        st.markdown(f"""
                        <div class="detail-card">
                            <div class="detail-title">🧬 Taxonomy</div>
                            <p><strong>Genus:</strong> {taxonomy.get('genus', 'Unknown')}</p>
                            <p><strong>Family:</strong> {taxonomy.get('family', 'Unknown')}</p>
                            <p><strong>Order:</strong> {taxonomy.get('order', 'Unknown')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    # Common names card
                    if "plant_details" in best_match and "common_names" in best_match["plant_details"]:
                        common_names = ", ".join(best_match["plant_details"]["common_names"][:3])
                        st.markdown(f"""
                        <div class="detail-card">
                            <div class="detail-title">🏷️ Common Names</div>
                            <p>{common_names}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # More information card
                    if "plant_details" in best_match and "url" in best_match["plant_details"]:
                        st.markdown(f"""
                        <div class="detail-card">
                            <div class="detail-title">🔍 More Information</div>
                            <p><a href="{best_match['plant_details']['url']}" target="_blank" style="color: #98FB98;">Official Plant Database</a></p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Show top 3 similar matches
                if len(data["suggestions"]) > 1:
                    st.markdown("""
                    <div style="margin: 1.5rem 0;">
                        <h3 style="color: #98FB98;">Other Possible Matches</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for i, suggestion in enumerate(data["suggestions"][1:4], 1):
                        conf = suggestion["probability"] * 100
                        st.markdown(f"""
                        <div class="detail-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <strong>{i}. {suggestion["plant_name"]}</strong>
                                    <div style="color: #98FB98; font-size: 0.9rem;">
                                        {suggestion["plant_details"]["scientific_name"] if "plant_details" in suggestion and "scientific_name" in suggestion["plant_details"] else ""}
                                    </div>
                                </div>
                                <span class="confidence-badge">{conf:.1f}%</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
            else:
                st.error("We couldn't identify a plant in this image. Please try with a clearer photo.")
        
        except requests.exceptions.RequestException as e:
            st.error("We encountered an issue processing your request. Please try again later.")

# Footer
st.markdown("""
<div class="footer">
    <div>
        © 2025 Vanaspati Vigyan | Plant Identification System<br>
        Created with ❤️ by Shreya Joshi | Powered by Streamlit & Plant.id API
    </div>
</div>
""", unsafe_allow_html=True)




# #THE BASIC LOGIC
# # Plant identifier web application
# # Built using streamlit and plant.id API

# import streamlit as st
# import requests
# from PIL import Image
# import io
# import time
# import base64  # Added for base64 encoding


# # Set page config (Appears in Browser Tab)
# st.set_page_config(
#    page_title="Prakriti Darshan - Plant identifier",
#    page_icon="🪴",
#    layout="centered",
# )

# st.markdown(
  
#     <style>
#     .stApp {
#         background-color: #f0f8f0;  /* Light green background */
#     }
#     .stFileUploader > div > div {
#         border: 2px dashed #4CAF50 !important;  /* Green border for upload box */
#     }
#     .css-1aumxhk {
#         font-family: 'Arial', sans-serif;
#     }
#     </style>
    
#     unsafe_allow_html=True,
# )

# # App Description
# st.title("Prakriti Darshan")
# st.markdown("Upload a plant image and discover its name")

# # image upload section
# uploaded_file = st.file_uploader(
#     "Upload a plant image..",
#     type=["jpg", "jpeg", "png"],
#     help="Drag & drop or click to upload",
# )

# # if image is uploaded, process it
# if uploaded_file is not None:
#     # display the image
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Upload Plant Image", use_container_width=True)

#     # show loading spinner while processing
#     with st.spinner("Identifying the plant..."):
#         # Prepare API Request
#         api_key = "R4zprk0cN6u9KiDiSe8y4hrUeJvKtP73dM0FY0oCM6ASP5oxj3"
#         api_url = "https://api.plant.id/v2/identify"

#         # Convert image to base64
#         img_bytes = io.BytesIO()
#         image.save(img_bytes, format="PNG")
#         base64_image = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

#         # Prepare request data
#         headers = {
#             "Content-Type": "application/json",
#             "Api-Key": api_key
#         }
#         data = {
#             "images": [base64_image],
#             "modifiers": ["similar_images"],
#             "plant_details": ["common_names", "url"]
#         }

#         try:
#             response = requests.post(api_url, headers=headers, json=data)  # Fixed this line
#             response.raise_for_status()  # checks for errors
            
#             # extract plant name & confidence
#             data = response.json()
#             if data["suggestions"]:
#                 best_match = data["suggestions"][0]
#                 plant_name = best_match["plant_name"]
#                 confidence = best_match["probability"] * 100

#                 # Display Results
#                 st.success(f"**Identified Plant:** {plant_name}")
#                 st.metric("Confidence Level", f"{confidence:.2f}%")

#                 # Additional Details (if available)
#                 if "plant_details" in best_match:
#                     st.subheader("🌱 Plant Details")
#                     st.write(best_match["plant_details"])

#             else:
#                 st.warning("No plant identified. Try a clearer image!")
               
#         except requests.exceptions.RequestException as e:
#             st.error(f"API Error: {e}")

# Footer
# st.markdown("---")
# st.caption("Made with ❤️ by Shreya Joshi | Powered by Streamlit & Plant.id API")
