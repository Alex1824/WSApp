[app]

# (str) Title of your application
title = WhatsApp Link Generator

# (str) Package name
package.name = whatsapp_link

# (str) Package domain (needed for android/ios packaging)
package.domain = org.whatsapp.link

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ico

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (str) Application versioning
version = 0.1

# (list) Application requirements
# Requirements should match previously updated requirements.txt
requirements = python3,kivy,pyjnius,phonenumbers,pycountry,emoji,geocoder,pillow

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_CONTACTS,WRITE_CONTACTS

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (list) Icon files
icon.filename = %(source.dir)s/assets/icons/app_icon.png
icon.adaptive_foreground.filename = %(source.dir)s/assets/icons/app_icon_foreground.png
icon.adaptive_background.filename = %(source.dir)s/assets/icons/app_icon_background.png

# (list) Gradle dependencies to add
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.0.0

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D