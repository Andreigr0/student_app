from enum import Enum


class Tags(str, Enum):
    projects = 'Проекты'
    student = 'Личный профиль студента'
    students = 'Публичный профиль студента'
    companies = 'Компании'
    curriculum = 'Дисциплины'
    reports = 'Отчеты'
    invitations = 'Приглашения'
    portfolio = 'Портфолио'
    reviews = 'Отзывы'
    competencies = 'Компетенции'
    academic_performance = 'Успеваемость'
    attendance = 'Посещаемость'
    contacts = 'Контакты'

    schedule = 'Расписание'
    notifications_history = 'История уведомлений'
