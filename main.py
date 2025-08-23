from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field as F,computed_field
from typing import Annotated,Literal
import json

class Patient(BaseModel):
    id:Annotated[str,F(..., description="ID of patient", example="P001")]
    name: Annotated[str,F(..., description="Name of patient", example="John Doe")]
    city: Annotated[str,F(..., description="City of patient", example="New York")]
    age: Annotated[int,F(...,gt=0,lt=120, description="Age of patient", example=30)]
    gender: Annotated[Literal['Male','Female','Others'],F(..., description="Gneder of patient")]
    height: Annotated[float,F(...,gt=0, description="Height of patient in m", example=175.5)]
    weight: Annotated[float,F(...,gt=0, description="Weight of patient in kg", example=70.5)]

    @computed_field
    @property
    def bmi(self)-> float:
        return round(self.weight / (self.height/100)**2,2)
    
    @computed_field
    @property
    def verdict(self)-> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

app = FastAPI()

def Load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message" : "Patients Management System API"} 

@app.get("/about")
def about():
    return {"message" : "A fully functional Patients Management System API"}

@app.get("/view")
def view():
    return Load_data()

@app.get("/patient/{id}")
def view_patient(id:str = Path(..., description="The ID of the patient to view",example="P001")):
    data = Load_data()
    if id in data:
        return data[id]
    else:
        raise HTTPException(status_code=404, detail="Patient not found")
    
@app.get("/sort")
def sort_patients(sort_by:str = Query(..., description="Sort on the basis of height, weight, BMI"), order:str = Query('asc',description="Sort in ascending or descending order")):
    valid_field = ['height','weight','bmi']
    if sort_by not in valid_field:
        raise HTTPException(status_code=400, detail=f"Invalid sort from : {valid_field}")

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail="Invalid order")

    data = Load_data()
    sorted_order = True if order== 'desc' else False
    return sorted(
        data.values(), key=lambda x: x.get(sort_by, 0), reverse=sorted_order
    )

@app.post("/create")
def create_patient(patient: Patient):
    #load data
    data = Load_data()

    #check if patient id already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists")
    
    #add new partient
    data[patient.id] = patient.model_dump(exclude = [id])

    #save data into json
    save_data(data)

    return JSONResponse(content={"message": "Patient created successfully"}, status_code=201)