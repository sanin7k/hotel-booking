import secrets
from backend.app.models.models import User

def generate_internal_username(prefix="user", length=6):
  return f"{prefix}_{secrets.token_hex(length // 2)}"

async def get_unique_internal_username(db):
  while True:
    candidate = generate_internal_username()
    exists = db.query(User).filter(User.username == candidate).first()
    if not exists:
      return candidate