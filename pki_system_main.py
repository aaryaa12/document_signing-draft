#!/usr/bin/env python3
"""
PKI Document Signing System - Complete Integrated Application
All-in-one GUI system for PKI operations: registration, login, signing, verification
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import hashlib
import base64
import threading
import time
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime


# Professional Color Scheme
class Colors:
    # Primary Colors
    PRIMARY_DARK = '#1a1a2e'      # Deep navy blue
    PRIMARY_BLUE = '#16213e'      # Dark blue
    ACCENT_BLUE = '#0f3460'       # Medium blue
    LIGHT_BLUE = '#533483'        # Purple-blue

    # Background Colors
    BG_MAIN = '#f8f9fa'           # Light gray background
    BG_CARD = '#ffffff'           # White cards
    BG_HEADER = '#2c3e50'         # Dark header
    BG_SIDEBAR = '#34495e'        # Sidebar

    # Text Colors
    TEXT_PRIMARY = '#2c3e50'      # Dark text
    TEXT_SECONDARY = '#7f8c8d'    # Gray text
    TEXT_LIGHT = '#bdc3c7'        # Light gray text
    TEXT_WHITE = '#ffffff'        # White text

    # Status Colors
    SUCCESS = '#27ae60'           # Green
    WARNING = '#f39c12'           # Orange
    ERROR = '#e74c3c'             # Red
    INFO = '#3498db'              # Blue

    # Interactive Colors
    BUTTON_PRIMARY = '#3498db'    # Primary button
    BUTTON_SUCCESS = '#27ae60'    # Success button
    BUTTON_WARNING = '#f39c12'    # Warning button
    BUTTON_DANGER = '#e74c3c'     # Danger button
    BUTTON_HOVER = '#2980b9'      # Hover state

    # Border Colors
    BORDER_LIGHT = '#ecf0f1'      # Light border
    BORDER_MEDIUM = '#bdc3c7'     # Medium border
    BORDER_DARK = '#95a5a6'       # Dark border


# Professional Fonts
class Fonts:
    # Font families (use single font name for tkinter compatibility)
    PRIMARY = 'Segoe UI'
    SECONDARY = 'Consolas'
    FALLBACK = 'Arial'

    # Font sizes
    TITLE = 24
    HEADING = 18
    SUBHEADING = 14
    BODY = 11
    SMALL = 9
    CAPTION = 8


class PKISystem:
    def __init__(self, root):
        self.root = root
        self.current_user = None
        self.is_logged_in = False
        self.private_key_path = None
        self.certificate_path = None
        
        # Ensure directories exist
        self.ensure_directories()
        
        # Setup UI
        self.setup_ui()
        
        # Update status
        self.update_system_status()
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        directories = ['keys', 'certs', 'signed_docs']
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def setup_ui(self):
        """Setup the main interface with professional styling"""
        # Window configuration
        self.root.title("PKI Document Signing System - Professional Edition")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        self.root.configure(bg=Colors.BG_MAIN)

        # Configure window icon and styling
        try:
            self.root.state('zoomed')  # Maximize on Windows
        except:
            pass

        # Configure modern styling
        self.configure_styles()

        # Create main container with scrollable content
        self.create_main_container()

        # Create header
        self.create_header()

        # Create main content area
        self.create_main_content()

        # Create status bar
        self.create_status_bar()

        # Add smooth animations
        self.setup_animations()

    def configure_styles(self):
        """Configure modern TTK styles"""
        style = ttk.Style()

        # Configure modern button style
        style.configure('Modern.TButton',
                       font=(Fonts.PRIMARY, Fonts.BODY, 'bold'),
                       padding=(20, 10))

        # Configure modern frame style
        style.configure('Card.TFrame',
                       background=Colors.BG_CARD,
                       relief='flat',
                       borderwidth=1)

    def setup_animations(self):
        """Setup smooth animations and transitions"""
        # Add fade-in effect for the main window
        self.root.attributes('-alpha', 0.0)
        self.fade_in_window()

    def fade_in_window(self):
        """Smooth fade-in animation for the main window"""
        alpha = self.root.attributes('-alpha')
        if alpha < 1.0:
            alpha += 0.05
            self.root.attributes('-alpha', alpha)
            self.root.after(20, self.fade_in_window)
    
    def create_main_container(self):
        """Create modern scrollable main container"""
        # Main frame with modern background
        self.main_frame = tk.Frame(self.root, bg=Colors.BG_MAIN)
        self.main_frame.pack(fill='both', expand=True, padx=2, pady=2)

        # Create modern canvas with custom styling
        self.canvas = tk.Canvas(self.main_frame,
                               bg=Colors.BG_MAIN,
                               highlightthickness=0,
                               bd=0)

        # Custom styled scrollbar
        self.scrollbar = tk.Scrollbar(self.main_frame,
                                     orient="vertical",
                                     command=self.canvas.yview,
                                     bg=Colors.BG_SIDEBAR,
                                     troughcolor=Colors.BG_MAIN,
                                     activebackground=Colors.BUTTON_HOVER,
                                     width=12)

        self.scrollable_frame = tk.Frame(self.canvas, bg=Colors.BG_MAIN)

        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Bind canvas resize event
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Pack with modern layout
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Enhanced mouse wheel binding
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.root.bind("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_canvas_configure(self, event):
        """Handle canvas resize to update scroll region and width"""
        # Update the canvas scroll region when the frame changes size
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Update the canvas window width to match the canvas width
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def create_header(self):
        """Create modern professional header"""
        # Main header container with gradient effect
        header_container = tk.Frame(self.scrollable_frame, bg=Colors.BG_MAIN)
        header_container.pack(fill='x', padx=0, pady=(20, 10))

        # Header card with shadow effect
        header_frame = tk.Frame(header_container, bg=Colors.PRIMARY_DARK,
                               relief='flat', bd=0, height=100)
        header_frame.pack(fill='x', padx=20)
        header_frame.pack_propagate(False)

        # Add subtle shadow effect
        shadow_frame = tk.Frame(header_container, bg=Colors.BORDER_MEDIUM, height=2)
        shadow_frame.pack(fill='x')

        # Left side - Modern title section
        left_frame = tk.Frame(header_frame, bg=Colors.PRIMARY_DARK)
        left_frame.pack(side='left', fill='y', padx=30, pady=15)

        # Icon and title container
        title_container = tk.Frame(left_frame, bg=Colors.PRIMARY_DARK)
        title_container.pack(anchor='w')

        # Modern icon
        icon_label = tk.Label(title_container, text="🔐",
                             font=(Fonts.PRIMARY, 32),
                             fg=Colors.TEXT_WHITE, bg=Colors.PRIMARY_DARK)
        icon_label.pack(side='left', padx=(0, 15))

        # Title and subtitle
        text_container = tk.Frame(title_container, bg=Colors.PRIMARY_DARK)
        text_container.pack(side='left', fill='y')

        title_label = tk.Label(text_container, text="PKI Document Signing System",
                              font=(Fonts.PRIMARY, Fonts.TITLE, 'bold'),
                              fg=Colors.TEXT_WHITE, bg=Colors.PRIMARY_DARK)
        title_label.pack(anchor='w')

        subtitle_label = tk.Label(text_container, text="Professional Digital Authentication Platform",
                                 font=(Fonts.PRIMARY, Fonts.BODY),
                                 fg=Colors.TEXT_LIGHT, bg=Colors.PRIMARY_DARK)
        subtitle_label.pack(anchor='w')

        # Right side - Modern user status
        right_frame = tk.Frame(header_frame, bg=Colors.PRIMARY_DARK)
        right_frame.pack(side='right', fill='y', padx=30, pady=15)

        # Status container
        status_container = tk.Frame(right_frame, bg=Colors.PRIMARY_DARK)
        status_container.pack(anchor='e')

        self.user_status_label = tk.Label(status_container, text="● Not Logged In",
                                         font=(Fonts.PRIMARY, Fonts.SUBHEADING, 'bold'),
                                         fg=Colors.ERROR, bg=Colors.PRIMARY_DARK)
        self.user_status_label.pack(anchor='e')

        self.user_info_label = tk.Label(status_container, text="Please login to access all features",
                                       font=(Fonts.PRIMARY, Fonts.SMALL),
                                       fg=Colors.TEXT_LIGHT, bg=Colors.PRIMARY_DARK)
        self.user_info_label.pack(anchor='e')
    
    def create_main_content(self):
        """Create the main content area with dynamic sections based on login state"""
        self.content_frame = tk.Frame(self.scrollable_frame, bg='#f0f0f0')
        self.content_frame.pack(fill='both', expand=True, padx=0, pady=10)

        # Create initial UI (before login)
        self.create_initial_ui()

    def create_initial_ui(self):
        """Create the initial UI before login"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create sections for non-authenticated users
        self.create_registration_section(self.content_frame)
        self.create_login_section(self.content_frame)
        self.create_verification_section(self.content_frame)

    def create_user_ui(self):
        """Create the user-centric UI after successful login"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Welcome message
        welcome_frame = tk.Frame(self.content_frame, bg='#27ae60', relief='raised', bd=2)
        welcome_frame.pack(fill='x', pady=10, padx=5)

        welcome_label = tk.Label(welcome_frame,
                                text=f"Welcome, {self.current_user}! You are now logged in.",
                                font=('Arial', 14, 'bold'), fg='white', bg='#27ae60')
        welcome_label.pack(pady=15)

        # Create sections for authenticated users
        self.create_signing_section(self.content_frame)
        self.create_verification_section(self.content_frame)
        self.create_logout_section(self.content_frame)

    def create_logout_section(self, parent):
        """Create modern logout section"""
        logout_frame = self.create_section_frame(parent, "🚪 Session Management", Colors.ERROR)

        # Description with modern typography
        desc_label = tk.Label(logout_frame,
                             text="End your current session and return to the main authentication interface",
                             font=(Fonts.PRIMARY, Fonts.BODY),
                             fg=Colors.TEXT_SECONDARY, bg=Colors.BG_CARD,
                             wraplength=600, justify='center')
        desc_label.pack(pady=(0, 25))

        # Modern logout button
        button_container = tk.Frame(logout_frame, bg=Colors.BG_CARD)
        button_container.pack(pady=15)

        logout_button = self.create_modern_button(button_container, "🔓 Logout from System",
                                                 self.perform_logout, Colors.BUTTON_DANGER)
        logout_button.pack()
    
    def create_section_frame(self, parent, title, color):
        """Create a modern card-based section frame"""
        # Container for shadow effect - ensure it fills width
        container = tk.Frame(parent, bg=Colors.BG_MAIN)
        container.pack(fill='both', expand=True, pady=15, padx=20)

        # Shadow frame
        shadow_frame = tk.Frame(container, bg=Colors.BORDER_LIGHT, height=2)
        shadow_frame.pack(fill='x', pady=(2, 0))

        # Main card frame - ensure it fills width
        section_frame = tk.Frame(container, bg=Colors.BG_CARD, relief='flat', bd=0)
        section_frame.pack(fill='both', expand=True)

        # Header section with colored accent
        header_frame = tk.Frame(section_frame, bg=color, height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Title with modern typography
        title_label = tk.Label(header_frame, text=title,
                              font=(Fonts.PRIMARY, Fonts.HEADING, 'bold'),
                              fg=Colors.TEXT_WHITE, bg=color)
        title_label.pack(expand=True, pady=12)

        # Content area - ensure it fills width
        content_frame = tk.Frame(section_frame, bg=Colors.BG_CARD)
        content_frame.pack(fill='both', expand=True, padx=25, pady=20)

        return content_frame

    def create_modern_button(self, parent, text, command, bg_color, hover_color=None):
        """Create a modern button with hover effects"""
        if hover_color is None:
            hover_color = Colors.BUTTON_HOVER

        button = tk.Button(parent, text=text, command=command,
                          bg=bg_color, fg=Colors.TEXT_WHITE,
                          font=(Fonts.PRIMARY, Fonts.BODY, 'bold'),
                          relief='flat', bd=0, padx=25, pady=12,
                          cursor='hand2', activebackground=hover_color,
                          activeforeground=Colors.TEXT_WHITE)

        # Add hover effects
        def on_enter(e):
            button.config(bg=hover_color)

        def on_leave(e):
            button.config(bg=bg_color)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        return button

    def animate_button_click(self, button, original_color, click_color):
        """Animate button click with color change"""
        button.config(bg=click_color)
        self.root.after(100, lambda: button.config(bg=original_color))

    def create_registration_section(self, parent):
        """Create modern user registration section"""
        reg_frame = self.create_section_frame(parent, "👤 User Registration", Colors.INFO)

        # Description with modern typography
        desc_label = tk.Label(reg_frame,
                             text="Create a new user account with RSA-2048 key pair and X.509 certificate",
                             font=(Fonts.PRIMARY, Fonts.BODY),
                             fg=Colors.TEXT_SECONDARY, bg=Colors.BG_CARD,
                             wraplength=600, justify='center')
        desc_label.pack(pady=(0, 20))

        # Modern input container
        input_container = tk.Frame(reg_frame, bg=Colors.BG_CARD)
        input_container.pack(pady=10)

        # Username input with modern styling
        input_frame = tk.Frame(input_container, bg=Colors.BG_CARD)
        input_frame.pack()

        username_label = tk.Label(input_frame, text="Username:",
                                 font=(Fonts.PRIMARY, Fonts.BODY, 'bold'),
                                 fg=Colors.TEXT_PRIMARY, bg=Colors.BG_CARD)
        username_label.pack(side='left', padx=(0, 10))

        # Modern entry field
        self.username_entry = tk.Entry(input_frame,
                                      font=(Fonts.PRIMARY, Fonts.BODY),
                                      width=25, relief='flat', bd=1,
                                      bg=Colors.BG_MAIN, fg=Colors.TEXT_PRIMARY,
                                      insertbackground=Colors.TEXT_PRIMARY)
        self.username_entry.pack(side='left', padx=10, ipady=8)

        # Modern register button
        self.register_button = self.create_modern_button(
            input_frame, "Register User", self.register_user, Colors.BUTTON_PRIMARY)
        self.register_button.pack(side='left', padx=15)

        # Status label with modern styling
        self.reg_status_label = tk.Label(reg_frame, text="",
                                        font=(Fonts.PRIMARY, Fonts.BODY),
                                        bg=Colors.BG_CARD, wraplength=600)
        self.reg_status_label.pack(pady=(15, 0))

    def create_login_section(self, parent):
        """Create modern login section"""
        login_frame = self.create_section_frame(parent, "🔑 User Authentication", Colors.WARNING)

        # Description with modern typography
        desc_label = tk.Label(login_frame,
                             text="Authenticate using your private key and certificate for secure access",
                             font=(Fonts.PRIMARY, Fonts.BODY),
                             fg=Colors.TEXT_SECONDARY, bg=Colors.BG_CARD,
                             wraplength=600, justify='center')
        desc_label.pack(pady=(0, 25))

        # Modern file selection container
        file_container = tk.Frame(login_frame, bg=Colors.BG_CARD)
        file_container.pack(fill='x', pady=10)

        # Private key selection with modern styling
        key_section = tk.Frame(file_container, bg=Colors.BG_CARD)
        key_section.pack(fill='x', pady=8)

        key_label = tk.Label(key_section, text="Private Key File:",
                            font=(Fonts.PRIMARY, Fonts.BODY, 'bold'),
                            fg=Colors.TEXT_PRIMARY, bg=Colors.BG_CARD)
        key_label.pack(anchor='w')

        key_row = tk.Frame(key_section, bg=Colors.BG_CARD)
        key_row.pack(fill='x', pady=(5, 0))

        self.key_path_label = tk.Label(key_row, text="📄 No file selected",
                                      font=(Fonts.PRIMARY, Fonts.SMALL),
                                      fg=Colors.ERROR, bg=Colors.BG_MAIN,
                                      relief='flat', bd=1, padx=10, pady=8,
                                      anchor='w')
        self.key_path_label.pack(side='left', fill='x', expand=True, padx=(0, 10))

        key_browse_btn = self.create_modern_button(key_row, "Browse Keys",
                                                  self.select_private_key, Colors.BUTTON_PRIMARY)
        key_browse_btn.pack(side='right')

        # Certificate selection with modern styling
        cert_section = tk.Frame(file_container, bg=Colors.BG_CARD)
        cert_section.pack(fill='x', pady=8)

        cert_label = tk.Label(cert_section, text="Certificate File:",
                             font=(Fonts.PRIMARY, Fonts.BODY, 'bold'),
                             fg=Colors.TEXT_PRIMARY, bg=Colors.BG_CARD)
        cert_label.pack(anchor='w')

        cert_row = tk.Frame(cert_section, bg=Colors.BG_CARD)
        cert_row.pack(fill='x', pady=(5, 0))

        self.cert_path_label = tk.Label(cert_row, text="📄 No file selected",
                                       font=(Fonts.PRIMARY, Fonts.SMALL),
                                       fg=Colors.ERROR, bg=Colors.BG_MAIN,
                                       relief='flat', bd=1, padx=10, pady=8,
                                       anchor='w')
        self.cert_path_label.pack(side='left', fill='x', expand=True, padx=(0, 10))

        cert_browse_btn = self.create_modern_button(cert_row, "Browse Certificates",
                                                   self.select_certificate, Colors.WARNING)
        cert_browse_btn.pack(side='right')

        # Modern login button
        button_container = tk.Frame(login_frame, bg=Colors.BG_CARD)
        button_container.pack(pady=25)

        self.login_button = self.create_modern_button(button_container, "🔓 Login to System",
                                                     self.perform_login, Colors.BUTTON_SUCCESS)
        self.login_button.pack()

        # Status label with modern styling
        self.login_status_label = tk.Label(login_frame, text="",
                                          font=(Fonts.PRIMARY, Fonts.BODY),
                                          bg=Colors.BG_CARD, wraplength=600)
        self.login_status_label.pack(pady=(15, 0))

    def create_signing_section(self, parent):
        """Create modern document signing section (only shown after login)"""
        sign_frame = self.create_section_frame(parent, "✍️ Document Signing", Colors.SUCCESS)

        # Description with modern typography
        desc_label = tk.Label(sign_frame,
                             text="Sign documents with your digital signature using RSA-PSS cryptography",
                             font=(Fonts.PRIMARY, Fonts.BODY),
                             fg=Colors.TEXT_SECONDARY, bg=Colors.BG_CARD,
                             wraplength=600, justify='center')
        desc_label.pack(pady=(0, 25))

        # Modern document selection container
        doc_container = tk.Frame(sign_frame, bg=Colors.BG_CARD)
        doc_container.pack(fill='x', pady=10)

        # Document selection with modern styling
        doc_section = tk.Frame(doc_container, bg=Colors.BG_CARD)
        doc_section.pack(fill='x', pady=8)

        doc_label = tk.Label(doc_section, text="Document to Sign:",
                            font=(Fonts.PRIMARY, Fonts.BODY, 'bold'),
                            fg=Colors.TEXT_PRIMARY, bg=Colors.BG_CARD)
        doc_label.pack(anchor='w')

        doc_row = tk.Frame(doc_section, bg=Colors.BG_CARD)
        doc_row.pack(fill='x', pady=(5, 0))

        self.doc_path_label = tk.Label(doc_row, text="📄 No document selected",
                                      font=(Fonts.PRIMARY, Fonts.SMALL),
                                      fg=Colors.ERROR, bg=Colors.BG_MAIN,
                                      relief='flat', bd=1, padx=10, pady=8,
                                      anchor='w')
        self.doc_path_label.pack(side='left', fill='x', expand=True, padx=(0, 10))

        doc_browse_btn = self.create_modern_button(doc_row, "Browse Documents",
                                                  self.select_document, Colors.SUCCESS)
        doc_browse_btn.pack(side='right')

        # Modern sign button
        button_container = tk.Frame(sign_frame, bg=Colors.BG_CARD)
        button_container.pack(pady=25)

        self.sign_button = self.create_modern_button(button_container, "🖊️ Sign Document",
                                                    self.sign_document, Colors.BUTTON_SUCCESS)
        self.sign_button.pack()

        # Status label with modern styling
        self.sign_status_label = tk.Label(sign_frame, text="Ready to sign documents",
                                         font=(Fonts.PRIMARY, Fonts.BODY),
                                         fg=Colors.SUCCESS, bg=Colors.BG_CARD, wraplength=600)
        self.sign_status_label.pack(pady=(15, 0))

    def create_verification_section(self, parent):
        """Create modern document verification section"""
        verify_frame = self.create_section_frame(parent, "✅ Document Verification", Colors.LIGHT_BLUE)

        # Description with modern typography
        desc_label = tk.Label(verify_frame,
                             text="Verify the authenticity and integrity of digitally signed documents",
                             font=(Fonts.PRIMARY, Fonts.BODY),
                             fg=Colors.TEXT_SECONDARY, bg=Colors.BG_CARD,
                             wraplength=600, justify='center')
        desc_label.pack(pady=(0, 25))

        # Modern file selection container
        file_container = tk.Frame(verify_frame, bg=Colors.BG_CARD)
        file_container.pack(fill='x', pady=10)

        # Original document selection with modern styling
        orig_section = tk.Frame(file_container, bg=Colors.BG_CARD)
        orig_section.pack(fill='x', pady=8)

        orig_label = tk.Label(orig_section, text="Original Document:",
                             font=(Fonts.PRIMARY, Fonts.BODY, 'bold'),
                             fg=Colors.TEXT_PRIMARY, bg=Colors.BG_CARD)
        orig_label.pack(anchor='w')

        orig_row = tk.Frame(orig_section, bg=Colors.BG_CARD)
        orig_row.pack(fill='x', pady=(5, 0))

        self.orig_doc_label = tk.Label(orig_row, text="📄 No document selected",
                                      font=(Fonts.PRIMARY, Fonts.SMALL),
                                      fg=Colors.ERROR, bg=Colors.BG_MAIN,
                                      relief='flat', bd=1, padx=10, pady=8,
                                      anchor='w')
        self.orig_doc_label.pack(side='left', fill='x', expand=True, padx=(0, 10))

        orig_browse_btn = self.create_modern_button(orig_row, "Browse Documents",
                                                   self.select_original_document, Colors.LIGHT_BLUE)
        orig_browse_btn.pack(side='right')

        # Signature file selection with modern styling
        sig_section = tk.Frame(file_container, bg=Colors.BG_CARD)
        sig_section.pack(fill='x', pady=8)

        sig_label = tk.Label(sig_section, text="Signature File (.sig):",
                            font=(Fonts.PRIMARY, Fonts.BODY, 'bold'),
                            fg=Colors.TEXT_PRIMARY, bg=Colors.BG_CARD)
        sig_label.pack(anchor='w')

        sig_row = tk.Frame(sig_section, bg=Colors.BG_CARD)
        sig_row.pack(fill='x', pady=(5, 0))

        self.sig_file_label = tk.Label(sig_row, text="🔏 No signature selected",
                                      font=(Fonts.PRIMARY, Fonts.SMALL),
                                      fg=Colors.ERROR, bg=Colors.BG_MAIN,
                                      relief='flat', bd=1, padx=10, pady=8,
                                      anchor='w')
        self.sig_file_label.pack(side='left', fill='x', expand=True, padx=(0, 10))

        sig_browse_btn = self.create_modern_button(sig_row, "Browse Signatures",
                                                  self.select_signature_file, Colors.LIGHT_BLUE)
        sig_browse_btn.pack(side='right')

        # Certificate file selection with modern styling
        cert_section = tk.Frame(file_container, bg=Colors.BG_CARD)
        cert_section.pack(fill='x', pady=8)

        cert_label = tk.Label(cert_section, text="Certificate File (.pem):",
                             font=(Fonts.PRIMARY, Fonts.BODY, 'bold'),
                             fg=Colors.TEXT_PRIMARY, bg=Colors.BG_CARD)
        cert_label.pack(anchor='w')

        cert_row = tk.Frame(cert_section, bg=Colors.BG_CARD)
        cert_row.pack(fill='x', pady=(5, 0))

        self.cert_verify_label = tk.Label(cert_row, text="📜 No certificate selected",
                                         font=(Fonts.PRIMARY, Fonts.SMALL),
                                         fg=Colors.ERROR, bg=Colors.BG_MAIN,
                                         relief='flat', bd=1, padx=10, pady=8,
                                         anchor='w')
        self.cert_verify_label.pack(side='left', fill='x', expand=True, padx=(0, 10))

        cert_browse_btn = self.create_modern_button(cert_row, "Browse Certificates",
                                                   self.select_certificate_for_verification, Colors.LIGHT_BLUE)
        cert_browse_btn.pack(side='right')

        # Modern verify button
        button_container = tk.Frame(verify_frame, bg=Colors.BG_CARD)
        button_container.pack(pady=25)

        self.verify_button = self.create_modern_button(button_container, "🔍 Verify Document",
                                                      self.verify_document, Colors.LIGHT_BLUE)
        self.verify_button.pack()

        # Status label with modern styling
        self.verify_status_label = tk.Label(verify_frame, text="",
                                           font=(Fonts.PRIMARY, Fonts.BODY),
                                           bg=Colors.BG_CARD, wraplength=600)
        self.verify_status_label.pack(pady=(15, 0))

    def create_status_bar(self):
        """Create modern status bar"""
        # Status container
        status_container = tk.Frame(self.scrollable_frame, bg=Colors.BG_MAIN)
        status_container.pack(fill='x', side='bottom', padx=0, pady=(10, 20))

        # Modern status bar with gradient effect
        status_frame = tk.Frame(status_container, bg=Colors.BG_SIDEBAR, height=40)
        status_frame.pack(fill='x', padx=20)
        status_frame.pack_propagate(False)

        # Left side - Status indicator
        left_status = tk.Frame(status_frame, bg=Colors.BG_SIDEBAR)
        left_status.pack(side='left', fill='y', padx=20, pady=8)

        self.status_label = tk.Label(left_status, text="🟢 System Ready",
                                    font=(Fonts.PRIMARY, Fonts.BODY),
                                    fg=Colors.TEXT_WHITE, bg=Colors.BG_SIDEBAR)
        self.status_label.pack(anchor='w')

        # Right side - System information
        right_status = tk.Frame(status_frame, bg=Colors.BG_SIDEBAR)
        right_status.pack(side='right', fill='y', padx=20, pady=8)

        self.system_info_label = tk.Label(right_status, text="",
                                         font=(Fonts.PRIMARY, Fonts.SMALL),
                                         fg=Colors.TEXT_LIGHT, bg=Colors.BG_SIDEBAR)
        self.system_info_label.pack(anchor='e')

    # ==================== CORE FUNCTIONALITY METHODS ====================

    def register_user(self):
        """Register a new user with RSA key pair and certificate"""
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username!")
            return

        if not username.isalnum():
            messagebox.showerror("Error", "Username must contain only letters and numbers!")
            return

        # Check if user already exists
        if os.path.exists(f"keys/{username}_private.pem"):
            messagebox.showerror("Error", f"User '{username}' already exists!")
            return

        try:
            self.reg_status_label.config(text="Generating RSA key pair...", fg='#f39c12')
            self.root.update()

            # Generate RSA key pair
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            public_key = private_key.public_key()

            # Create certificate
            self.reg_status_label.config(text="Creating certificate...", fg='#f39c12')
            self.root.update()

            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "State"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "City"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "PKI System"),
                x509.NameAttribute(NameOID.COMMON_NAME, username),
            ])

            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                public_key
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.datetime.utcnow()
            ).not_valid_after(
                datetime.datetime.utcnow() + datetime.timedelta(days=365)
            ).sign(private_key, hashes.SHA256())

            # Save private key
            with open(f"keys/{username}_private.pem", "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))

            # Save public key
            with open(f"keys/{username}_public.pem", "wb") as f:
                f.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))

            # Save certificate
            with open(f"certs/{username}_cert.pem", "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))

            self.reg_status_label.config(text=f"✓ User '{username}' registered successfully!", fg='#27ae60')
            self.username_entry.delete(0, tk.END)
            self.update_system_status()

            messagebox.showinfo("Success",
                              f"User '{username}' registered successfully!\n\n"
                              f"Files created:\n"
                              f"• keys/{username}_private.pem\n"
                              f"• keys/{username}_public.pem\n"
                              f"• certs/{username}_cert.pem")

        except Exception as e:
            self.reg_status_label.config(text=f"Registration failed: {str(e)}", fg='#e74c3c')
            messagebox.showerror("Error", f"Registration failed: {str(e)}")

    def select_private_key(self):
        """Select private key file with modern feedback"""
        file_path = filedialog.askopenfilename(
            title="Select Private Key File",
            filetypes=[("PEM files", "*.pem"), ("All files", "*.*")],
            initialdir="keys" if os.path.exists("keys") else "."
        )
        if file_path:
            self.private_key_path = file_path
            filename = os.path.basename(file_path)
            # Modern success feedback
            self.key_path_label.config(text=f"🔑 {filename}",
                                      fg=Colors.SUCCESS, bg=Colors.BG_MAIN)
            self.animate_selection_feedback(self.key_path_label)

    def select_certificate(self):
        """Select certificate file with modern feedback"""
        file_path = filedialog.askopenfilename(
            title="Select Certificate File",
            filetypes=[("PEM files", "*.pem"), ("All files", "*.*")],
            initialdir="certs" if os.path.exists("certs") else "."
        )
        if file_path:
            self.certificate_path = file_path
            filename = os.path.basename(file_path)
            # Modern success feedback
            self.cert_path_label.config(text=f"📜 {filename}",
                                       fg=Colors.SUCCESS, bg=Colors.BG_MAIN)
            self.animate_selection_feedback(self.cert_path_label)

    def animate_selection_feedback(self, label):
        """Animate file selection feedback"""
        original_bg = label.cget('bg')
        # Brief highlight animation
        label.config(bg=Colors.SUCCESS)
        self.root.after(150, lambda: label.config(bg=original_bg))

    def perform_login(self):
        """Perform user login"""
        if not self.private_key_path or not self.certificate_path:
            messagebox.showerror("Error", "Please select both private key and certificate files!")
            return

        try:
            # Extract username from private key filename
            key_filename = os.path.basename(self.private_key_path)
            if '_private.pem' in key_filename:
                username = key_filename.replace('_private.pem', '')
            else:
                messagebox.showerror("Error", "Invalid private key file format!")
                return

            # Verify files exist and are valid
            if not os.path.exists(self.private_key_path):
                messagebox.showerror("Error", "Private key file not found!")
                return

            if not os.path.exists(self.certificate_path):
                messagebox.showerror("Error", "Certificate file not found!")
                return

            # Test loading the private key
            with open(self.private_key_path, "rb") as key_file:
                private_key = load_pem_private_key(key_file.read(), password=None)

            # Update login state
            self.current_user = username
            self.is_logged_in = True

            # Update header UI
            self.user_status_label.config(text=f"● Logged in as: {username}", fg='#27ae60')
            self.user_info_label.config(text="All features enabled")

            # Switch to user-centric UI
            self.create_user_ui()

            self.update_system_status()

            messagebox.showinfo("Login Successful", f"Welcome {username}!\nYou now have access to document signing features.")

        except Exception as e:
            messagebox.showerror("Login Error", f"Login failed: {str(e)}")
            self.login_status_label.config(text=f"Login failed: {str(e)}", fg='#e74c3c')

    def perform_logout(self):
        """Perform user logout and return to initial UI"""
        if messagebox.askyesno("Logout", f"Are you sure you want to logout?\nCurrent user: {self.current_user}"):
            # Reset state
            self.current_user = None
            self.is_logged_in = False
            self.private_key_path = None
            self.certificate_path = None

            # Update header UI
            self.user_status_label.config(text="● Not Logged In", fg='#e74c3c')
            self.user_info_label.config(text="Please login to access all features")

            # Switch back to initial UI
            self.create_initial_ui()

            self.update_system_status()
            messagebox.showinfo("Logged Out", "Successfully logged out. You have returned to the main interface.")

    def select_document(self):
        """Select document to sign with modern feedback"""
        file_path = filedialog.askopenfilename(
            title="Select Document to Sign",
            filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            self.document_path = file_path
            filename = os.path.basename(file_path)
            # Modern success feedback
            self.doc_path_label.config(text=f"📄 {filename}",
                                      fg=Colors.SUCCESS, bg=Colors.BG_MAIN)
            self.animate_selection_feedback(self.doc_path_label)

    def sign_document(self):
        """Sign the selected document"""
        if not hasattr(self, 'document_path') or not self.document_path:
            messagebox.showerror("Error", "Please select a document to sign!")
            return

        try:
            self.sign_status_label.config(text="Signing document...", fg='#f39c12')
            self.root.update()

            # Read the document
            with open(self.document_path, 'rb') as f:
                document_data = f.read()

            # Load private key
            with open(self.private_key_path, "rb") as key_file:
                private_key = load_pem_private_key(key_file.read(), password=None)

            # Create signature
            signature = private_key.sign(
                document_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            # Save signed document and signature
            doc_name = os.path.basename(self.document_path)
            signed_doc_path = f"signed_docs/{doc_name}"
            signature_path = f"signed_docs/{doc_name}.sig"
            cert_copy_path = f"signed_docs/{doc_name}_cert.pem"

            # Copy original document to signed_docs
            with open(self.document_path, 'rb') as src, open(signed_doc_path, 'wb') as dst:
                dst.write(src.read())

            # Save signature
            with open(signature_path, 'wb') as f:
                f.write(signature)

            # Copy certificate for verification
            with open(self.certificate_path, 'rb') as src, open(cert_copy_path, 'wb') as dst:
                dst.write(src.read())

            self.sign_status_label.config(text=f"✓ Document signed successfully!", fg='#27ae60')
            self.update_system_status()

            messagebox.showinfo("Success",
                              f"Document signed successfully!\n\n"
                              f"Files created:\n"
                              f"• {signed_doc_path}\n"
                              f"• {signature_path}\n"
                              f"• {cert_copy_path}\n\n"
                              f"Use these files for verification.")

        except Exception as e:
            self.sign_status_label.config(text=f"Signing failed: {str(e)}", fg='#e74c3c')
            messagebox.showerror("Error", f"Document signing failed: {str(e)}")

    def select_original_document(self):
        """Select original document for verification with modern feedback"""
        file_path = filedialog.askopenfilename(
            title="Select Original Document for Verification",
            filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf"), ("All files", "*.*")],
            initialdir="signed_docs" if os.path.exists("signed_docs") else "."
        )
        if file_path:
            self.orig_document_path = file_path
            filename = os.path.basename(file_path)
            # Modern success feedback
            self.orig_doc_label.config(text=f"📄 {filename}",
                                      fg=Colors.SUCCESS, bg=Colors.BG_MAIN)
            self.animate_selection_feedback(self.orig_doc_label)

    def select_signature_file(self):
        """Select signature file for verification with modern feedback"""
        file_path = filedialog.askopenfilename(
            title="Select Digital Signature File",
            filetypes=[("Signature files", "*.sig"), ("All files", "*.*")],
            initialdir="signed_docs" if os.path.exists("signed_docs") else "."
        )
        if file_path:
            self.signature_file_path = file_path
            filename = os.path.basename(file_path)
            # Modern success feedback
            self.sig_file_label.config(text=f"🔏 {filename}",
                                      fg=Colors.SUCCESS, bg=Colors.BG_MAIN)
            self.animate_selection_feedback(self.sig_file_label)

    def select_certificate_for_verification(self):
        """Select certificate file for verification with modern feedback"""
        file_path = filedialog.askopenfilename(
            title="Select Certificate File for Verification",
            filetypes=[("PEM files", "*.pem"), ("Certificate files", "*.crt"), ("All files", "*.*")],
            initialdir="signed_docs" if os.path.exists("signed_docs") else "."
        )
        if file_path:
            self.cert_verify_path = file_path
            filename = os.path.basename(file_path)
            # Modern success feedback
            self.cert_verify_label.config(text=f"📜 {filename}",
                                         fg=Colors.SUCCESS, bg=Colors.BG_MAIN)
            self.animate_selection_feedback(self.cert_verify_label)

    def verify_document(self):
        """Verify document signature"""
        if not hasattr(self, 'orig_document_path') or not self.orig_document_path:
            messagebox.showerror("Error", "Please select the original document!")
            return

        if not hasattr(self, 'signature_file_path') or not self.signature_file_path:
            messagebox.showerror("Error", "Please select the signature file!")
            return

        if not hasattr(self, 'cert_verify_path') or not self.cert_verify_path:
            messagebox.showerror("Error", "Please select the certificate file!")
            return

        try:
            self.verify_status_label.config(text="Verifying document...", fg='#f39c12')
            self.root.update()

            # Read original document
            with open(self.orig_document_path, 'rb') as f:
                document_data = f.read()

            # Read signature
            with open(self.signature_file_path, 'rb') as f:
                signature = f.read()

            # Read certificate and extract public key
            with open(self.cert_verify_path, 'rb') as f:
                cert_data = f.read()

            cert = x509.load_pem_x509_certificate(cert_data)
            public_key = cert.public_key()

            # Verify signature
            try:
                public_key.verify(
                    signature,
                    document_data,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )

                # Get certificate info
                subject = cert.subject
                common_name = subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

                self.verify_status_label.config(text="✓ Document signature is VALID!", fg='#27ae60')
                messagebox.showinfo("Verification Successful",
                                  f"✓ Document signature is VALID!\n\n"
                                  f"Signed by: {common_name}\n"
                                  f"Document integrity: VERIFIED\n"
                                  f"Signature authenticity: CONFIRMED")

            except Exception:
                self.verify_status_label.config(text="✗ Document signature is INVALID!", fg='#e74c3c')
                messagebox.showerror("Verification Failed",
                                   "✗ Document signature is INVALID!\n\n"
                                   "The document may have been:\n"
                                   "• Modified after signing\n"
                                   "• Signed with a different certificate\n"
                                   "• Corrupted during transfer")

        except Exception as e:
            self.verify_status_label.config(text=f"Verification error: {str(e)}", fg='#e74c3c')
            messagebox.showerror("Error", f"Verification failed: {str(e)}")

    def update_system_status(self):
        """Update system status information"""
        info_parts = []

        # Count registered users
        if os.path.exists('keys'):
            key_count = len([f for f in os.listdir('keys') if f.endswith('_private.pem')])
            info_parts.append(f"Users: {key_count}")
        else:
            info_parts.append("Users: 0")

        # Count signed documents
        if os.path.exists('signed_docs'):
            doc_count = len([f for f in os.listdir('signed_docs')
                           if not f.endswith('.sig') and not f.endswith('_cert.pem')])
            info_parts.append(f"Signed Docs: {doc_count}")
        else:
            info_parts.append("Signed Docs: 0")

        # Add current user
        if self.is_logged_in:
            info_parts.append(f"Current: {self.current_user}")

        self.system_info_label.config(text=" | ".join(info_parts))


def main():
    """Main function to run the PKI system"""
    root = tk.Tk()
    app = PKISystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
