from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AliasBase(BaseModel):
    alias_code: str
    alias_type: str = 'old'
    is_primary: bool = False

class AliasOut(AliasBase):
    id: int
    family_id: int
    class Config: from_attributes = True

class FamilyBase(BaseModel):
    family_code: str
    family_name: str
    category: Optional[str] = None
    description: Optional[str] = None

class FamilyCreate(FamilyBase): pass

class FamilyOut(FamilyBase):
    id: int
    created_at: datetime
    aliases: List[AliasOut] = []
    class Config: from_attributes = True

class VersionBase(BaseModel):
    version_code: str
    specification: Optional[str] = None
    status: str = 'active'
    created_by: Optional[str] = None

class VersionCreate(VersionBase): pass

class VersionOut(VersionBase):
    id: int
    family_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config: from_attributes = True

class PartBase(BaseModel):
    part_category: str
    part_name: Optional[str] = None
    part_code: Optional[str] = None
    sort_order: int = 0

class PartCreate(PartBase): pass

class ParameterBase(BaseModel):
    param_name: str
    param_value: Optional[str] = None
    param_unit: Optional[str] = None
    param_type: str = 'text'
    sort_order: int = 0

class ParameterCreate(ParameterBase): pass

class ParameterOut(ParameterBase):
    id: int
    part_id: int
    class Config: from_attributes = True

class PartOut(PartBase):
    id: int
    version_id: int
    parameters: List[ParameterOut] = []
    class Config: from_attributes = True

class AttachmentOut(BaseModel):
    id: int
    version_id: int
    file_name: str
    file_path: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    file_category: Optional[str] = None
    uploaded_at: datetime
    class Config: from_attributes = True

class SearchSuggestion(BaseModel):
    term: str
    type: str = 'history'
    family_id: Optional[int] = None
