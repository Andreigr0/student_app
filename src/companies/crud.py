from sqlalchemy import text, case, func, and_
from sqlalchemy.orm import Session

from app.exceptions import ModelNotFoundException
from app.models import CompanyModel
from projects.models import ProjectModel, ProjectsCompaniesModel
from shared.schemas import PaginationQuery


def get_companies(db: Session, pagination: PaginationQuery):
    # query = db.query(
    #     CompanyModel,
    #     func.count(case((and_(ProjectModel.status.in_(['under_recruitment', 'recruited']), ProjectsCompaniesModel.type == 'organizer'), ProjectModel.id))).label('active_projects_count'),
    #     func.count(case((ProjectsCompaniesModel.type == 'organizer', ProjectModel.id))).label('total_projects_count')
    # ).join(
    #     ProjectsCompaniesModel,
    #     CompanyModel.id == ProjectsCompaniesModel.company_id,
    #     isouter=True  # This makes it a LEFT JOIN
    # ).join(
    #     ProjectModel,
    #     ProjectsCompaniesModel.project_id == ProjectModel.id,
    #     isouter=True  # This makes it a LEFT JOIN
    # ).group_by(
    #     CompanyModel.id
    # )

    offset = (pagination.page - 1) * pagination.per_page

    query = db.execute(text('''
SELECT c.*,
       COUNT(DISTINCT CASE WHEN p.status IN ('under_recruitment', 'recruited') AND pc.type = 'organizer' THEN p.id END) AS active_projects_count,
       COUNT(DISTINCT CASE WHEN pc.type = 'organizer' THEN p.id END) AS total_projects_count
FROM companies c
LEFT JOIN projects_companies pc ON c.id = pc.company_id
LEFT JOIN projects p ON pc.project_id = p.id
where c.id > {offset}
GROUP BY c.id
limit {per_page}
    '''.format(offset=offset, per_page=pagination.per_page)))

    keys = query.keys()
    results = [dict(zip(keys, row)) for row in query]
    return results

    query = db.query(CompanyModel)

    query = query.offset(offset).limit(pagination.per_page)

    return query.all()


def get_company(db: Session, company_id: int):
    company = db.query(CompanyModel).get(company_id)
    if not company:
        raise ModelNotFoundException(CompanyModel)
    return company


def get_company_projects(db: Session, company_id: int):
    company = get_company(db=db, company_id=company_id)
    return company.organized_projects.all()
