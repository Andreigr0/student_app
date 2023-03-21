from enum import Enum


class Tags(str, Enum):
    projects = 'Проекты'
    student = 'Личный профиль студента'
    students = 'Публичный профиль студента'
    companies = 'Компании'
    curriculum = 'Дисциплины'
    reports = 'Отчеты'
    invitations = 'Приглашения'

    academic_performance = 'Успеваемость'
    attendance = 'Посещаемость'
    schedule = 'Расписание'
    contacts = 'Контакты'
    notifications_history = 'История уведомлений'
