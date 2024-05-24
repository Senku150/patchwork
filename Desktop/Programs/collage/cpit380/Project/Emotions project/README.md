## Happiness Logger

This program is a facial recognition system designed to log a user's emotion upon successful login. It utilizes the DeepFace library for facial recognition and emotion detection.

### Features

* Login using a stored profile picture
* Capture a new image for comparison
* Verify captured image with stored profile
* Detect user's dominant emotion upon successful login
* Log date, time, and emotion to a text file

### Requirements

* Python 3.10+
* OpenCV
* Pillow
* DeepFace (**Note:** DeepFace may have usage limitations, refer to the library's documentation for details)
* customtkinter

### Installation

1. Install required libraries using pip:

```
pip install opencv-python pillow deepface customtkinter
```

### Usage

1. **Set User Directory:** Click the "Set the users Dir" button and select the folder containing your user profile pictures.
2. **Create a New Profile (Optional):** Click the "create a new profile" button to capture an image and assign a name to create a new profile.
3. **Choose a Profile:** Click the "Choose a Profile" button to select a profile picture for login.
4. **Capture Image:** Upon selecting a profile, the program will prompt you to capture a new image using your webcam. This image will be compared to the chosen profile picture.
5. **Login:** If the captured image matches the chosen profile, the program will log the date, time, and detected emotion to a text file named "report.txt".


### License

The licensing terms for the included libraries (OpenCV, Pillow, customtkinter) are generally permissive and allow for modification and distribution. DeepFace may have its own specific licensing terms, so refer to the library's documentation for details.
