from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
from fastapi.middleware.cors import CORSMiddleware
# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins; change to your React URL for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the saved model and encoder
# Ensure these files are copied into your /backend folder!
with open('hydration_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('encoder.pkl', 'rb') as f:
    encoders = pickle.load(f)

# Define the data shape coming from your React frontend
class HydrationData(BaseModel):
    age: int
    weight: float
    water_intake: float
    activity_level: int
    weather: int

@app.post("/predict")
async def predict_hydration(data: HydrationData):
    # Convert incoming JSON to a DataFrame matching your model's training columns
    input_df = pd.DataFrame(
        [[data.age, data.weight, data.water_intake, data.activity_level, data.weather]],
        columns=['Age', 'Weight (kg)', 'Daily Water Intake (liters)', 'Physical Activity Level', 'Weather']
    )
    
    # Make prediction
    prediction = model.predict(input_df)
    
    # Map the numerical result back to text for your UI
    result = "Hydrated" if prediction[0] == 0 else "Dehydrated"
    
    return {"prediction": result}

@app.get("/")
def read_root():
    return {"status": "HydroPredict API is Running"}