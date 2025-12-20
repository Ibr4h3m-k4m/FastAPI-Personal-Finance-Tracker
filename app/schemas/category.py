from pydantic import BaseModel, ConfigDict, field_validator , model_validator
from typing import Optional
from datetime import datetime, timedelta
from decimal import Decimal
from datetime import timezone
from pydantic import Field
import re

# For Creating a new transaction
class CategoryCreate(BaseModel):
    name: str = Field(min_length=2 ,max_length=50)
    color: Optional[str] = Field(None, max_length=7)
    icon: Optional[str] = Field(None, max_length=10)
    
    @field_validator('color')
    @classmethod
    def validate_color(cls, v):
        if v is None:
            return v
        # Validate hex color format (#RGB or #RRGGBB)
        if not re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', v):
            raise ValueError('Color must be in hex format (#RGB or #RRGGBB)')
        return v

    
    
# For Updating a category
class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(min_length=2 ,max_length=50)
    color: Optional[str] = Field(None, max_length=7)
    icon: Optional[str] = Field(None, max_length=10)
    
    @field_validator('color')
    @classmethod
    def validate_color(cls, v):
        if v is None:
            return v
        # Validate hex color format (#RGB or #RRGGBB)
        if not re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', v):
            raise ValueError('Color must be in hex format (#RGB or #RRGGBB)')
        return v
    
    @model_validator(mode='after')
    def check_at_least_one_field(self):
        # At least one must be provided
        if self.name is None and self.color is None and self.icon is None:
            raise ValueError('Must provide at least one field to update')
        return self

    
# For API responses
class CategoryResponse(BaseModel):
    id: int
    name: str
    user_id: int
    color: Optional[str]
    icon : Optional[str]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    