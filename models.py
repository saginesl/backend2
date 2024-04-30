from sqlalchemy import Column, Integer, String, ForeignKey, Identity
from sqlalchemy.orm import relationship, declarative_base
from typing import Optional
from pydantic import BaseModel,Field
Base = declarative_base()
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, Identity(start=1), primary_key=True)
    title = Column(String, index=True, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")

class New_Response(BaseModel):
    message: str

class BookCreate(BaseModel):
    title: str
    author_id: Optional[int] = Field(default=10, ge=10)

class AuthorCreate(BaseModel):
    name: str

class AuthorModel(BaseModel):
    name: str
    id: Optional[int] = Field(default=10, ge=10)