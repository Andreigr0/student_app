from pydantic import BaseModel, Field

from shared.schemas import ValueSchema


class PersonShort(BaseModel):
    id: int
    last_name: str = Field(title='Фамилия')
    first_name: str = Field(title='Имя')
    patronymic: str | None = Field(title='Отчество')


class ContactInfo(BaseModel):
    address: str | None = Field(title='Адрес')
    phone: str | None = Field(title='Телефон')
    inner_phone: str | None = Field(title='Внутренний телефон')
    email: str | None = Field(title='Email')
    site: str | None = Field(title='Сайт')


class Person(PersonShort, ContactInfo):
    position: str = Field(title='Должность')
    degree: str | None = Field(title='Ученая степень')


class Department(ContactInfo):
    id: int
    name: str = Field(title='Название')
    responsible: PersonShort = Field(title='Ответственный за заполнение контактов')
    employees: list[PersonShort] = Field(title='Сотрудники')
    departments: list['Department'] | None = Field(title='Подразделения')


class Position(ContactInfo):
    id: int
    name: str = Field(title='Название должности (например, "Профессор")')
    faculty: ValueSchema = Field(title='Факультет')


class Publication(BaseModel):
    name: str = Field(title='Название')
    description: str | None = Field(title='Описание')
    link: str = Field(title='Ссылка')


class PersonDetails(Person):
    is_male: bool = Field(title='Пол (true - мужской, false - женский)')
    image: str | None = Field(title='Фото')
    faculty: ValueSchema | None = Field(title='Факультет')
    subjects: list[ValueSchema] | None = Field(title='Преподаваемые дисциплины')
    biography: str | None = Field(title='Биография')
    other_positions: list[Position] | None = Field(title='Другие должности')
    publications: list[Publication] | None = Field(title='Сведения о публикациях')
