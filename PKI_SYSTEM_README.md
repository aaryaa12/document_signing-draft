# PKI Document Signing System - Complete Application

## 🚀 **New Unified System**

We've created a **complete, all-in-one PKI system** that handles everything from a single interface:

- ✅ **User Registration** with RSA key generation
- ✅ **User Authentication** with private key/certificate
- ✅ **Document Signing** with digital signatures
- ✅ **Document Verification** with signature validation
- ✅ **Scrollable Interface** for all screen sizes
- ✅ **Professional UI** with real-time status updates

## 📁 **Main System File**

**`pki_system_main.py`** - The complete PKI system (31KB, 745 lines)

This single file contains everything you need for PKI operations.

## 🎯 **How to Use**

### **1. Launch the System**
```bash
python pki_system_main.py
```

### **2. Register a New User**
1. Enter a username (letters/numbers only)
2. Click **"Register User"**
3. Wait for success message
4. Files created automatically:
   - `keys/username_private.pem` (Private key)
   - `keys/username_public.pem` (Public key)
   - `certs/username_cert.pem` (Certificate)

### **3. Login to System**
1. Click **"Browse"** next to Private Key
2. Select your private key from `keys/` folder
3. Click **"Browse"** next to Certificate
4. Select your certificate from `certs/` folder
5. Click **"Login"**
6. Status updates to show logged-in user

### **4. Sign a Document**
1. After login, click **"Browse"** next to Document to Sign
2. Select any file (text, PDF, etc.)
3. Click **"Sign Document"**
4. Files created in `signed_docs/`:
   - Original document copy
   - `.sig` signature file
   - `_cert.pem` certificate copy

### **5. Verify a Document**
1. Click **"Browse"** for Original Document
2. Select document from `signed_docs/`
3. Click **"Browse"** for Signature File
4. Select `.sig` file from `signed_docs/`
5. Click **"Browse"** for Certificate File
6. Select `_cert.pem` file from `signed_docs/`
7. Click **"Verify Document"**
8. See verification result

## 🎨 **Interface Features**

### **Scrollable Design**
- Use mouse wheel to scroll through all sections
- All content accessible on any screen size
- Professional card-based layout

### **Real-time Status**
- Header shows current login status
- Each section has status indicators
- Bottom status bar shows system statistics

### **Visual Feedback**
- ✓ Green checkmarks for successful operations
- ✗ Red indicators for errors
- Color-coded status messages
- File selection confirmations

## 🔧 **Technical Details**

### **Cryptography**
- **RSA 2048-bit** key pairs
- **SHA-256** hashing
- **PSS padding** for signatures
- **X.509 certificates** (1-year validity)

### **File Structure**
```
signetrix/
├── pki_system_main.py      # Main application
├── keys/                   # Private/public keys
├── certs/                  # X.509 certificates
├── signed_docs/            # Signed documents + signatures
└── sample_document.txt     # Test document
```

### **Dependencies**
- `tkinter` - GUI framework
- `cryptography` - PKI operations
- `os`, `sys` - File system
- `datetime` - Certificate validity

## ✨ **Key Advantages**

### **1. Single Application**
- No separate windows or processes
- Everything in one unified interface
- No complex window management

### **2. Complete Workflow**
- Register → Login → Sign → Verify
- All steps in logical order
- Clear visual progression

### **3. User-Friendly**
- Intuitive file selection
- Clear error messages
- Step-by-step guidance

### **4. Professional Design**
- Modern UI with proper spacing
- Color-coded sections
- Responsive layout

### **5. Robust Error Handling**
- Validates all inputs
- Clear error messages
- Graceful failure recovery

## 🧪 **Testing**

### **Quick Test Workflow**
1. Run: `python pki_system_main.py`
2. Register user: "testuser"
3. Login with generated keys
4. Sign `sample_document.txt`
5. Verify the signed document

### **Expected Results**
- Registration creates 3 files
- Login enables signing features
- Signing creates 3 files in `signed_docs/`
- Verification shows "VALID" signature

## 🔒 **Security Features**

- **Strong Cryptography**: RSA-2048 + SHA-256
- **Signature Verification**: Detects tampering
- **Certificate Validation**: Ensures authenticity
- **File Integrity**: Protects against modification

## 📋 **Status Information**

The system tracks:
- **Registered Users**: Count of user accounts
- **Signed Documents**: Count of signed files
- **Current User**: Active logged-in user
- **Operation Status**: Real-time feedback

---

## 🎉 **Success!**

You now have a **complete, professional PKI system** in a single file that handles all document signing operations with a beautiful, scrollable interface!

**Main Command**: `python pki_system_main.py`
