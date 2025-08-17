from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def Load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {"message" : "Patients Management System API"} 

@app.get("/about")
def about():
    return {"message" : "A fully functional Patients Management System API"}

@app.get("/view")
def view():
    data = Load_data() 
    return data

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
        raise HTTPException(status_code=400, detail=f"Invalid order")

    data = Load_data()
    sorted_order = True if order== 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x:x.get(sort_by,0), reverse=sorted_order)
    return sorted_data
