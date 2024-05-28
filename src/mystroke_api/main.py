from typing import List
from fastapi import FastAPI, HTTPException
import tensorflow as tf
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a FastAPI instance
app = FastAPI()

# Load the model
try:
    model = tf.saved_model.load("MyStroke_model")
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise HTTPException(status_code=500, detail="Model loading failed")

# Create API route
@app.post("/api")
async def api(data: dict):
    try:
        landmarks = data.get("data", [])
        if not landmarks:
            raise ValueError("No landmarks provided")

        # Convert landmarks to numpy array and reshape to (21, 3)
        landmarks_array = np.array(landmarks, dtype=np.float32).reshape(21, 3)

        # Run prediction
        prediction = model(landmarks_array)
        prediction = np.array(prediction[0])

        response_content = {
            "prediction": prediction.tolist(),
            "argmax": int(np.argmax(prediction)),
            "top_2": np.argsort(prediction)[-2:].tolist(),
        }

        return response_content
    except ValueError as ve:
        logger.error(f"Value error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
