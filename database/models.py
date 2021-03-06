import datetime as dt

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):  # type: ignore
    __abstract__ = True

    uuid = sa.Column(
        sa.Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True,
    )
    created_at = sa.Column(
        sa.DateTime, nullable=False, default=dt.datetime.now
    )
    updated_at = sa.Column(
        sa.DateTime,
        nullable=False,
        default=dt.datetime.now,
        onupdate=dt.datetime.now,
    )

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(id={self.id!r})>'


class ShopUnit(BaseModel):
    __tablename__ = 'shop_unit'

    id = sa.Column(sa.String, nullable=False, unique=True)
    name = sa.Column(sa.String, nullable=False)
    type = sa.Column(sa.String, nullable=False)
    price = sa.Column(sa.Integer, nullable=True)
    parentId = sa.Column(
        sa.String,
        sa.ForeignKey('shop_unit.id', ondelete='CASCADE'),
        nullable=True,
    )
    date = sa.Column(sa.String, nullable=False)

    offers_count = sa.Column(sa.Integer, nullable=True)
    children_prices_sum = sa.Column(sa.Integer, nullable=True)

    dt_date = sa.Column(sa.DateTime, nullable=False)

    children = sa.orm.relationship(
        'ShopUnit',
        backref=sa.orm.backref('parent', remote_side=[id]),
        cascade='all, delete',
    )
    stats = sa.orm.relationship(
        'ShopUnitStatisticUnit',
        cascade='all, delete',
    )


class ShopUnitStatisticUnit(BaseModel):
    __tablename__ = 'shop_unit_statistic_unit'

    id = sa.Column(
        sa.String,
        sa.ForeignKey('shop_unit.id', ondelete='CASCADE'),
        nullable=False,
    )
    name = sa.Column(sa.String, nullable=False)
    type = sa.Column(sa.String, nullable=False)
    price = sa.Column(sa.Integer, nullable=True)
    parentId = sa.Column(sa.String, nullable=True)
    date = sa.Column(sa.DateTime, nullable=False)
