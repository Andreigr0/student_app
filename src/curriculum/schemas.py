from pydantic import BaseModel, Field

from shared.schemas import FileSchema, Semester


class Subject(BaseModel):
    id: int
    name: str = Field(title='Название предмета')
    is_adaptive: bool = Field(title='Адаптивная дисциплина', default=False)
    evaluation: str = Field(title='Оценка')


class Curriculum(BaseModel):
    id: int
    semester: Semester
    plan: FileSchema = Field(title='Учебный план в PDF')
    subjects: list[Subject] = Field(title='Предметы')


class Literature(BaseModel):
    id: int
    name: str = Field(title='Название литературы')
    available: int = Field(title='Доступно в библиотеке', default=0)
    file: FileSchema | None = Field(title='Ссылка на файл')


class LiteratureResult(BaseModel):
    main: list[Literature] | None = Field(title='Основная литература')
    additional: list[Literature] | None = Field(title='Дополнительная литература')
    teaching_aids: list[Literature] | None = Field(title='Учебно-методические пособия')


class LiteratureDetails(Literature):
    type: str = Field(title='Тип литературы, например: Учебное пособие')
    author: str = Field(title='Автор')
    year: int = Field(title='Год издания')
    pages: int = Field(title='Количество страниц')
    description: str = Field(title='Описание')


class AssessmentLearningOutcome(BaseModel):
    type: str = Field(title='Вид контроля')
    semester: int = Field(title='Семестр')


class SemesterSpentHours(BaseModel):
    semester: int | None = Field(title='Семестр')
    practical_exercises: int = Field(title='Практические занятия', default=0)
    independent_work: int = Field(title='Самостоятельная работа', default=0)
    independent_work_practical: int = Field(title='из них практическая подготовка', default=0)
    total: int = Field(title='Общая трудоемкость', default=0)


class AcquiredCompetency(BaseModel):
    code: str = Field(title='Код')
    description: str = Field(title='Содержание')


class SubjectDetails(Subject):
    plan: FileSchema = Field(title='План занятий и лекций')
    training_form: str | None = Field(title='Форма обучения')
    study_period: str | None = Field(title='Период обучения (например: 5 семестр)')
    providing_cathedra: str | None = Field(title='Обеспечивающая кафедра')
    literature: LiteratureResult = Field(title='Литература')
    assessment_learning_outcomes: list[AssessmentLearningOutcome] = Field(title='Оценка результатов обучения')
    semesters_spent_hours: list[SemesterSpentHours] = Field(title='Объем дисциплины и виды учебной деятельности')
    acquired_competencies: list[AcquiredCompetency] = Field(title='Приобретаемые компетенции')
