import enum

from pydantic import BaseModel, Field

from shared.schemas import Semester


class SubjectGradeStatus(enum.Enum):
    """Статус оценки по предмету (вовремя, после окончания периода, не сдана, перезачтена, не обязательна)"""
    in_time = 'in_time'
    late = 'late'
    failed = 'failed'
    reapplied = 'reapplied'
    not_required = 'not_required'


class SubjectEvaluationType(enum.Enum):
    """Вид контроля (экзамен, зачет, курсовая работа)"""
    exam = 'exam'
    credit = 'credit'
    course_work = 'course_work'


class SubjectGrade(BaseModel):
    """Оценка за контрольный промежуток"""
    id: int
    grade: int = Field(title='Оценка')
    status: SubjectGradeStatus = Field(title='Статус оценки')
    evaluation_type: SubjectEvaluationType = Field(title='Вид контроля')


class GradedSubject(BaseModel):
    id: int
    short_name: str = Field(title='Краткое название предмета')
    full_name: str = Field(title='Полное название предмета')
    first_grade: SubjectGrade | None = Field(title='Оценка за первый контрольный промежуток')
    second_grade: SubjectGrade | None = Field(title='Оценка за второй контрольный промежуток')
    exam_grade: SubjectGrade | None = Field(title='Оценка за экзаменационную сессию')


class AcademicPerformance(BaseModel):
    total_average_grade: float | None = Field(title='Средний балл по зачётке')
    semester: Semester
    subjects: list[GradedSubject] = Field(title='Предметы с оценками за контрольные промежутки')
