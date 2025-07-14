from sqlalchemy.orm import Session

class SQLAlchemyRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, obj):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_by_id(self, model, id_):
        return self.session.query(model).get(id_)

    def get_by_filter(self, model, **filters):
        return self.session.query(model).filter_by(**filters).all()