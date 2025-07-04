from fastapi import HTTPException, status

from core.models import User


def super_user_validate(user: User) -> bool | HTTPException:
    if not user.role_access == "Super user":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to view this page.",
        )
    return True
