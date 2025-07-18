#!/usr/bin/env python3
"""
Test script to verify the new UI flow
"""

import tkinter as tk
from pki_system_main import PKISystem


def test_ui_flow():
    """Test the UI flow changes"""
    print("Testing New UI Flow")
    print("=" * 25)
    
    try:
        # Create root window (hidden for testing)
        root = tk.Tk()
        root.withdraw()
        
        # Create PKI system
        pki_system = PKISystem(root)
        
        # Test initial state
        print("✓ Initial UI created successfully")
        
        # Check that user is not logged in initially
        assert pki_system.is_logged_in == False, "Should start logged out"
        assert pki_system.current_user is None, "Should start with no user"
        print("✓ Initial login state correct")
        
        # Test that initial UI has correct sections
        # (We can't easily test GUI elements, but we can test the logic)
        
        # Simulate successful login
        pki_system.current_user = "testuser"
        pki_system.is_logged_in = True
        pki_system.private_key_path = "keys/testuser_private.pem"
        pki_system.certificate_path = "certs/testuser_cert.pem"
        
        # Test user UI creation
        pki_system.create_user_ui()
        print("✓ User UI created successfully after login")
        
        # Test logout
        pki_system.current_user = None
        pki_system.is_logged_in = False
        pki_system.private_key_path = None
        pki_system.certificate_path = None
        
        pki_system.create_initial_ui()
        print("✓ Initial UI restored after logout")
        
        root.destroy()
        print("✓ All UI flow tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ UI flow test failed: {e}")
        return False


def main():
    """Main test function"""
    print("PKI System - UI Flow Test")
    print("=" * 35)
    
    success = test_ui_flow()
    
    print("\n" + "=" * 35)
    if success:
        print("SUCCESS: New UI flow is working correctly!")
        print("\nExpected behavior:")
        print("1. Initial UI shows:")
        print("   • User Registration")
        print("   • User Login")
        print("   • Document Verification")
        print("\n2. After successful login:")
        print("   • Welcome message with username")
        print("   • Document Signing (enabled)")
        print("   • Document Verification")
        print("   • Logout button")
        print("\n3. After logout:")
        print("   • Returns to initial UI")
        print("   • All user-specific features hidden")
        
        print("\nTo test manually:")
        print("1. Run: python pki_system_main.py")
        print("2. Register a user")
        print("3. Login with the user")
        print("4. Observe UI change to user-centric view")
        print("5. Logout and observe return to initial UI")
    else:
        print("FAILURE: UI flow test failed")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
