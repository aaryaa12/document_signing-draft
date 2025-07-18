# PKI Document Signing System

A comprehensive, all-in-one PKI (Public Key Infrastructure) system for secure document signing and verification using RSA cryptography and digital certificates.

## 🚀 **Complete Unified System**

**`pki_system_main.py`** - Single application containing all PKI functionality:

- User Registration with RSA key generation
- User Authentication with private key/certificate
- Document Signing with digital signatures
- Document Verification with signature validation
- Professional scrollable GUI interface
- Real-time status updates and feedback

## 🎯 **Quick Start**

```bash
# Launch the complete PKI system
python pki_system_main.py
```

## 📋 **Usage Workflow**

### **Initial Interface (Before Login):**

1. **User Registration** - Create new user accounts
2. **User Login** - Authenticate with existing credentials
3. **Document Verification** - Verify signed documents (public access)

### **After Successful Login (User-Centric Interface):**

1. **Document Signing** - Sign documents with your digital signature
2. **Document Verification** - Verify signed documents
3. **Logout** - Return to main interface

### **Step-by-Step Process:**

#### **1. Register a User**

- Enter username in registration section
- Click "Register User"
- System generates RSA keys and certificate automatically

#### **2. Login to System**

- Browse and select your private key from `keys/` folder
- Browse and select your certificate from `certs/` folder
- Click "Login" to authenticate
- **UI switches to user-centric view**

#### **3. Sign Documents (After Login)**

- Browse and select any document
- Click "Sign Document"
- Signed files saved to `signed_docs/` folder

#### **4. Verify Documents (Available Before & After Login)**

- Select original document, signature file, and certificate
- Click "Verify Document"
- System validates signature authenticity

#### **5. Logout**

- Click "Logout" button
- **UI returns to initial interface**

## 🔧 **Technical Features**

- **RSA 2048-bit** key pair generation
- **X.509 certificates** with 1-year validity
- **SHA-256** hashing for document integrity
- **RSA-PSS** digital signature algorithm
- **Professional GUI** with scrollable interface
- **Real-time status** updates and feedback
- **File organization** in structured directories
- **Error handling** with clear user messages

## 📁 **File Structure**

```
signetrix/
├── pki_system_main.py          # Main PKI application
├── PKI_SYSTEM_README.md        # Detailed usage guide
├── sample_document.txt         # Test document
├── keys/                       # Generated private/public keys
├── certs/                      # Generated X.509 certificates
└── signed_docs/                # Signed documents + signatures
```

## 🔒 **Security Features**

- **Strong Cryptography**: RSA-2048 with SHA-256
- **Digital Signatures**: RSA-PSS padding for security
- **Certificate Validation**: X.509 standard compliance
- **Tamper Detection**: Signature verification detects modifications
- **File Integrity**: Cryptographic proof of authenticity

## 📦 **Requirements**

- **Python 3.7+**
- **cryptography** library
- **tkinter** (included with Python)

## 🛠️ **Installation**

1. **Clone or download** the repository
2. **Install dependencies**:
   ```bash
   pip install cryptography
   ```
3. **Run the system**:
   ```bash
   python pki_system_main.py
   ```

## 🎮 **Complete Workflow Example**

```bash
# 1. Launch the system
python pki_system_main.py

# INITIAL INTERFACE (Before Login):
# 2. Register a user:
#    - Enter "testuser" in username field
#    - Click "Register User"
#    - Wait for success message

# 3. Login:
#    - Browse and select keys/testuser_private.pem
#    - Browse and select certs/testuser_cert.pem
#    - Click "Login"
#    - UI switches to user-centric view

# USER INTERFACE (After Login):
# 4. Sign a document:
#    - Browse and select sample_document.txt
#    - Click "Sign Document"
#    - Check signed_docs/ folder

# 5. Verify the document:
#    - Select signed_docs/sample_document.txt
#    - Select signed_docs/sample_document.txt.sig
#    - Select signed_docs/sample_document.txt_cert.pem
#    - Click "Verify Document"

# 6. Logout:
#    - Click "Logout" button
#    - UI returns to initial interface
```

## ✨ **Key Advantages**

- **Single Application**: Everything in one unified interface
- **No Window Management**: No separate applications to juggle
- **Scrollable Interface**: Works on any screen size
- **Real-time Feedback**: Instant status updates
- **Professional Design**: Clean, modern interface
- **Complete Workflow**: Registration → Login → Sign → Verify

## 🔍 **How It Works**

### **Registration Process**

1. **RSA Key Generation**: Creates 2048-bit key pair
2. **X.509 Certificate**: Generates self-signed certificate
3. **File Organization**: Saves to `keys/` and `certs/` folders
4. **Success Feedback**: Real-time status updates

### **Authentication Process**

1. **File Validation**: Verifies private key and certificate
2. **Key Loading**: Loads cryptographic materials
3. **Login State**: Updates system status and enables features
4. **UI Updates**: Shows logged-in user and enables signing

### **Document Signing Process**

1. **Document Reading**: Loads file as binary data
2. **SHA-256 Hashing**: Creates document fingerprint
3. **RSA-PSS Signing**: Creates digital signature
4. **File Storage**: Saves to `signed_docs/` with signature and certificate

### **Verification Process**

1. **File Loading**: Loads document, signature, and certificate
2. **Hash Computation**: Recalculates document hash
3. **Signature Validation**: Verifies using public key
4. **Tamper Detection**: Identifies any modifications

## 📚 **Additional Resources**

- **`PKI_SYSTEM_README.md`** - Detailed usage guide
- **`sample_document.txt`** - Test document for signing
- **`test_pki_system_main.py`** - System validation tests

---

## 🎉 **Ready to Use!**

Your complete PKI document signing system is ready:

```bash
python pki_system_main.py
```

**Everything you need in one application!** 🚀

## 🧪 **Testing**

Test the system functionality:

```bash
python test_pki_system_main.py
```

## ⚠️ **Security Notes**

- **Educational Purpose**: This is a demonstration system for learning PKI concepts
- **Self-signed Certificates**: Not suitable for production environments
- **Unencrypted Keys**: Private keys stored without password protection
- **Local Use**: Designed for local testing and education

## 📋 **System Requirements**

- **Username**: Letters and numbers only
- **File Permissions**: Read/write access to project directory
- **Python Version**: 3.7 or higher
- **Dependencies**: cryptography library

## 🔐 **Certificate Information**

Generated certificates include:

- **Country**: US
- **Organization**: PKI System
- **Common Name**: Username
- **Validity**: 365 days
- **Key Size**: RSA 2048-bit
