# Creating fastapi backend (main.py)

from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
 
app = FastAPI(title="Realtime Calculator App")

#input model using pydantic
class Numbers(BaseModel):
    numbers: list[float]

@app.get("/")
def welcome():
    return {"message": "Welcome to Realtime Calculator App"}

@app.post("/sum")
def calculate_sum(data:Numbers):
    result = np.sum(data.numbers)
    return {"operation":"Sum","result":float(result)}

@app.post("/mean")
def calculate_mean(data: Numbers):
    result = np.mean(data.numbers)
    return {"operation":"mean", "result":float(result)}

@app.post("/median")
def calculate_median(data: Numbers):
    result = np.median(data.numbers)
    return {"operation":"median", "result":float(result)}

# Variance
@app.post("/variance")
def calculate_variance(data: Numbers):
    result = np.var(data.numbers)
    return {"operation":"Variance", "result":float(result)}

# Matrix multiply
@app.post("/multiply")
def calculate_multiply(data:dict):
    #example { a = [[1,2],[3,4]], b = [[5,6],[7,8]]}
    arr1 = np.array(data["a"])
    arr2 = np.array(data["b"])
    result = np.matmul(arr1,arr2)
    return {"Operation":"multiply","result":result.tolist()}