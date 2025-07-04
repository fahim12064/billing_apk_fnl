[app]

# Application Title
title = Khan's Optical Billing

# Package name (no space, no special character)
package.name = khansoptical

# Domain (can be anything, used for package signature)
package.domain = org.khanoptical.billing

# Source code file extensions to include
source.include_exts = py,kv,json,png,jpg

# Application version
version = 1.0

# Supported orientation
orientation = portrait

# Whether to make fullscreen or not
fullscreen = 0

# Path to your main.py
source.dir = .

# Your main .py file
main.py = main.py

# Icon of the app (optional - provide filename if you have one)
icon.filename = kiw.jpg

# Permissions (add more if needed)
android.permissions = INTERNET

# Android entrypoint (default: org.kivy.android.PythonActivity)
android.entrypoint = org.kivy.android.PythonActivity

# Minimum API level (21 = Android 5.0+)
android.minapi = 21

# Target API level
android.target = 33

# Android SDK version
android.sdk = 33

# Python version
python.version = 3

# Dependencies (IMPORTANT)
requirements = python3,kivy==2.3.0,kivymd==1.1.1

# Presplash (optional)
# presplash.filename = presplash.png

# Include .kv files automatically
include_patterns = *.kv

# Don't include tests or .pyc files
exclude_patterns = tests/*,*.pyc

# Bootstrap type
android.bootstrap = sdl2

# Hide title bar
android.window = softinput_avoid_resize

# Logcat filter (for debug)
log_level = 2

# Package format
android.packaging = zip

# (Optional) enable AndroidX (for some new libraries)
android.enable_androidx = 1

# (Optional) architecture (32bit or 64bit)
# android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1

# Copy the .apk to this folder after build
output.dir = bin

# Clean up after build
clean_build = False
