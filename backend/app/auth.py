import os
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash

from contextlib import contextmanager
from collections.abc import Iterator


# Carga la configuración privada de backend/.env
BACKEND_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_DIR / ".env")

password_hasher = PasswordHash.recommended()

JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

if JWT_EXPIRE_MINUTES <= 0:
    raise ValueError("JWT_EXPIRE_MINUTES debe ser un número positivo.")


def get_database_path() -> Path:
    """Devuelve la ruta configurada para la base de datos SQLite."""
    configured_path = os.getenv("DATABASE_PATH")

    if configured_path:
        return Path(configured_path)

    return BACKEND_DIR / "data" / "app.db"


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Abre la base de datos y cierra la conexión al terminar."""
    database_path = get_database_path()
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.commit()

        yield connection

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_jwt_secret() -> str:
    """Obtiene y valida la clave secreta JWT."""
    secret = os.getenv("JWT_SECRET_KEY")

    if not secret:
        raise RuntimeError("Falta configurar JWT_SECRET_KEY.")

    if len(secret.encode("utf-8")) < 32:
        raise RuntimeError(
            "JWT_SECRET_KEY debe tener al menos 32 bytes."
        )

    return secret


def hash_password(password: str) -> str:
    """Genera un hash seguro de la contraseña."""
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Comprueba una contraseña sin almacenarla en texto plano."""
    return password_hasher.verify(password, password_hash)


def create_user(email: str, password: str) -> dict | None:
    """Registra un usuario. Devuelve None si el correo ya existe."""
    normalized_email = email.strip().lower()
    password_hash = hash_password(password)
    created_at = datetime.now(timezone.utc).isoformat()

    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO users (email, password_hash, created_at)
                VALUES (?, ?, ?)
                """,
                (normalized_email, password_hash, created_at),
            )
            user_id = cursor.lastrowid

            return {
                "id": user_id,
                "email": normalized_email,
            }

    except sqlite3.IntegrityError:
        return None


def get_user_by_email(email: str) -> dict | None:
    """Busca un usuario por correo electrónico."""
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, email, password_hash FROM users WHERE email = ?",
            (email.strip().lower(),),
        ).fetchone()

    return dict(row) if row else None


def get_user_by_id(user_id: int) -> dict | None:
    """Busca un usuario por su identificador."""
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, email FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()

    return dict(row) if row else None


def authenticate_user(email: str, password: str) -> dict | None:
    """Comprueba las credenciales y devuelve el usuario si son válidas."""
    user = get_user_by_email(email)

    if not user or not verify_password(password, user["password_hash"]):
        return None

    return {
        "id": user["id"],
        "email": user["email"],
    }


def create_access_token(user_id: int) -> str:
    """Crea un token JWT con caducidad."""
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=JWT_EXPIRE_MINUTES),
    }

    return jwt.encode(
        payload,
        get_jwt_secret(),
        algorithm=JWT_ALGORITHM,
    )


def get_user_from_token(token: str) -> dict | None:
    """Valida un JWT y recupera el usuario asociado."""
    try:
        payload = jwt.decode(
            token,
            get_jwt_secret(),
            algorithms=[JWT_ALGORITHM],
        )
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
        return None

    return get_user_by_id(user_id)

