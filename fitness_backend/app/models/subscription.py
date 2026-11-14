from sqlalchemy import Column, Integer, String, Date, ForeignKey, DECIMAL, Boolean, Text
from sqlalchemy.orm import relationship
from ..database import Base

class SubscriptionAccessLevel(Base):
    __tablename__ = "subscription_access_level"
    
    id = Column(Integer, primary_key=True, index=True)
    access_level_name = Column(String(250), nullable=False)
    access_description = Column(Text)

class SubscriptionActivity(Base):
    __tablename__ = "subscription_activity"
    
    id = Column(Integer, primary_key=True, index=True)
    status_name = Column(String(100), nullable=False)
    activity_flag = Column(Boolean, default=True)

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    subscription_type = Column(String(250), nullable=False)
    price = Column(DECIMAL(10, 2))
    validity_period = Column(Integer)  # in days
    subscription_access_level_id = Column(Integer, ForeignKey("subscription_access_level.id"))
    
    access_level = relationship("SubscriptionAccessLevel")
    client_subscriptions = relationship("ClientSubscription", back_populates="subscription")

class ClientSubscription(Base):
    __tablename__ = "client_subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    start_action_date = Column(Date)
    end_action_date = Column(Date)
    subscription_activity_id = Column(Integer, ForeignKey("subscription_activity.id"))
    
    client = relationship("Client", back_populates="subscriptions")
    subscription = relationship("Subscription", back_populates="client_subscriptions")
    activity = relationship("SubscriptionActivity")