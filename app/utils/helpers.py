import bcrypt


def hash_passwd(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(
        password=password.encode(),
        salt=salt,
    )


def verify_password(password: str, hashed_password: bytes) -> bool:

    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
