# Data Modeling — Summary

## Core Approach

Design data models with Pydantic schemas — type-safe, validated, and relationship-aware.

## Key Decisions

1. **Base models**: Pydantic BaseModel with Field() for all metadata
2. **Validation**: Field constraints (min/max/regex) + @validator for business rules
3. **Relationships**: Foreign keys as typed IDs, nested models for embedded data
4. **Serialization**: orm_mode for SQLAlchemy integration, aliases for API contracts
5. **Constrained types**: constr, conint, confloat for reusable type constraints

## Core Pattern

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class Entity(BaseModel):
    id: Optional[int] = Field(None, description="Auto-generated")
    name: str = Field(..., min_length=1, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @validator('name')
    def validate_name(cls, v):
        return v.strip()

    class Config:
        orm_mode = True
```

## When to Go Deeper

- Ask for **patterns** → relationships, cross-field validation, constrained types
- Ask for **full reference** → complete data-model-guide.md and pydantic-patterns.md
