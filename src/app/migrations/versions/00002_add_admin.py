"""add_admin

Revision ID: ff218b5980c1
Revises: 871cecbd250c
Create Date: 2023-12-01 20:30:41.727169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base


# revision identifiers, used by Alembic.
revision: str = 'ff218b5980c1'
down_revision: Union[str, None] = '871cecbd250c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

Base = declarative_base()


class UserAlchemyModel(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.BigInteger, primary_key=True)
    username = sa.Column(sa.String(length=100), index=True, nullable=False, unique=True)
    password_hash = sa.Column(sa.String(length=60), nullable=False)
    is_admin = sa.Column(sa.Boolean, nullable=False)

    advertisements = orm.relationship('AdvertisementAlchemyModel', back_populates='owner')


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    session.execute(
        sa.insert(UserAlchemyModel).values(
            username='admin',
            password_hash='$2b$12$NK4NKddxBPm4Sb9rGrMJdOgfspW7AQzDYTvXhnh.qKc2QF/kI68i2',
            is_admin=True,
        ),
    )
    session.commit()




def downgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    session.execute(
        sa.delete(UserAlchemyModel).where(
            UserAlchemyModel.username == 'admin',
        ),
    )
    session.commit()
