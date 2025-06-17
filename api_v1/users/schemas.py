from datetime import date, datetime

from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    username: str
    password: str
    verified: bool = False
    role_access: str = 'Unverified user'
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    country: str | None = None
    phone_number: str | None = None
    sex: str | None = None
    date_of_birth: date | None = None

    @field_validator('first_name','last_name', 'country')
    @classmethod
    def capitalize_field(cls, val: str | None) -> str:
        if val:
            return val.capitalize()

    @field_validator('password')
    @classmethod
    def validate_password(cls, val: str) -> str | ValueError:
        special_symbols = ['@', '#', '$', '%', '&', '!', '?', '[', ']',
                           '(', ')', '£', '€', '¥', '<', '>', '{', '}',
                           '+', '-', '=', '\\', '/', ',', '.', ':', ';', '`', '#', '^', '*']
        special_symbols_flag = False
        digits_flag = False
        if val.lower() == val:
            raise ValueError('Your password must include at least one upper character.')
        for i in val:
            if i in special_symbols:
                special_symbols_flag = True
            if i.isdigit():
                digits_flag = True
        if not special_symbols_flag:
            raise ValueError('Your password must include at least one special symbol.')
        if not digits_flag:
            raise ValueError('Your password must include at least one digit.')
        if len(val) < 8:
            raise ValueError('Your password must be at least 8 characters long.')
        if len(val) > 100:
            raise ValueError('Your password must not exceed 100 characters.')
        return val

    @field_validator('phone_number')
    @classmethod
    def verify_phone_number(cls, val: str) -> str | ValueError:
        if val[0] != '+':
            raise ValueError("Your phone number must start with the '+' symbol.")
        if val[1] != '7' and val[1] != '8':
            raise ValueError("Your phone number's first digit must be either 7 or 8.")
        if not val[1::].isdigit():
            raise ValueError('Incorrect phone number format.')
        if len(val) < 12:
            raise ValueError('Your phone number is too short.')
        if len(val) > 12:
            raise ValueError('Your phone number is too long.')
        return val

    @field_validator('sex')
    @classmethod
    def templatize_sex(cls, val: str) -> str | ValueError:
        if (not val.startswith('m') and not val.startswith('M')
                and not val.startswith('f') and not val.startswith('F')):
            raise ValueError('Incorrect sex.')
        if val.startswith('m') or val.startswith('M'):
            return 'Male'
        return 'Female'

    @field_validator('role_access')
    @classmethod
    def validate_role_access(cls, val: str) -> str | ValueError:
        if not val == 'Unverified user':
            raise ValueError('Incorrect role access.')
        return val

    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls, val: date) -> date | ValueError:
        if val.year > datetime.now().year or val.year < 1909:
            raise ValueError('Incorrect year of birth.')
        return val

    @field_validator('verified')
    @classmethod
    def validate_verified_field(cls, val: bool) -> bool:
        return False

    @field_validator('username')
    @classmethod
    def validate_username(cls, val: str) -> str | ValueError:
        if len(val) < 4:
            raise ValueError('Your username is too short.')
        if len(val) > 30:
            raise ValueError('Your username is too long.')
        return val


class UserRead(BaseModel):
    username: str
    verified: bool
    email: EmailStr | None
    first_name: str | None
    last_name: str | None
    country: str | None
    phone_number: str | None
    sex: str | None
    date_of_birth: date | None


class UserUpdatePartial(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    country: str | None = None
    phone_number: str | None = None
    sex: str | None = None
    date_of_birth: date | None = None

    @field_validator('phone_number')
    @classmethod
    def verify_phone_number(cls, val: str) -> str | ValueError:
        if val[0] != '+':
            raise ValueError("Your phone number must start with the '+' symbol.")
        if val[1] != '7' and val[1] != '8':
            raise ValueError("Your phone number's first digit must be either 7 or 8.")
        if not val[1::].isdigit():
            raise ValueError('Incorrect phone number format.')
        if len(val) < 12:
            raise ValueError('Your phone number is too short.')
        if len(val) > 12:
            raise ValueError('Your phone number is too long.')
        return val

    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls, val: date) -> date | ValueError:
        if val.year > datetime.now().year or val.year < 1909:
            raise ValueError('Incorrect year of birth.')
        return val

    @field_validator('sex')
    @classmethod
    def templatize_sex(cls, val: str) -> str | ValueError:
        if (not val.startswith('m') and not val.startswith('M')
                and not val.startswith('f') and not val.startswith('F')):
            raise ValueError('Incorrect sex.')
        if val.startswith('m') or val.startswith('M'):
            return 'Male'
        return 'Female'

    @field_validator('first_name', 'last_name', 'country')
    @classmethod
    def capitalize_field(cls, val: str | None) -> str:
        if val:
            return val.capitalize()


class UserUpdate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    country: str
    phone_number: str
    sex: str
    date_of_birth: date

    @field_validator('phone_number')
    @classmethod
    def verify_phone_number(cls, val: str) -> str | ValueError:
        if val[0] != '+':
            raise ValueError("Your phone number must start with the '+' symbol.")
        if val[1] != '7' and val[1] != '8':
            raise ValueError("Your phone number's first digit must be either 7 or 8.")
        if not val[1::].isdigit():
            raise ValueError('Incorrect phone number format.')
        if len(val) < 12:
            raise ValueError('Your phone number is too short.')
        if len(val) > 12:
            raise ValueError('Your phone number is too long.')
        return val

    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls, val: date) -> date | ValueError:
        if val.year > datetime.now().year or val.year < 1909:
            raise ValueError('Incorrect year of birth.')
        return val

    @field_validator('sex')
    @classmethod
    def templatize_sex(cls, val: str) -> str | ValueError:
        if (not val.startswith('m') and not val.startswith('M')
                and not val.startswith('f') and not val.startswith('F')):
            raise ValueError('Incorrect sex.')
        if val.startswith('m') or val.startswith('M'):
            return 'Male'
        return 'Female'

    @field_validator('first_name', 'last_name', 'country')
    @classmethod
    def capitalize_field(cls, val: str | None) -> str:
        if val:
            return val.capitalize()

    

