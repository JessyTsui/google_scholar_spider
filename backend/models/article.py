from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base


class ArticleDB(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    authors = Column(Text)  # 原始作者字符串
    # main_author_id = Column(Integer, ForeignKey("authors.id"))  # 第一作者ID
    venue = Column(String(300))
    publisher = Column(String(200))
    year = Column(Integer)
    citations = Column(Integer, default=0)
    citations_per_year = Column(Float, default=0.0)
    description = Column(Text)
    url = Column(String(500))
    search_id = Column(Integer, ForeignKey("searches.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    search = relationship("SearchDB", back_populates="articles")
    # author_obj = relationship("AuthorDB", back_populates="papers")


class SearchDB(Base):
    __tablename__ = "searches"
    
    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(200), nullable=False)
    start_year = Column(Integer)
    end_year = Column(Integer)
    total_results = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    articles = relationship("ArticleDB", back_populates="search", cascade="all, delete-orphan")


class ArticleSchema(BaseModel):
    id: Optional[int] = None
    title: str
    authors: Optional[str] = None
    venue: Optional[str] = None
    publisher: Optional[str] = None
    year: Optional[int] = None
    citations: int = 0
    citations_per_year: float = 0.0
    description: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SearchSchema(BaseModel):
    id: Optional[int] = None
    keyword: str
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    total_results: int = 0
    created_at: Optional[datetime] = None
    articles: List[ArticleSchema] = []
    
    class Config:
        from_attributes = True


class SearchRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=200)
    num_results: int = Field(50, ge=10, le=1000)
    start_year: Optional[int] = Field(None, ge=1900, le=datetime.now().year)
    end_year: Optional[int] = Field(None, ge=1900, le=datetime.now().year)
    sort_by: str = Field("citations", pattern="^(citations|citations_per_year|year)$")


class SearchResponse(BaseModel):
    search_id: int
    keyword: str
    total_results: int
    articles: List[ArticleSchema]
    message: str = "Search completed successfully"