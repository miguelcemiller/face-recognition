import face_recognition
import os, sys
from os.path import join, dirname, realpath, splitext
import cv2
import numpy as np
import math

# face confidence
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

# faces folder path
PATH = join(dirname(realpath(__file__)), 'static/faces')

# arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []

# face recognition
def run_recognition():
    print('ENCODING FACES...')
    for image in os.listdir(PATH):
        face_image = face_recognition.load_image_file(f"{PATH}/{image}")
        face_encoding = face_recognition.face_encodings(face_image)[0]

        # remove image extension
        image_name, image_extension = splitext(image)

        known_face_encodings.append(face_encoding)
        known_face_names.append(image_name)
    print('REGISTERED FACES: ', known_face_names)

    print('RUNNING FACE RECOGNITION...')

    # variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_curr_frame = True  

    video_capture = cv2.VideoCapture(0)

    while True:
        # grab a single frame of video
        ret, frame = video_capture.read()

        # resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # convert BGR to RGB
        small_frame_rgb = small_frame[:, :, ::-1]
        
        # only process every other frame of video to save time
        if process_curr_frame:
            # find all faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(small_frame_rgb)
            face_encodings = face_recognition.face_encodings(small_frame_rgb, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # see if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                confidence = "?"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    confidence = face_confidence(face_distances[best_match_index])

                face_names.append(name)
                print(f'NAME: {name} - CONFIDENCE: {confidence}')
        
        process_curr_frame = not process_curr_frame

        # display results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # scale back up face locations since the frame was scaled to 1/4 
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)

            # draw label with name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 14, bottom - 14), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 1)
        
        cv2.namedWindow('Face Recognition',cv2.WINDOW_KEEPRATIO)
        cv2.imshow('Face Recognition', frame)

        # Hit 'q' or 'Q' on the keyboard to quit
        if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

