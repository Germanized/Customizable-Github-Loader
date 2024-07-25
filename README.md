# Germanized's Customizable GitHub Loader

## Installation

1. **Install the Required Packages:**

   Run the following command to install all necessary packages:

   `pip install -r requirements.txt`

2. **Download the Required Assets:**

   - **Fonts:** Ensure you have the `Mont.otf` font file in the same directory as the script.
   - **Music:** Place `background_music.mp3` in the same directory as the script.
   - **Icons:** Ensure you have `mute_icon.png` and `unmute_icon.png` for the mute button functionality.

## Usage

1. **Run the Application:**

   Execute the script using:

   `python loader.py`

2. **Navigating the Application:**

   - **Repositories Tab:** Click on the repository buttons to open them in a web browser.
   - **Readme Tab:** View the README content of the GitHub profile.
   - **Mute/Unmute Music:** Click the mute button to toggle background music.

## Customization

- **Splash Screen Animation:** Adjust the duration and animation parameters in the `SplashScreen` class.
- **Main Window:** Modify the appearance and functionality in the `LoaderApp` class. Change button styles, colors, and music files as needed.

## Troubleshooting

- **Failed to Fetch Repositories or README:**
  - Check your internet connection.
  - Ensure the URL paths are correct.

- **Music Issues:**
  - Verify that the `background_music.mp3` file is present and properly formatted.
  - Check for errors related to pygame initialization.

## License

This project is licensed under the [MIT License](LICENSE).
