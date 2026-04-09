from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base
from app.repositories.faq_repository import FAQRepository
from app.schemas import FAQCreate

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    url = DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def setup_function():
    Base.metadata.create_all(bind=engine)

def teardown_function():
    Base.metadata.drop_all(bind=engine)

def test_create_and_get_active_faqs():
    db = TestSessionLocal()
    repo = FAQRepository(db)

    repo.create_faq(
        FAQCreate(
            question="How can I reset my password?",
            answer="Click the forgot password link on the login page.",
            category="Account",
            tags="password, login",
            is_active=1
        )
    )

    repo.create_faq(
        FAQCreate(
            question="How do I contact support?",
            answer="Email support@example.com.",
            category="Support",
            tags="support, contact",
            is_active=1
        )
    )

    faqs = repo.get_all_active_faqs()

    assert len(faqs) == 2
    assert faqs[0].question == "How can I reset my password?"
    assert faqs[0].category == "Account"
    assert faqs[1].question == "How do I contact support?"
    assert faqs[1].category == "Support"

    db.close()

def test_inactive_faq_is_not_returned():
    db = TestSessionLocal()
    repo = FAQRepository(db)

    repo.create_faq(
        FAQCreate(
            question="Active FAQ",
            answer="This should be returned",
            category="General",
            tags="test",
            is_active=1
        )
    )

    repo.create_faq(
        FAQCreate(
            question="Inactive FAQ",
            answer="This should NOT be returned",
            category="General",
            tags="test",
            is_active=0
        )
    )

    faqs = repo.get_all_active_faqs()

    assert len(faqs) == 1
    assert faqs[0].question == "Active FAQ"

    db.close()
    