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

# --- CUSTOM CSS (FINAL DESKTOP + MOBILE FIX) ---
st.markdown(f"""
    <style>
    /* Global Settings */
    * {{
        box-sizing: border-box;
    }}

    /* 1. HEADER & FOOTER (High Z-Index on Desktop) */
    .fixed-header {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 90px;
        background-color: #f1f1f1 !important;
        color: #000000 !important;
        z-index: 100000; /* High Z-index ensures it sits over main content */
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-family: sans-serif;
    }}

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
        z-index: 100000;
    }}

    .footer a {{
        color: #0066cc !important;
        text-decoration: none;
        font-weight: bold;
    }}

    /* 2. ADJUST MAIN CONTENT */
    .block-container {{
        padding-top: 110px; /* Push content down so header doesn't hide it */
        padding-bottom: 80px;
    }}

    /* 3. SIDEBAR FIXES (The Critical Part) */
    
    /* Make the Sidebar start BELOW the header on Desktop */
    section[data-testid="stSidebar"] {{
        top: 90px !important; /* Move sidebar down by height of header */
        height: calc(100vh - 90px) !important; /* Adjust height */
        z-index: 99999 !important; /* Just below the header */
    }}

    /* 4. STREAMLIT DEFAULT HEADER (Hamburger Menu) */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        z-index: 100001 !important; /* Button must be ON TOP of everything */
        height: 90px; /* Match our custom header height */
    }}
    
    /* Move hamburger button to right position if needed */
    header[data-testid="stHeader"] button {{
        color: black !important; 
    }}

    /* --- MOBILE SPECIFIC OVERRIDES --- */
    @media only screen and (max-width: 600px) {{
        /* On mobile, Sidebar must cover everything */
        section[data-testid="stSidebar"] {{
            top: 0px !important;
            height: 100vh !important;
            z-index: 100002 !important; /* On top of header */
        }}
        
        /* Adjust Header for Mobile */
        .fixed-header {{
            height: 70px;
            padding: 0 10px;
            z-index: 1000; /* Lower z-index so sidebar can cover it */
        }}

        .header-logo {{ height: 40px; margin-right: 8px; }}
        .header-title h1 {{ font-size: 16px; }}
        .header-btn {{ font-size: 12px; padding: 8px 12px; }}
        
        .block-container {{ padding-top: 80px; }}
        
        /* Shift logo right to avoid overlapping hamburger menu */
        .header-left {{ margin-left: 50px; }}
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
