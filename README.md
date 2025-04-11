# 🔐 Secure Data Vault

A sleek, secure, and modern Streamlit-based application to **encrypt, store, and retrieve sensitive data** using **256-bit encryption** powered by the `cryptography` library. Designed with glassmorphism UI, this project ensures both security and aesthetics.

![Streamlit App Screenshot](https://fintechweekly.s3.amazonaws.com/article/438/How_to_Prevent_Biometrics_Hacking_in_Banking_Apps-min.png)

## ✨ Features

- 🔒 **256-bit AES Encryption** for strong data protection
- 📝 **Login/Register System** with hashed passwords
- 🧠 **Key-based Encryption/Decryption** using passkeys
- 📊 **Dashboard** with total entries and security tips
- 💾 **Data Storage** with persistent local file saving (`data_store.json`)
- 🎨 **Beautiful UI** with custom CSS and glassmorphism design
- 📱 **Responsive design** for all screen sizes

## 🛠 Tech Stack

- **Python 3.9+**
- **Streamlit**
- **Cryptography**
- **PBKDF2 Hashing**
- **Custom HTML/CSS for UI styling**

## 🚀 How to Run

1. **Clone this repository**

   git clone https://github.com/your-username/secure-data-vault.git
   cd secure-data-vault

## 🔐 Security Details
Passwords are never stored in plaintext.

Passkeys are hashed using PBKDF2 with SHA-256.

Data is encrypted using Fernet (AES-128 GCM).

Local JSON file (data_store.json) is used for secure, offline storage.

## 📁 Project Structure
pgsql
Copy
Edit
├── app.py                  # Main Streamlit application
├── data_store.json         # JSON storage for encrypted user data
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
📷 Screenshots   
Login Page  	Dashboard   	Encryption  
📢 Future Improvements    
🔐 Add two-factor authentication (2FA)   
☁️ Integrate with cloud database (like Firebase or Supabase)    

📱 Deploy to Streamlit Cloud

## 🙋‍♀️ Author
Syeda Farheen Zehra

