from enum import Enum


class Tags(str, Enum):
    projects = 'Проекты'
    student = 'Личный профиль студента'
    students = 'Публичный профиль студента'
    companies = 'Компании'
    curriculum = 'Дисциплины'

    academic_performance = 'Успеваемость'
    attendance = 'Посещаемость'
    schedule = 'Расписание'
    contacts = 'Контакты'
    projects_applications = 'Заявки на проекты'
    invitations = 'Приглашения'
    reports = 'Отчеты'
    notifications_history = 'История уведомлений'
