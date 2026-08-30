from app.database import SessionLocal
from app.services.seed import seed_database


def run_seed() -> None:
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
