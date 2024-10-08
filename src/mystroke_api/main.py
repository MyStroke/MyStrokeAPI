from typing import Annotated
import io

from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware

import mediapipe as mp

import numpy as np
import tensorflow as tf
from PIL import Image


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

loaded_model = tf.saved_model.load("MyStroke_model")
hands = mp.solutions.hands.Hands()


@app.get("/")
async def root():
    return "MyStroke API is running!!!"


@app.post("/api")
async def predict(image: Annotated[bytes, File()]):
    img = Image.open(io.BytesIO(image))
    img = img.convert("RGB")

    wpercent = 512 / img.size[0]
    hsize = int(img.size[1] * wpercent)
    img = img.resize((512, hsize), Image.Resampling.LANCZOS)

    img = np.array(img)

    hands_result = hands.process(img)
    hand_landmark = hands_result.multi_hand_landmarks

    if hand_landmark is None:
        return {"prediction": None}

    landmark_list = []
    for landmark in hand_landmark[0].landmark:
        landmark_list.append(np.array([landmark.x, landmark.y, landmark.z]))

    landmark_array = np.array(landmark_list)

    prediction, _ = loaded_model(landmark_array)
    prediction = np.array(prediction[0])
    return {
        "prediction": prediction.tolist(),
        "argmax": np.argmax(prediction).tolist(),
        "top_2": np.argsort(prediction)[-2:].tolist(),
    }