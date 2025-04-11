from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    TIMESTAMP,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String)
    is_trial_used = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="user")
    devices = relationship("Device", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    support_requests = relationship("SupportRequest", back_populates="user")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    plan = Column(String, nullable=False)  # 'monthly', 'yearly', etc.
    start_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="subscriptions")


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    device_name = Column(String)
    ip_address = Column(String)
    connected_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="devices")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    amount = Column(Numeric(10, 2))
    currency = Column(String, default="RUB")
    payment_method = Column(String)  # 'card', 'crypto', etc.
    status = Column(String)  # 'pending', 'success', 'failed'
    transaction_id = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="payments")


class SupportRequest(Base):
    __tablename__ = "support_requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    message = Column(Text, nullable=False)
    status = Column(String, default="open")  # 'open', 'closed'
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    closed_at = Column(TIMESTAMP, nullable=True)

    user = relationship("User", back_populates="support_requests")
