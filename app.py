import streamlit as st
from graph_engine import ProductGraph
import os
import base64
import streamlit.components.v1 as components 

# --- PAGE CONFIGURATION ---
favicon = "Rlogo - Product Recommendation.png"
if not os.path.exists(favicon):
    favicon = "🛒"

st.set_page_config(
    page_title="Shopkeeper AI | Rehmah Projects",
    page_icon=favicon,
    layout="wide"
)

# --- GOOGLE ANALYTICS TRACKING ---
components.html("""
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-88H1ZZYWY2"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-88H1ZZYWY2');
    </script>
""", height=0)

# --- HELPER: IMAGE TO BASE64 ---
def get_img_as_base64(file):
    try:
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return None

logo_b64 = get_img_as_base64("Rlogo - Product Recommendation.png")
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="header-logo">' if logo_b64 else '<span style="font-size: 30px;">🛒</span>'

# --- CUSTOM CSS (FINAL MOBILE FIX) ---
st.markdown(f"""
    <style>
    /* Global Settings */
    * {{
        box-sizing: border-box;
    }}

    /* 1. CUSTOM HEADER (Lower Z-Index) */
    .fixed-header {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 90px;
        background-color: #f1f1f1 !important;
        color: #000000 !important;
        z-index: 90; /* Lower than Sidebar (which is usually around 100) */
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-family: sans-serif;
    }}

    /* 2. CUSTOM FOOTER */
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1 !important;
        color: #333 !important;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        border-top: 1px solid #ccc;
        z-index: 90;
    }}

    .footer a {{
        color: #0066cc !important;
        text-decoration: none;
        font-weight: bold;
    }}

    /* 3. STREAMLIT HEADER & HAMBURGER MENU */
    /* Make the default header transparent but keep the button clickable */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        z-index: 100 !important; /* Above custom header */
        height: 90px;
    }}
    
    /* Force the hamburger menu to be black and visible */
    header[data-testid="stHeader"] button {{
        color: black !important;
        z-index: 101 !important;
    }}

    /* 4. SIDEBAR BEHAVIOR (The Fix) */
    
    /* DESKTOP: Sidebar starts below header */
    @media (min-width: 601px) {{
        section[data-testid="stSidebar"] {{
            top: 90px !important;
            height: calc(100vh - 90px) !important;
        }}
    }}

    /* MOBILE: Sidebar covers everything */
    @media (max-width: 600px) {{
        section[data-testid="stSidebar"] {{
            top: 0px !important;
            height: 100vh !important;
            z-index: 99999 !important; /* Super high Z-index to cover header */
        }}
        
        /* Shift logo right so it doesn't sit under the hamburger button */
        .header-left {{
            margin-left: 50px; 
        }}
        
        /* Adjust header height for mobile */
        .fixed-header {{
            height: 70px;
            padding: 0 10px;
        }}
        
        .header-logo {{ height: 40px; margin-right: 8px; }}
        .header-title h1 {{ font-size: 16px; }}
        .header-btn {{ font-size: 12px; padding: 8px 12px; }}
        
        .block-container {{ padding-top: 80px; }}
    }}

    /* 5. CONTENT PADDING */
    .block-container {{
        padding-top: 110px;
        padding-bottom: 80px;
    }}

    /* Header Styling Details */
    .header-left {{ display: flex; align-items: center; overflow: hidden; }}
    .header-logo {{ height: 60px; width: auto; margin-right: 15px; }}
    .header-title h1 {{ margin: 0; font-size: 24px; font-weight: 700; color: #000; white-space: nowrap; }}
    .header-btn {{ background-color: #110945; color: white !important; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; border: none; white-space: nowrap; }}
    .header-btn:hover {{ background-color: #2a1b70; color: white !important; }}

    </style>
""", unsafe_allow_html=True)

# --- INJECT HEADER HTML ---
st.markdown(f"""
    <div class="fixed-header">
        <div class="header-left">
            {logo_html}
            <div class="header-title">
                <h1>Product Rec. App</h1>
            </div>
        </div>
        <a href="https://rehmahprojects.com/projects.html" target="_blank" class="header-btn">More Projects</a>
    </div>
""", unsafe_allow_html=True)

# --- INJECT FOOTER HTML ---
st.markdown("""
    <div class="footer">
        <p>Powered by <b>Rehmah Projects</b> | 
        <a href="mailto:admin@rehmahprojects.com">admin@rehmahprojects.com</a></p>
    </div>
""", unsafe_allow_html=True)

# --- MAIN APP LOGIC ---

# Initialize Graph
@st.cache_resource
def load_graph():
    return ProductGraph("data.json")

try:
    kg = load_graph()
except FileNotFoundError:
    st.error("❌ 'data.json' not found. Please run the converter script first.")
    st.stop()

# --- SIDEBAR INPUTS ---
st.sidebar.header("User Requirements")
product_map = kg.get_all_product_names()

if not product_map:
    st.sidebar.error("No products found in the graph.")
    st.stop()

selected_product_name = st.sidebar.selectbox("Select Product", list(product_map.values()))
selected_product_id = [k for k, v in product_map.items() if v == selected_product_name][0]

max_price = st.sidebar.number_input("Max Price (₹)", min_value=10, value=500, step=10)
required_tags = st.sidebar.multiselect("Required Attributes", ["Oil", "Rice", "Masala", "Snacks", "Dairy"])

# --- RESULTS SECTION ---
if st.sidebar.button("Find Product"):
    product_details = kg.get_product_details(selected_product_id)
    
    if product_details.get('in_stock', False):
        st.success(f"✅ **{product_details['name']}** is available!")
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Price", f"₹{product_details['price']}")
        with c2:
            st.metric("Status", "In Stock", delta_color="normal")
            
        st.json(product_details)
    else:
        st.error(f"❌ {product_details['name']} is **Out of Stock**.")
        st.markdown("### 🔍 Finding Best Alternatives (Graph Search)...")
        
        substitutes = kg.find_substitutes(selected_product_id, max_price, required_tags)
        
        if not substitutes:
            st.warning("No suitable alternatives found matching your constraints.")
        else:
            cols = st.columns(len(substitutes))
            for idx, sub in enumerate(substitutes):
                with cols[idx]:
                    with st.container(border=True):
                        st.subheader(sub['name'])
                        st.write(f"**Price:** ₹{sub['price']}")
                        
                        st.markdown("**Why this?**")
                        for rule in sub['reasons']:
                            if rule == 'same_brand_match':
                                st.caption(f"🔹 Same Brand")
                            elif rule == 'cheaper_option':
                                st.caption(f"💰 Cheaper Option")
                            elif rule == 'same_category':
                                st.caption(f"📂 Same Category")
                            elif rule == 'diff_brand_alternative':
                                st.caption(f"🔸 Different Brand")
                            elif rule == 'premium_option':
                                st.caption(f"💎 Premium Option")
