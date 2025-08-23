from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field as F,computed_field
from typing import Annotated,Literal,Optional
import json

class Patient(BaseModel):
    id:Annotated[str,F(..., description="ID of patient", example="P001")]
    name: Annotated[str,F(..., description="Name of patient", example="John Doe")]
    city: Annotated[str,F(..., description="City of patient", example="New York")]
    age: Annotated[int,F(...,gt=0,lt=120, description="Age of patient", example=30)]
    gender: Annotated[Literal['Male','Female','Others'],F(..., description="Gender of patient")]
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
        
class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],F(default=None)]
    city:Annotated[Optional[str],F(default=None)]
    age:Annotated[Optional[int],F(default=None,gt=0)]
    gender:Annotated[Optional[Literal['Male','Female','Others']],F(default=None)]
    height:Annotated[Optional[float],F(default=None,gt=0)]
    weight:Annotated[Optional[float],F(default=None,gt=0)]

app = FastAPI()

def Load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)

#Home
@app.get("/")
def hello():
    return {"message" : "Patients Management System API"} 

#About
@app.get("/about")
def about():
    return {"message" : "A fully functional Patients Management System API"}

#View Data
@app.get("/view")
def view():
    return Load_data()

#View particular patient
@app.get("/patient/{id}")
def view_patient(id:str = Path(..., description="The ID of the patient to view",example="P001")):
    data = Load_data()
    if id in data:
        return data[id]
    else:
        raise HTTPException(status_code=404, detail="Patient not found")
    
#Sort the patient data
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

#Add a patient
@app.post("/create")
def create_patient(patient: Patient):
    #load data
    data = Load_data()

    #check if patient id already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists")
    
    #add new partient
    data[patient.id] = patient.model_dump(exclude = ['id'])

    #save data into json
    save_data(data)

    return JSONResponse(content={"message": "Patient created successfully"}, status_code=200)

#Edit patient detail
@app.put("/edit/{patient_id}")
def update_patient(patient_id:str, patient_update:PatientUpdate):
    data = Load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Invalid Patient ID")
    
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id 
    patient_pydantic_obj = Patient(**existing_patient_info)
    existing_patient_info = patient_pydantic_obj.model_dump(exclude=['id'])
    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(content={"message": "Patient updated successfully"}, status_code=200)

#Delete a patient
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data = Load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Invalid Patient ID")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code = 200, content={'message' : 'User deleted Successfully'})