from app.database import SessionLocal, DEFAULT_USERNAME, DEFAULT_PASSWORD
from app.models import User

if (DEFAULT_USERNAME == None or DEFAULT_PASSWORD == None):
    raise EnvironmentError("DEFAULT_USERNAME or DEFAULT_PASSWORD not variable defined")

def init_admin_user():
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        if user_count == 0:
            admin = User(
                username=DEFAULT_USERNAME,
                password=DEFAULT_PASSWORD,
                role="admin"
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()
