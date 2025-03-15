# VirtualPainter
This is a Python-based virtual drawing application that allows users to draw using hand gestures detected by webcam. It utilizes OpenCV and Mediapipe.

## Features
* Hand tracking using a custom hand tracking module
(HandTrackingModule.py)
* Virtual drawing using index finger
* Can choose different colors from a header menu
* Eraser to remove drawings

## Installation

### 1 Clone the Repository
git clone https://github.com/ThusSpokeSwan/VirtualPainter.git

### 2 Install Dependencies
Make sure you have python installed (ver 3.8 or up), then install the required libraries by running the following in cmd.
pip install opencv-python mediapipe numpy

### 3 Run the Virtual Painter
⚠️ Important: This project requires an IDE like PyCharm to run correctly. Running it directly from a terminal or command prompt may not work properly.

 * Running in PyCharm:
 1. Open PyCharm.
 2. Load the project folder.
 3. Ensure the required packages are installed in the project interpreter.
 4. Run VirtualPainter.py.

## Usage
* Raise index and middle finger to enter selection mode.
* Raise only the index finger to start drawing.
* Select the eraser to erase the drawing.

This project is inspired from **Murtaza's Workshop**