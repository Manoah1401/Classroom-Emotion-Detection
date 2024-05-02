# Emotion Detection and Recognition Project

## Overview

This project implements an emotion detection and recognition system using deep learning techniques. It includes scripts for detecting faces in videos, extracting emotions from detected faces, and recognizing individuals in images.

## Project Structure

The repository contains the following files:

- `automator.py`: Python script for automating the process of running the emotion detection and recognition pipeline.
- `emotion_detection.py`: Python script for detecting emotions in videos using a pre-trained deep learning model.
- `face_detection.py`: Python script for recognizing individuals in images using a pre-trained VGG16 model.
- `rafdb.h5`: Pre-trained model for emotion detection (RAF-DB).
- `face_recognition_vgg16_model_1.h5`: Pre-trained model for face recognition (VGG16).

## Usage

### Running the Emotion Detection and Recognition Pipeline

To run the complete pipeline for emotion detection and recognition, follow these steps:

1. Ensure you have all the required dependencies installed (listed in `requirements.txt`).
2. Run the `automator.py` script to automate the process. This script will run the emotion detection (`emotion_detection.py`) and face recognition (`face_detection.py`) scripts sequentially.

### Individual Scripts

- `emotion_detection.py`: This script can be used independently to detect emotions in videos. You need to provide the path to the video file as input.
- `face_detection.py`: This script can be used independently to recognize individuals in images. You need to provide the path to the image file as input.

## Requirements

Ensure you have the following dependencies installed:

- Python 3.x
- OpenCV
- TensorFlow
- NumPy
- etc. (List all dependencies here)

You can install the required dependencies using the following command:

```bash
pip install -r requirements.txt
