import re
import unicodedata
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def generate_slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

    text = re.sub(r"[^\w\s-]", "", text).strip().lower()

    return re.sub(r"[-\s]+", "-", text)


def generate_slug(title):
    return title.lower().replace(" ", "-")


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
