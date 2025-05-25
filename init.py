import logging
from database import SessionLocal, DEFAULT_USERNAME, DEFAULT_PASSWORD
from models import User

if (DEFAULT_USERNAME == None or DEFAULT_PASSWORD == None):
    raise EnvironmentError("Not DEFAULT_USERNAME or DEFAULT_PASSWORD variable defined")

logger = logging.getLogger("uvicorn")

def init_admin_user():
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        if user_count == 0:
            logger.info("No admin user in database")
            admin = User(
                username=DEFAULT_USERNAME,
                password=DEFAULT_PASSWORD
            )
            db.add(admin)
            db.commit()
            logger.info("Admin user created")
        else:
            logger.info("Users already exist, skipping admin creation")
    finally:
        db.close()
