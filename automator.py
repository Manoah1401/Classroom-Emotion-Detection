import subprocess
import psutil
import time
import webbrowser
import os
import shutil

def run_yolo():
    print("Running RafDB...")
    subprocess.run(['python3', 'video.py'])  
    print("RafDB completed.")

def run_facenet():
    print("Running FaceNet...")
    subprocess.run(['python3', 'face_detection.py'])  
    print("FaceNet completed.")

def open_emotion_detection_html():
    print("Opening emotion_detection.html in the default web browser...")

    html_file_path = 'emotion_detection1.html'

    webbrowser.open('http://127.0.0.1:5500/' + html_file_path)

def delete_folder_contents(folder_path):
    print(f"Deleting contents of folder: {folder_path}")
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): 
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

if __name__ == "__main__":
    run_yolo()


    while "working.py" in (p.name() for p in psutil.process_iter()):
        time.sleep(1)

    run_facenet()


    open_emotion_detection_html()

    user_input = input("Press Enter to continue without deleting the folder contents, or any other key to delete: ")
    
    if user_input:
        folder_path = 'parent'
        delete_folder_contents(folder_path)
    else:
        print("Folder contents will not be deleted.")
