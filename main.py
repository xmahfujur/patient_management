import json
from fastapi import FastAPI , Path , HTTPException , Query
from pydantic import BaseModel

app = FastAPI()
datasets_path = 'datasets/bmi_dataset.json'

def data_loader(path):
    with open(path, 'r') as f:
        data = json.load(f)
        return data
    
@app.get('/')
def home():
    return {
        'message' : 'Patient Management System API'
    }
    
@app.get('/view')
def view():
    data = data_loader(datasets_path)
    return data
        
@app.get('/patient/{patient_id}')
def view_patient(patient_id : str = Path(..., description="Id of the patient", example='P001')):
    
    data = data_loader(datasets_path)
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient Not Found')
    
@app.get('/sort')
def sort_patient(sort_by : str = Query(..., description='Value Must me height, weight or bmi'), order : str = Query('asc', description="order value must me ascending or decending") ):
    valid_field_for_sort = ['height', 'weight', 'bmi']
    valid_field_for_order = ['asc', 'desc']
    
    if sort_by not in valid_field_for_sort:
        raise HTTPException(status_code=400, detail='Bad input')
    
    if order not in valid_field_for_order:
        raise HTTPException(status_code=400, detail='Bad input')
    
    data = data_loader(datasets_path)
    
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse= [True if order == 'asc' else False] )
        
    return sorted_data