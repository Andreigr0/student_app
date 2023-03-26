import datetime

from fastapi import UploadFile
from pydantic import BaseModel, Field

from shared.schemas import FileSchema


class ReportStage(BaseModel):
    id: int
    name: str = Field(description='Название периода отчетности (например, "Отчет по итогам 1 этапа")')


class Report(BaseModel):
    id: int
    name: str = Field(title='Название проекта')
    project_deadline: ReportStage = Field(title='Срок сдачи проекта')
    publication_date: datetime.date = Field(title='Дата публикации отчета')
    file: FileSchema = Field(title='Файл отчета')


class ProjectPeriods(BaseModel):
    project_id: int = Field(title='ID проекта')
    project_name: str = Field(title='Название проекта')
    periods: list[ReportStage] = Field(title='Список этапов (периодов отчетности)')


class ReportCreate(BaseModel):
    stage_id: int = Field(title='ID этапа (периода отчетности)')
    file: UploadFile = Field(title='Файл отчета')


class ReportUpdate(BaseModel):
    report_id: int = Field(title='ID отчета')
    file: UploadFile = Field(title='Файл отчета')
