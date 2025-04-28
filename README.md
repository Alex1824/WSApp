# WhatsApp Link Generator

## Project Overview
This project is a modern and efficient mobile application built with Kivy. It allows users to generate WhatsApp links quickly and easily.

## Features
- Generate WhatsApp links with phone number validation.
- Support for multiple languages.
- Integration with device contacts.
- Dark mode and light mode themes.
- AdMob integration for monetization.

## Setup Instructions
1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
Run the following command to start the application:
```bash
python main.py
```

## Building for Android
Use `buildozer` to package the application for Android. Ensure you have `buildozer` installed and configured.

## AdMob Integration

To enable AdMob in your Android build, follow these steps:

1. Add the following permissions to your `buildozer.spec` file:
   ```
   android.permissions = INTERNET, ACCESS_NETWORK_STATE
   ```

2. Include the AdMob dependency in your `buildozer.spec` file:
   ```
   android.gradle_dependencies = 'com.google.android.gms:play-services-ads:20.6.0'
   ```

3. Replace `YOUR_AD_UNIT_ID` in `ad_manager.py` with your actual AdMob unit ID.

4. Build the application using Buildozer:
   ```bash
   buildozer -v android debug
   ```

## Additional Setup Instructions

### Testing the Application
To test the application, follow these steps:
1. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application locally:
   ```bash
   python main.py
   ```

### Packaging for Android
To package the application for Android, use Buildozer:
1. Install Buildozer:
   ```bash
   pip install buildozer
   ```
2. Initialize Buildozer in the project directory:
   ```bash
   buildozer init
   ```
3. Edit the `buildozer.spec` file to configure your app (e.g., app name, permissions, etc.).
4. Build the APK:
   ```bash
   buildozer -v android debug
   ```

### Deployment
- For Android: Distribute the generated APK file to users.
- For other platforms: Follow platform-specific packaging instructions.

### Troubleshooting
- If you encounter issues with dependencies, ensure your Python environment is correctly set up.
- For Buildozer-related errors, consult the [Buildozer documentation](https://buildozer.readthedocs.io/en/latest/).

## Contribution
Feel free to fork the repository and submit pull requests for new features or bug fixes.