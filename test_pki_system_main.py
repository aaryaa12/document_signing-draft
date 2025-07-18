#!/usr/bin/env python3
"""
Test script for the new comprehensive PKI system
"""

import os
import sys


def test_file_structure():
    """Test that the main system file exists and is properly structured"""
    print("Testing PKI System Main File Structure")
    print("=" * 45)
    
    # Check main file exists
    if os.path.exists('pki_system_main.py'):
        print("✓ pki_system_main.py exists")
        
        # Check file size (should be substantial)
        file_size = os.path.getsize('pki_system_main.py')
        if file_size > 10000:  # Should be > 10KB
            print(f"✓ File size: {file_size} bytes (substantial)")
        else:
            print(f"⚠ File size: {file_size} bytes (might be incomplete)")
        
        # Check for key classes and methods
        with open('pki_system_main.py', 'r') as f:
            content = f.read()
            
        required_elements = [
            'class PKISystem',
            'def register_user',
            'def perform_login',
            'def sign_document',
            'def verify_document',
            'from cryptography',
            'def create_registration_section',
            'def create_login_section',
            'def create_signing_section',
            'def create_verification_section'
        ]
        
        for element in required_elements:
            if element in content:
                print(f"✓ Contains: {element}")
            else:
                print(f"✗ Missing: {element}")
    else:
        print("✗ pki_system_main.py not found")


def test_directory_structure():
    """Test that required directories exist or can be created"""
    print("\nTesting Directory Structure")
    print("=" * 30)
    
    required_dirs = ['keys', 'certs', 'signed_docs']
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✓ {directory}/ directory exists")
            
            # Count files in directory
            files = os.listdir(directory)
            print(f"  - Contains {len(files)} files")
            
            # Show some example files
            if files:
                for file in files[:3]:  # Show first 3 files
                    print(f"    • {file}")
                if len(files) > 3:
                    print(f"    ... and {len(files) - 3} more")
        else:
            print(f"⚠ {directory}/ directory missing (will be created by system)")


def test_dependencies():
    """Test that required dependencies are available"""
    print("\nTesting Dependencies")
    print("=" * 20)
    
    dependencies = [
        ('tkinter', 'GUI framework'),
        ('cryptography', 'Cryptographic operations'),
        ('os', 'File system operations'),
        ('datetime', 'Date/time handling')
    ]
    
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"✓ {module} - {description}")
        except ImportError:
            print(f"✗ {module} - {description} (MISSING)")


def test_sample_document():
    """Check if sample document exists for testing"""
    print("\nTesting Sample Document")
    print("=" * 25)
    
    if os.path.exists('sample_document.txt'):
        print("✓ sample_document.txt exists")
        with open('sample_document.txt', 'r') as f:
            content = f.read()
        print(f"  - Size: {len(content)} characters")
        print(f"  - Preview: {content[:50]}...")
    else:
        print("⚠ sample_document.txt missing")
        print("  Creating sample document for testing...")
        
        sample_content = """This is a sample document for PKI testing.

This document can be used to test the digital signing functionality
of the PKI Document Signing System.

Content:
- This is line 1 of the document
- This is line 2 of the document  
- This is line 3 of the document

The system will create a digital signature for this document
that can be verified later to ensure authenticity and integrity.

Test completed successfully!
"""
        
        try:
            with open('sample_document.txt', 'w') as f:
                f.write(sample_content)
            print("✓ Created sample_document.txt")
        except Exception as e:
            print(f"✗ Failed to create sample document: {e}")


def main():
    """Run all tests"""
    print("PKI System Main - Comprehensive Test")
    print("=" * 50)
    
    test_file_structure()
    test_directory_structure()
    test_dependencies()
    test_sample_document()
    
    print("\n" + "=" * 50)
    print("USAGE INSTRUCTIONS:")
    print("=" * 50)
    print("1. Run the system: python pki_system_main.py")
    print("2. Register a user:")
    print("   • Enter username in registration section")
    print("   • Click 'Register User'")
    print("   • Wait for success message")
    print("3. Login:")
    print("   • Click 'Browse' next to Private Key")
    print("   • Select your private key from keys/ folder")
    print("   • Click 'Browse' next to Certificate")
    print("   • Select your certificate from certs/ folder")
    print("   • Click 'Login'")
    print("4. Sign a document:")
    print("   • Click 'Browse' next to Document to Sign")
    print("   • Select sample_document.txt or any file")
    print("   • Click 'Sign Document'")
    print("   • Check signed_docs/ folder for results")
    print("5. Verify a document:")
    print("   • Select original document from signed_docs/")
    print("   • Select signature file (.sig)")
    print("   • Select certificate file (_cert.pem)")
    print("   • Click 'Verify Document'")
    
    print("\nFEATURES:")
    print("• All-in-one interface (no separate windows)")
    print("• Scrollable content for small screens")
    print("• Real-time status updates")
    print("• Comprehensive error handling")
    print("• Professional UI design")
    print("• Complete PKI workflow in one application")


if __name__ == "__main__":
    main()
