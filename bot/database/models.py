from sqlalchemy import String, Text, BigInteger, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    # updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Users(Base):
    __tablename__ = 'user'
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(20), nullable=True)


class Catalogs(Base):
    __tablename__ = 'catalog'
    name: Mapped[str] = mapped_column(String(50), unique=True)


class Categories(Base):
    __tablename__ = 'category'
    name: Mapped[str] = mapped_column(String(50))
    catalog_id: Mapped[int] = mapped_column()


class UnderCategories(Base):
    __tablename__ = 'under_category'
    name: Mapped[str] = mapped_column(String(50))
    categories_id: Mapped[int] = mapped_column()


class Products(Base):
    __tablename__ = 'product'
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image: Mapped[str] = mapped_column(String(250), nullable=True)
    price: Mapped[float] = mapped_column(default=0.00)
    undercategories_id: Mapped[int] = mapped_column()


class Orders(Base):
    __tablename__ = 'order'
    user_id: Mapped[int] = mapped_column()
    address: Mapped[str] = mapped_column(String(250), nullable=True)
    ammont: Mapped[float] = mapped_column(default=0.00)
    payment_number: Mapped[str] = mapped_column(String(250), nullable=True)
    date_paid: Mapped[DateTime] = mapped_column(DateTime, nullable=True)


class Carts(Base):
    __tablename__ = 'cart'
    order_id: Mapped[int] = mapped_column()
    product_id: Mapped[int] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    ammont: Mapped[float] = mapped_column(default=0.00)


class Questions(Base):
    __tablename__ = 'question'
    user_id: Mapped[int] = mapped_column()
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text, nullable=True)


class Dispatchs(Base):
    __tablename__ = 'dispatch'
    text: Mapped[str] = mapped_column(Text)
    ready: Mapped[bool] = mapped_column(default=False, nullable=True)


class Subscriptions(Base):
    __tablename__ = 'subscription'
    name: Mapped[str] = mapped_column(String(50))
    url: Mapped[str] = mapped_column(String(50))
