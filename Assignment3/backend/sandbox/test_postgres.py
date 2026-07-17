import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import declarative_base, sessionmaker

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import settings

# Database connection URL
DATABASE_URL = f"postgresql+psycopg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

# Create SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Student table schema
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    major = Column(String)

# 1. Test function: Create table students
def create_students_table():
    print("\n--- [Test Function] Creating Table 'students' ---")
    Base.metadata.create_all(bind=engine)
    print("Table 'students' created successfully.")

# 2. Test function: Insert data
def insert_student_data(session, name: str, age: int, major: str):
    print("\n--- [Test Function] Inserting Student Data ---")
    new_student = Student(name=name, age=age, major=major)
    session.add(new_student)
    session.commit()
    session.refresh(new_student)
    print(f"Inserted: ID={new_student.id}, Name={new_student.name}, Age={new_student.age}, Major={new_student.major}")
    return new_student

# 3. Test function: Update data
def update_student_data(session, name: str, new_major: str):
    print("\n--- [Test Function] Updating Student Data ---")
    student = session.scalar(select(Student).where(Student.name == name))
    if student:
        student.major = new_major
        session.commit()
        session.refresh(student)
        print(f"Updated: ID={student.id}, Name={student.name}, Age={student.age}, New Major={student.major}")
    return student

# 4. Test function: Delete data
def delete_student_data(session, name: str):
    print("\n--- [Test Function] Deleting Student Data ---")
    student = session.scalar(select(Student).where(Student.name == name))
    if student:
        session.delete(student)
        session.commit()
        print(f"Student '{name}' deleted successfully.")
    
    remaining = session.scalars(select(Student)).all()
    print(f"Remaining students count: {len(remaining)}")

# 5. Test function: Delete table (Drop)
def drop_students_table():
    print("\n--- [Test Function] Dropping Table 'students' ---")
    Base.metadata.drop_all(bind=engine)
    print("Table 'students' dropped successfully.")

def main():
    # Run the test functions sequentially
    create_students_table()
    
    session = SessionLocal()
    try:
        # Insert test data
        insert_student_data(session, "Alice Somjai", 20, "Computer Science")
        
        # Update test data
        update_student_data(session, "Alice Somjai", "Artificial Intelligence")
        
        # Delete test data
        delete_student_data(session, "Alice Somjai")
    finally:
        session.close()
        
    # Drop table
    drop_students_table()

if __name__ == "__main__":
    main()
