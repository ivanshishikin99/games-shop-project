import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.crud import (
    create_user,
    delete_user,
    login_user,
    update_user_full,
    update_user_partial,
)
from api_v1.users.schemas import UserCreate, UserRead, UserUpdate, UserUpdatePartial
from core.models import User, VerificationToken
from mailing.email_helper import generate_secret_verification_code
from tasks import send_welcome_email
from tasks.tasks import send_email_verification_code
from utils.db_helper import db_helper
from utils.token_helpers import (
    TokenModel,
    create_access_token,
    create_refresh_token,
    get_user_by_token,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register_user",
    response_model=UserRead,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def register_user_view(
    user: UserCreate, session: AsyncSession = Depends(db_helper.session_getter)
) -> User:
    user_created = await create_user(user=user, session=session)
    if user_created.email:
        send_welcome_email.delay(
            user_id=user_created.id,
            user_email=user_created.email,
            user_username=user_created.username,
        )
    return user_created


@router.post("/login", response_model=TokenModel, status_code=status.HTTP_200_OK)
async def login_user_view(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> TokenModel:
    user = await login_user(
        username=form_data.username, password=form_data.password, session=session
    )
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return TokenModel(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout")
async def logout_user_view(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"You have logged out successfully!"}


@router.get(
    "/get_user_info",
    response_model=UserRead,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_user_info_view(
    user: User = Depends(get_user_by_token),
) -> User | HTTPException:
    return user


@router.patch(
    "/update_user_info_partial",
    response_model=UserRead,
    response_model_exclude_none=True,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_user_info_partial_view(
    user_info: UserUpdatePartial,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_user_by_token),
) -> User | HTTPException:
    return await update_user_partial(
        user_to_update=user, user_info=user_info, session=session
    )


@router.put(
    "/update_user_info_full",
    response_model=UserRead,
    response_model_exclude_none=True,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_user_info_full_view(
    user_info: UserUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_user_by_token),
):
    return await update_user_full(
        user_to_update=user, user_info=user_info, session=session
    )


@router.delete("/delete_user")
async def delete_user_view(
    user: User = Depends(get_user_by_token),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await delete_user(user=user, session=session)


@router.post("/verify_email")
async def verify_email_view(
    user: User = Depends(get_user_by_token),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    if not user.email:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Please, specify your email in your profile.",
        )
    if user.verified:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Your email has already been verified.",
        )
    secret_code = generate_secret_verification_code()
    send_email_verification_code.delay(
        user_id=user.id, user_email=user.email, secret_code=secret_code
    )
    verification_token = VerificationToken(
        **{"token": secret_code, "user_email": user.email}
    )
    session.add(verification_token)
    await session.commit()
    await session.refresh(verification_token)
    return {
        "A secret code has been sent, please check your email. Beware that the token is only valid for 1 hour."
    }


@router.post("/verify_email_token")
async def verify_email_token_view(
    code: uuid.UUID,
    user: User = Depends(get_user_by_token),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    statement = select(VerificationToken).where(VerificationToken.token == code)
    token = await session.execute(statement)
    token = token.scalar_one()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong code."
        )
    user.verified = True
    user.role_access = "Verified user"
    await session.delete(token)
    await session.commit()
    return {"Your email has successfully been verified!"}
