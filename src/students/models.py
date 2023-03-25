from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database import Base
from users.models import UserModel, UserType


class StudentModel(UserModel):
    __tablename__ = "students"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    course = Column(String, nullable=False)
    group = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    avatar = Column(String, nullable=True)

    training_direction = Column(String, nullable=False)
    training_profile = Column(String, nullable=False)
    faculty = Column(String, nullable=False)
    cathedra = Column(String, nullable=False)
    training_form = Column(String, nullable=False)

    about = Column(String, nullable=True)
    resume = Column(String, nullable=True)

    record_book_number = Column(String, nullable=False)
    document_number = Column(String, nullable=False)
    snils = Column(String, nullable=False)

    contacts = relationship("StudentContactModel", back_populates="student")
    relatives = relationship("StudentRelativeModel", back_populates="student")

    __mapper_args__ = {
        "polymorphic_identity": UserType.student
    }


class StudentContactModel(Base):
    __tablename__ = "student_contacts"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    text = Column(String, nullable=False)

    student = relationship(StudentModel, back_populates="contacts")


class StudentRelativeModel(Base):
    __tablename__ = "student_relatives"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    text = Column(String, nullable=False)

    student = relationship(StudentModel, back_populates="relatives")
