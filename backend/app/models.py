from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class ModelFamily(Base):
    __tablename__ = "model_families"
    id = Column(Integer, primary_key=True, index=True)
    family_code = Column(String(50), nullable=False, unique=True)
    family_name = Column(String(100))
    category = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    aliases = relationship("ModelAlias", back_populates="family", cascade="all, delete-orphan")
    versions = relationship("ModelVersion", back_populates="family", cascade="all, delete-orphan")

class ModelAlias(Base):
    __tablename__ = "model_aliases"
    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("model_families.id", ondelete="CASCADE"))
    alias_code = Column(String(50), nullable=False)
    alias_type = Column(String(20), default='old')
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    family = relationship("ModelFamily", back_populates="aliases")

class ModelVersion(Base):
    __tablename__ = "model_versions"
    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("model_families.id", ondelete="CASCADE"))
    version_code = Column(String(50), nullable=False)
    specification = Column(Text)
    status = Column(String(20), default='active')
    created_by = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    family = relationship("ModelFamily", back_populates="versions")
    parts = relationship("VersionPart", back_populates="version", cascade="all, delete-orphan")
    attachments = relationship("VersionAttachment", back_populates="version", cascade="all, delete-orphan")

class VersionPart(Base):
    __tablename__ = "version_parts"
    id = Column(Integer, primary_key=True, index=True)
    version_id = Column(Integer, ForeignKey("model_versions.id", ondelete="CASCADE"))
    part_category = Column(String(100), nullable=False)
    part_name = Column(String(200))
    part_code = Column(String(50))
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    version = relationship("ModelVersion", back_populates="parts")
    parameters = relationship("PartParameter", back_populates="part", cascade="all, delete-orphan")

class PartParameter(Base):
    __tablename__ = "part_parameters"
    id = Column(Integer, primary_key=True, index=True)
    part_id = Column(Integer, ForeignKey("version_parts.id", ondelete="CASCADE"))
    param_name = Column(String(100), nullable=False)
    param_value = Column(Text)
    param_unit = Column(String(50))
    param_type = Column(String(20), default='text')
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    part = relationship("VersionPart", back_populates="parameters")

class VersionAttachment(Base):
    __tablename__ = "version_attachments"
    id = Column(Integer, primary_key=True, index=True)
    version_id = Column(Integer, ForeignKey("model_versions.id", ondelete="CASCADE"))
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(100))
    file_size = Column(Integer)
    file_category = Column(String(50))
    description = Column(Text)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    uploaded_by = Column(String(100))
    
    version = relationship("ModelVersion", back_populates="attachments")

class SearchHistory(Base):
    __tablename__ = "search_history"
    id = Column(Integer, primary_key=True, index=True)
    search_term = Column(String(200), nullable=False)
    search_count = Column(Integer, default=1)
    last_searched = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
