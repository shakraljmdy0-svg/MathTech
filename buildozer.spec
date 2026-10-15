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
android.api = 31
android.build_tools_version = 35.0.0
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.entrypoint = org.kivy.android.PythonActivity

[buildozer]
log_level = 2
warn_on_root = 1