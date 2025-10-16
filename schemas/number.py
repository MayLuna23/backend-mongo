from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List

class NumberCreate(BaseModel):
    value: int = Field(..., description="Número a guardar")
    
    @field_validator('value')
    def value_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('El número debe ser mayor que 0')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "value": 42
            }
        }

class NumberResponse(BaseModel):
    id: str
    value: int
    created_at: str
    
class NumbersListResponse(BaseModel):
    username: str
    numbers: List[NumberResponse]
    
class NumberUpdate(BaseModel):
    value: int = Field(..., description="Nuevo valor del número")
    
    @field_validator('value')
    def value_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('El número debe ser mayor que 0')
        return v

class StatsResponse(BaseModel):
    username: str
    total_numbers: int
    average: float
    maximum: int
    minimum: int