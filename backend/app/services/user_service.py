import random
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password

def generate_anonymous_name() -> str:
    adjectives = ["Calm", "Bright", "Quiet", "Kind", "Blue", "Soft"]
    nouns = ["River", "Leaf", "Sky", "Stone", "Cloud", "Star"]
    number = random.randint(100, 999)

    return f"{random.choice(adjectives)}{random.choice(nouns)}{number}"

def get_user_by_email(db: Session, email:str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, name: str, email: str, password: str) -> User:
    anonymous_name = generate_anonymous_name()

    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        anonymous_name=anonymous_name
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
