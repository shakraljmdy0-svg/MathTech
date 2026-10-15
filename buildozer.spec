[app]
title = MathTech
package.name = mathtech
package.domain = com.mathtech

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf,json,txt
source.include_patterns = assets/*

version = 1.0.0

requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/splash.png

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.ndk = 25.2.9519653
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.entrypoint = org.kivy.android.PythonActivity
android.accept_sdk_license = True
android.sdk_path = /home/runner/android-sdk
android.ndk_path = /home/runner/android-sdk/ndk/25.2.9519653

[buildozer]
log_level = 2
warn_on_root = 1