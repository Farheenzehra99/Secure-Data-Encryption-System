# import streamlit as st
# import hashlib
# from cryptography.fernet import Fernet

# # Initialize session state
# if 'stored_data' not in st.session_state:
#     st.session_state.stored_data = {}
# if 'failed_attempts' not in st.session_state:
#     st.session_state.failed_attempts = 0
# if 'auth' not in st.session_state:
#     st.session_state.auth = False
# if 'fernet_key' not in st.session_state:
#     st.session_state.fernet_key = Fernet.generate_key()

# # Create cipher suite
# cipher = Fernet(st.session_state.fernet_key)

# def hash_passkey(passkey):
#     return hashlib.sha256(passkey.encode()).hexdigest()

# def encrypt_data(text):
#     return cipher.encrypt(text.encode()).decode()

# def decrypt_data(encrypted_text):
#     return cipher.decrypt(encrypted_text.encode()).decode()

# # Streamlit UI
# st.title("🔒 Secure Data Vault")

# # Navigation setup
# menu = ["Home", "Store Data", "Retrieve Data", "Login"]
# if st.session_state.failed_attempts >= 3:
#     st.session_state.choice = "Login"
# else:
#     if 'choice' not in st.session_state:
#         st.session_state.choice = "Home"

# # Force login if failed attempts exceeded
# if st.session_state.failed_attempts >= 3 and st.session_state.choice != "Login":
#     st.session_state.choice = "Login"

# # Sidebar navigation
# st.session_state.choice = st.sidebar.selectbox(
#     "Navigation",
#     menu,
#     index=menu.index(st.session_state.choice)
# )

# # Home Page
# if st.session_state.choice == "Home":
#     st.subheader("🏠 Welcome to Secure Data Vault")
#     st.markdown("""
#     ### Features:
#     - **Military-grade encryption** using Fernet (AES-128)
#     - **Secure passkey** hashing with SHA-256
#     - **Brute-force protection** with 3-attempt lockout
#     - **Zero external storage** - all data in memory
#     """)

# # Store Data Page
# elif st.session_state.choice == "Store Data":
#     st.subheader("📦 Store Sensitive Data")
    
#     with st.form("store_form"):
#         user_data = st.text_area("Data to encrypt:", height=150)
#         passkey = st.text_input("Set passkey:", type="password")
        
#         if st.form_submit_button("🔒 Encrypt & Store"):
#             if user_data and passkey:
#                 encrypted = encrypt_data(user_data)
#                 st.session_state.stored_data[encrypted] = {
#                     "passkey": hash_passkey(passkey),
#                     "encrypted_text": encrypted
#                 }
#                 st.success("Data encrypted successfully!")
#                 st.code(f"Encrypted Token: {encrypted}", language="text")
#             else:
#                 st.error("Both fields are required!")

# # Retrieve Data Page
# elif st.session_state.choice == "Retrieve Data" and st.session_state.auth:
#     st.subheader("🔍 Decrypt Your Data")
    
#     with st.form("retrieve_form"):
#         encrypted_text = st.text_area("Encrypted token:")
#         passkey = st.text_input("Enter passkey:", type="password")
        
#         if st.form_submit_button("🔓 Decrypt"):
#             if encrypted_text and passkey:
#                 if encrypted_text in st.session_state.stored_data:
#                     entry = st.session_state.stored_data[encrypted_text]
#                     if entry["passkey"] == hash_passkey(passkey):
#                         decrypted = decrypt_data(encrypted_text)
#                         st.session_state.failed_attempts = 0
#                         st.success("Decryption successful!")
#                         st.text_area("Decrypted Data:", value=decrypted, height=200)
#                     else:
#                         st.session_state.failed_attempts += 1
#                         st.error(f"❌ Invalid passkey! Attempts left: {3 - st.session_state.failed_attempts}")
#                 else:
#                     st.error("Invalid encrypted token!")
                
#                 if st.session_state.failed_attempts >= 3:
#                     st.session_state.auth = False
#                     st.experimental_rerun()

# # Login Page
# elif st.session_state.choice == "Login":
#     st.subheader("🔑 Administrator Authentication")
    
#     with st.form("login_form"):
#         password = st.text_input("Master Password:", type="password")
        
#         if st.form_submit_button("Authenticate"):
#             if password == "admin123":
#                 st.session_state.failed_attempts = 0
#                 st.session_state.auth = True
#                 st.session_state.choice = "Retrieve Data"
#                 st.experimental_rerun()
#             else:
#                 st.error("Incorrect master password!")

# # Authorization check
# if st.session_state.choice == "Retrieve Data" and not st.session_state.auth:
#     st.warning("⚠️ Please authenticate first!")
#     st.session_state.choice = "Login"
#     st.experimental_rerun()


import streamlit as st
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from hashlib import pbkdf2_hmac
import json
import os
import random

# --- Constants ---
DATA_FILE = "data_store.json"
MAX_FAILED_ATTEMPTS = 3
DEFAULT_SALT = "studifinity_salt"
BACKGROUND_IMAGE = "https://fintechweekly.s3.amazonaws.com/article/438/How_to_Prevent_Biometrics_Hacking_in_Banking_Apps-min.png"
            
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    f"""
    <style>
    /* Main app background with your image */
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{BACKGROUND_IMAGE}') no-repeat center center fixed;
        background-size: cover;
        color: white;
    }}
     /* Fixed Sidebar Styling */
    [data-testid="stSidebar"] {{
        background: rgba(0, 0, 0, 0.9) !important;
        padding: 2rem 1rem !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }}
    
    .stSidebar .stMarkdown,
    .stSidebar .stSelectbox,
    .stSidebar .stButton>button {{
        color: white !important;
    }}
    
    /* Sidebar - Black Glassmorphism with White Text */
       
    .stSidebar .stMarkdown h1,
    .stSidebar .stMarkdown h2,
    .stSidebar .stMarkdown h3,
    .stSidebar .stMarkdown h4,
    .stSidebar .stMarkdown h5,
    .stSidebar .stMarkdown h6 {{
        color: black !important;
    }}
    
    /* Force white text for all headings */
    h1, h2, h3, h4, h5, h6 {{
        color: white !important;
        background-image: none !important;
        -webkit-text-fill-color: white !important;
    }}
    
    /* Dashboard title specific styling */
    .dashboard-title {{
        color: white !important;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        background: none !important;
        -webkit-text-fill-color: white !important;
        text-shadow: none !important;
    }}
    
    /* Input fields - white background with black text */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {{
        background-color: white !important;
        color: black !important;
        border-radius: 8px !important;
    }}
    
    /* Placeholder text - dark gray */
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {{
        color: white !important;
        opacity: 0.8 !important;
    }}
    
    /* Buttons - dark  gradient */
    .stButton>button {{
        background: linear-gradient(to right, #2f4f4f, #365788) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(10, 92, 54, 0.4) !important;
    }}
    
    /* Cards - glassmorphism effect */
    .card {{
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    }}
    
    /* Success messages */
    .stAlert-success {{
        background: rgba(10, 92, 54, 0.2) !important;
        border-left: 4px solid #1db954 !important;
    }}
    [data-testid="stTextInput"] label p,
    [data-testid="stTextInput"] label div,
    [data-testid="stPasswordInput"] label p,
    [data-testid="stPasswordInput"] label div {{
        color: white !important;
        font-weight: 500 !important;
    }}

    .stTextInput input::placeholder,
    .stPasswordInput input::placeholder {{
        color: #cccccc !important;
        opacity: 0.8 !important;
    }}

    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .dashboard-title {{
            font-size: 2rem;
        }}
        
        .card {{
            padding: 15px !important;
        }}
            /* Login/Register Separation */
    .separator {{
        margin: 2rem 0;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        position: relative;
    }}
    
    .separator-text {{
        position: absolute;
        top: -11px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.9);
        padding: 0 1rem;
    }}

    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Key Management ---
@st.cache_resource
def load_cipher():
    key = Fernet.generate_key()
    return Fernet(key)

cipher = load_cipher()

# --- Data Handling ---
def load_data():
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Security Functions ---
def hash_passkey(passkey, salt=DEFAULT_SALT):
    key = pbkdf2_hmac('sha256', passkey.encode(), salt.encode(), 100000)
    return urlsafe_b64encode(key).decode()

def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text):
    return cipher.decrypt(encrypted_text.encode()).decode()

# --- Session Management ---
if "data_store" not in st.session_state:
    st.session_state.data_store = load_data()

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "authorized" not in st.session_state:
    st.session_state.authorized = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# --- Dashboard Page ---
def dashboard_page():
    """Dashboard/Home Page"""
    st.markdown('<h1 class="dashboard-title">📊 Secure Data Vault</h1>', unsafe_allow_html=True)
    
    # Stats Cards Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <h3>🔢</h3>
            <h2>{len(st.session_state.data_store[st.session_state.current_user]["entries"])}</h2>
            <p>Total Secrets</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>🛡️</h3>
            <h2>256-bit</h2>
            <p>Encryption</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>⚡</h3>
            <h2>100%</h2>
            <p>Secure</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Security Tips
    st.subheader("🔒 Security Tips")
    tips = [
        "Change passwords every 3 months",
        "Never share encryption keys",
        "Use complex passphrases",
        "Enable 2FA where possible",
        "Beware of phishing attempts"
    ]
    
    for tip in tips:
        st.markdown(f"""
        <div class="card" style="padding: 12px 15px; margin-bottom: 8px;">
            <p>✓ {tip}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("---")
    st.subheader("🚀 Quick Actions")
    action_col1, action_col2 = st.columns(2)
    with action_col1:
        if st.button("🔒 Encrypt New Data", use_container_width=True):
            st.session_state.page = "store"
            st.rerun()
    with action_col2:
        if st.button("🔓 Decrypt Data", use_container_width=True):
            st.session_state.page = "retrieve"
            st.rerun()

# --- Modified Login Page ---
def login_page():
    """Separated Login/Registration Page"""
    st.title("🔐 Secure Access")
    
    with st.container():
        # Registration Section
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("New User Registration")
        
        reg_user = st.text_input("Choose Username", key="reg_user")
        reg_pass = st.text_input("Create Password", type="password", key="reg_pass")
        reg_pass_confirm = st.text_input("Confirm Password", type="password", key="reg_pass_confirm")
        
        if st.button("Register Account"):
            if not reg_user or not reg_pass:
                st.error("Username and password required")
                return
            if reg_pass != reg_pass_confirm:
                st.error("Passwords do not match")
                return
                
            hashed_pass = hash_passkey(reg_pass)
            users = st.session_state.data_store
            
            if reg_user in users:
                st.error("Username already exists")
                return
                
            users[reg_user] = {"password": hashed_pass, "entries": {}}
            save_data(users)
            st.success("Registration successful! Please login")
            
        st.markdown('</div>', unsafe_allow_html=True)

        # Login Section
        st.markdown('<div class="separator"><span class="separator-text">OR</span></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Existing User Login")
        
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login to Account"):
            if not login_user or not login_pass:
                st.error("Username and password required")
                return
                
            users = st.session_state.data_store
            hashed_pass = hash_passkey(login_pass)
            
            if login_user not in users:
                st.error("User not found. Please register first")
                return
                
            if users[login_user]["password"] != hashed_pass:
                st.session_state.failed_attempts += 1
                st.error(f"Invalid credentials. {MAX_FAILED_ATTEMPTS - st.session_state.failed_attempts} attempts left")
                if st.session_state.failed_attempts >= MAX_FAILED_ATTEMPTS:
                    st.error("Account locked. Contact administrator")
                    st.stop()
                return
                
            st.session_state.current_user = login_user
            st.session_state.authorized = True
            st.rerun()

# --- Login/Register Page ---
# def login_page():
#     """Login/Registration Page"""
#     st.title("🔐 Secure Login")
    
#     with st.container():
#         st.markdown('<div class="card">', unsafe_allow_html=True)
        
#         username = st.text_input("Username", placeholder="Enter username")
#         password = st.text_input("Password", type="password", placeholder="Enter password")
        
#         if st.button("Login / Register"):
#             if not username or not password:
#                 st.error("Please enter both fields")
#                 return
                
#             hashed_pass = hash_passkey(password)
#             users = st.session_state.data_store
            
#             if username not in users:
#                 users[username] = {"password": hashed_pass, "entries": {}}
#                 st.success("Account created! Logged in.")
#             elif users[username]["password"] != hashed_pass:
#                 st.session_state.failed_attempts += 1
#                 st.error(f"Wrong password. {MAX_FAILED_ATTEMPTS - st.session_state.failed_attempts} attempts left")
#                 return
#             else:
#                 st.success("Login successful!")
                
#             st.session_state.current_user = username
#             st.session_state.authorized = True
#             save_data(users)
#             st.rerun()
            
#         st.markdown('</div>', unsafe_allow_html=True)

# --- Store Data Page ---
def store_data_page():
    """Data Encryption Page"""
    st.title("🔒 Store Data")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        data = st.text_area("Your Data", placeholder="Enter text to encrypt", height=150)
        passkey = st.text_input("Encryption Key", type="password", placeholder="Set a passkey")
        
        if st.button("Encrypt & Save"):
            if not data or not passkey:
                st.error("All fields required")
                return
                
            encrypted = encrypt_data(data)
            hashed_key = hash_passkey(passkey)
            
            st.session_state.data_store[st.session_state.current_user]["entries"][encrypted] = hashed_key
            save_data(st.session_state.data_store)
            
            st.success("Data encrypted and saved!")
            st.code(encrypted)
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- Retrieve Data Page ---
def retrieve_data_page():
    """Data Decryption Page"""
    st.title("🔓 Retrieve Data")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        encrypted = st.text_area("Encrypted Data", placeholder="Paste encrypted data", height=100)
        passkey = st.text_input("Decryption Key", type="password", placeholder="Enter passkey")
        
        if st.button("Decrypt"):
            if not encrypted or not passkey:
                st.error("All fields required")
                return
                
            entries = st.session_state.data_store[st.session_state.current_user]["entries"]
            hashed_input = hash_passkey(passkey)
            
            if encrypted in entries and entries[encrypted] == hashed_input:
                decrypted = decrypt_data(encrypted)
                st.success("Decrypted successfully!")
                st.text_area("Decrypted Data", decrypted, height=150)
            else:
                st.error("Invalid passkey or data")
                
        st.markdown('</div>', unsafe_allow_html=True)

# --- Main App ---
if st.session_state.authorized:
    st.sidebar.title(f"Welcome, {st.session_state.current_user}!")
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🏠 Dashboard"):
        st.session_state.page = "home"
    if st.sidebar.button("💾 Store Data"):
        st.session_state.page = "store"
    if st.sidebar.button("📂 Retrieve Data"):
        st.session_state.page = "retrieve"
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authorized = False
        st.session_state.current_user = ""
        st.rerun()

if not st.session_state.authorized:
    login_page()
else:
    if "page" not in st.session_state:
        st.session_state.page = "home"
        
    if st.session_state.page == "home":
        dashboard_page()
    elif st.session_state.page == "store":
        store_data_page()
    elif st.session_state.page == "retrieve":
        retrieve_data_page()