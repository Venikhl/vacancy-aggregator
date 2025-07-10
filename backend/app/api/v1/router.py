"""API routes."""

import os

from fastapi.responses import FileResponse
from app.core.config import get_settings
from app.database.database import get_async_session
from app.database.crud import get_experience_category_by_name, user, \
    get_location_by_region, vacancy as dbvacancy, resume as dbresume
import app.database.models as dbmodels
from app.services.jwt import create_access_token, create_refresh_token, \
    verify_token
from app.services.security import hash_password, verify_password
from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .models import AccessToken, Company, EmploymentType, \
    ExperienceCategory, Location, Login, Register, Resume, ResumeList, \
    ResumeShort, ResumesView, Salary, Source, Specialization, TimeStamp, \
    Tokens, RefreshToken, UpdateMe, User, Vacancy, VacancyList, \
    VacancyShort, VacanciesView, View, ErrorResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List, Optional
from PIL import Image
from io import BytesIO


router = APIRouter()

bearer_scheme = HTTPBearer()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post("/register", responses={
    200: {
        "model": Tokens,
        "description": "User successfully registered"
    },
    400: {
        "model": ErrorResponse,
        "description": "Email or username already exists"
    },
    422: {
        "model": ErrorResponse,
        "description": "Validation error in registration data"
    }
})
async def register(
    register: Register,
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> Tokens:
    """Register a user."""
    existing_user = await user.get_by_email(session, register.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already taken")

    hashed_password = hash_password(register.password)
    db_user = await user.create(session, {
        "first_name": register.first_name,
        "last_name": register.last_name,
        "email": register.email,
        "hashed_password": hashed_password,
    })

    access_token = create_access_token(db_user.id)
    refresh_token = create_refresh_token(db_user.id)

    return Tokens(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", responses={
    200: {
        "model": Tokens,
        "description": "Successfully logged in"
    },
    401: {
        "model": ErrorResponse,
        "description": "Invalid email or password"
    },
    422: {
        "model": ErrorResponse,
        "description": "Validation error in login data"
    }
})
async def login(
    login: Login,
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> Tokens:
    """Login."""
    db_user = await user.get_by_email(session, email=login.email)
    if not db_user or not verify_password(
        login.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(db_user.id)
    refresh_token = create_refresh_token(db_user.id)

    return Tokens(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh_token", responses={
    200: {
        "model": AccessToken,
        "description": "Access token refreshed"
    },
    401: {
        "model": ErrorResponse,
        "description": "Invalid or expired refresh token"
    },
    422: {
        "model": ErrorResponse,
        "description": "Refresh token not provided or invalid format"
    }
})
async def refresh_token(
    refresh_token: RefreshToken,
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> AccessToken:
    """Refresh expired access token."""
    user_id = verify_token(refresh_token.refresh_token)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Refresh token expired or invalid"
        )

    access_token = create_access_token(user_id)
    return AccessToken(access_token=access_token)


@router.post("/update_me", responses={
    200: {
        "description": "Successfully updated"
    },
    401: {
        "model": ErrorResponse,
        "description": "Missing or invalid access token"
    },
    403: {
        "model": ErrorResponse,
        "description": "Access denied"
    },
    422: {
        "model": ErrorResponse,
        "description": "Validation error in update data"
    }
})
async def update_me(
    update_me: UpdateMe,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    """Update user information. Requires authentication."""
    token = credentials.credentials
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Access token expired or invalid"
        )
    db_user = await user.get_by_id(session, id=user_id)
    if not db_user:
        raise HTTPException(status_code=403, detail="Access denied")
    fields = {}
    if update_me.first_name:
        fields["first_name"] = update_me.first_name
    if update_me.last_name:
        fields["last_name"] = update_me.last_name
    if update_me.email:
        fields["email"] = update_me.email
    if update_me.gender:
        fields["gender"] = update_me.gender
    if update_me.birth_date:
        fields["birth_date"] = update_me.birth_date
    if update_me.current_password or update_me.new_password:
        if not update_me.current_password:
            raise HTTPException(
                status_code=422,
                detail="Current password is empty"
            )
        if not update_me.new_password:
            raise HTTPException(
                status_code=422,
                detail="New password is empty"
            )
        if not verify_password(
            update_me.current_password,
            db_user.hashed_password
        ):
            raise HTTPException(
                status_code=422,
                detail="Current password is incorrect"
            )
        hashed_password = hash_password(update_me.current_password)
        fields["hashed_password"] = hashed_password
    await user.update(session, db_obj=db_user, obj_in=fields)
    return Response(status_code=200)


@router.post("/update_profile_pic", responses={
    200: {
        "description": "Successfully updated"
    },
    400: {
        "description": "Invalid picture format"
    },
    401: {
        "model": ErrorResponse,
        "description": "Missing or invalid access token"
    },
    403: {
        "model": ErrorResponse,
        "description": "Access denied"
    },
})
async def update_profile_pic(
    profile_pic: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    """
    Update user profile picture.

    The picture dimesions should be between 128x128 and 512x512.
    only PNG, JPG, and JPEG are accepted.
    """
    token = credentials.credentials
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Access token expired or invalid"
        )
    contents = await profile_pic.read()
    image = None
    image_format = None
    width = None
    height = None
    try:
        image = Image.open(BytesIO(contents))
        if image.format is not None:
            image_format = image.format.upper()
        width, height = image.size
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid picture format"
        )

    if image_format not in {"PNG", "JPG", "JPEG"}:
        raise HTTPException(
            status_code=400,
            detail="Unsupported picture format. Use PNG or JPEG"
        )

    if not (128 <= width <= 512 and 128 <= height <= 512):
        raise HTTPException(
            status_code=400,
            detail="Unsupported picture dimensions. \
                Only sizes between 128x128 and 512x512 are allowed."
        )

    settings = get_settings()
    filename = f"{user_id}.jpeg"
    save_path = os.path.join(settings.PROFILE_PICTURE_DIRECTORY, filename)

    rgb_image = image.convert("RGB")
    rgb_image.save(save_path, "JPEG", quality=85)

    return Response(status_code=200)


@router.get("/profile_pic/{user_id}", responses={
    200: {
        "description": "Profile picture"
    },
    404: {
        "description": "Profile picture not found"
    }
})
async def profile_pic(user_id: int) -> FileResponse:
    settings = get_settings()
    filename = f"{user_id}.jpeg"
    image_path = os.path.join(settings.PROFILE_PICTURE_DIRECTORY, filename)
    if not os.path.exists(image_path):
        raise HTTPException(
            status_code=404,
            detail="Profile picture not found"
        )

    return FileResponse(path=image_path, media_type="image/jpeg")


@router.post("/get_me", responses={
    200: {
        "model": User,
        "description": "User data retrieved"
    },
    401: {
        "model": ErrorResponse,
        "description": "Missing or invalid access token"
    },
    403: {
        "model": ErrorResponse,
        "description": "Access denied"
    }
})
async def get_me(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> User:
    """Get user information. Requires authentication."""
    token = credentials.credentials
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Access token expired or invalid"
        )
    db_user = await user.get_by_id(session, user_id)
    if not db_user:
        raise HTTPException(status_code=403, detail="Access denied")

    profile_pic_url = None
    settings = get_settings()
    filename = f"{user_id}.jpeg"
    image_path = os.path.join(settings.PROFILE_PICTURE_DIRECTORY, filename)
    if os.path.exists(image_path):
        profile_pic_url = f"{settings.HOST}/api/v1/profile_pic/{user_id}"

    return User(
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        email=db_user.email,
        birth_date=db_user.birth_date,
        gender=db_user.gender,
        profile_pic_url=profile_pic_url,
    )


@router.post("/liked_vacancies", responses={
    200: {
        "model": VacancyList,
        "description": "List of liked vacancies returned"
    },
    401: {
        "model": ErrorResponse,
        "description": "Missing or invalid access token"
    }
})
async def liked_vacancies(
    view: View,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> VacancyList:
    """View the list of liked vacancies. Requires authentication."""
    token = credentials.credentials
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Access token expired or invalid"
        )
    (count, vacancies) = await user.get_favorite_vacancies(
        session,
        user_id,
        view.offset,
        view.count
    )
    short_vacancies = []
    for v in vacancies:
        v_rel = await dbvacancy.get_with_relations(session, v.id)
        if not v_rel:
            continue
        vacancy = db_vacancy_to_vacancy(v_rel)
        short_vacancy = vacancy_to_vacancy_short(vacancy)
        short_vacancies.append(short_vacancy)

    return VacancyList(
        count=count,
        vacancies=short_vacancies
    )


@router.get("/like_vacancy/{id}", responses={
    200: {
        "description": "Vacancy added to likes"
    },
    401: {
        "model": ErrorResponse,
        "description": "Missing or invalid access token"
    },
    404: {
        "model": ErrorResponse,
        "description": "Vacancy not found"
    }
})
async def like_vacancy(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    """Add a vacancy to liked. Requires authentication."""
    token = credentials.credentials
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Access token expired or invalid"
        )
    db_vacancy = await dbvacancy.get_with_relations(session, id)
    if not db_vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    await user.add_favorite_vacancy(session, user_id, db_vacancy.id)


@router.get("/unlike_vacancy/{id}", responses={
    200: {
        "description": "Vacancy removed from likes"
    },
    401: {
        "model": ErrorResponse,
        "description": "Missing or invalid access token"
    },
    404: {
        "model": ErrorResponse,
        "description": "Vacancy not found"
    }
})
async def unlike_vacancy(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    """Remove a vacancy from liked. Requires authentication."""
    token = credentials.credentials
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Access token expired or invalid"
        )
    db_vacancy = await dbvacancy.get_with_relations(session, id)
    if not db_vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    await user.remove_favorite_vacancy(session, user_id, db_vacancy.id)


@router.post("/liked_resumes", responses={
    200: {
        "model": ResumeList,
        "description": "List of liked resumes returned"
    },
    401: {
        "model": ErrorResponse,
        "description": "Missing or invalid access token"
    }
})
async def liked_resumes(
    view: View,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> ResumeList:
    """View the list of liked resumes. Requires authentication."""
    token = credentials.credentials
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Access token expired or invalid"
        )
    (count, resumes) = await user.get_favorite_resumes(
        session,
        user_id,
        view.offset,
        view.count
    )
    short_resumes = []
    for r in resumes:
        r_rel = await dbresume.get_with_relations(session, r.id)
        if not r_rel:
            continue
        resume = db_resume_to_resume(r_rel)
        short_resume = resume_to_resume_short(resume)
        short_resumes.append(short_resume)

    return ResumeList(
        count=count,
        resumes=short_resumes
    )


@router.get("/like_resume/{id}", responses={
    200: {
        "description": "Resume added to likes"
    },
    401: {
        "model": ErrorResponse,
        "description": "Missing or invalid access token"
    },
    404: {
        "model": ErrorResponse,
        "description": "Resume not found"
    }
})
async def like_resume(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    """Add a resume to liked. Requires authentication."""
    token = credentials.credentials
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Access token expired or invalid"
        )
    db_resume = await dbresume.get_with_relations(session, id)
    if not db_resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    await user.add_favorite_vacancy(session, user_id, db_resume.id)


@router.get("/unlike_resume/{id}", responses={
    200: {
        "description": "Resume removed from likes"
    },
    401: {
        "model": ErrorResponse,
        "description": "Missing or invalid access token"
    },
    404: {
        "model": ErrorResponse,
        "description": "Resume not found"
    }
})
async def unlike_resume(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    """Remove a resume from liked. Requires authentication."""
    token = credentials.credentials
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Access token expired or invalid"
        )
    db_resume = await dbresume.get_with_relations(session, id)
    if not db_resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    await user.remove_favorite_vacancy(session, user_id, db_resume.id)


@router.post("/vacancies", responses={
    200: {
        "model": VacancyList,
        "description": "List of all available vacancies"
    },
})
async def vacancies(
    vacancies_view: VacanciesView,
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> VacancyList:
    """List all available vacancies."""
    filter = vacancies_view.filter
    experience_category_ids: Optional[List[int]] = None
    if not filter.experience_categories:
        experience_category_ids = None
    else:
        experience_category_ids = []
        for experience_category in filter.experience_categories:
            db_experience_category = \
                await get_experience_category_by_name(
                    session,
                    experience_category.name
                )
            if not db_experience_category:
                continue
            experience_category_ids.append(db_experience_category.id)
    location_id: Optional[int] = None
    if filter.location:
        db_location = await get_location_by_region(
            session,
            filter.location.region
        )
        if db_location:
            location_id = db_location.location_id

    offset = vacancies_view.view.offset
    count = vacancies_view.view.count

    db_vacancies = await dbvacancy.search(
        session,
        title=filter.title,
        min_salary=filter.salary_min,
        max_salary=filter.salary_max,
        experience_category_ids=experience_category_ids,
        location_id=location_id,
        offset=offset,
        limit=count
    )
    vacancies = []
    vacancy_count = 0
    if db_vacancies:
        (total_count, db_vacancy_list) = db_vacancies
        vacancy_count = total_count
        for db_vacancy in db_vacancy_list:
            v_rel = await dbvacancy.get_with_relations(
                session,
                db_vacancy.id
            )
            if not v_rel:
                continue
            vacancy = db_vacancy_to_vacancy(v_rel)
            vacancy_short = vacancy_to_vacancy_short(vacancy)
            vacancies.append(vacancy_short)

    return VacancyList(
        count=vacancy_count,
        vacancies=vacancies
    )


@router.get("/vacancy/{id}", responses={
    200: {
        "model": Vacancy,
        "description": "Vacancy details"
    },
    404: {
        "model": ErrorResponse,
        "description": "Vacancy not found"
    }
})
async def vacancy(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> Vacancy:
    """Get a vacancy by ID."""
    db_vacancy = await dbvacancy.get_with_relations(session, id)
    if not db_vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return db_vacancy_to_vacancy(db_vacancy)


@router.post("/resumes", responses={
    200: {
        "model": ResumeList,
        "description": "List of all available resumes"
    },
})
async def resumes(
    resumes_view: ResumesView,
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> ResumeList:
    """List all available resumes."""
    filter = resumes_view.filter
    experience_category_ids: Optional[List[int]] = None
    if not filter.experience_categories:
        experience_category_ids = None
    else:
        experience_category_ids = []
        for experience_category in filter.experience_categories:
            db_experience_category = \
                await get_experience_category_by_name(
                    session,
                    experience_category.name
                )
            if not db_experience_category:
                continue
            experience_category_ids.append(db_experience_category.id)
    location_id: Optional[int] = None
    if filter.location:
        db_location = await get_location_by_region(
            session,
            filter.location.region
        )
        if db_location:
            location_id = db_location.location_id
    db_resumes = await dbresume.search(
        session,
        title=filter.title,
        location_id=location_id,
        min_salary=filter.salary_min,
        max_salary=filter.salary_max,
        experience_category_ids=experience_category_ids,
        skills=filter.skills
    )
    resumes = []
    resume_count = 0
    if db_resumes:
        (count, db_resume_list) = db_resumes
        resume_count = count
        for db_resume in db_resume_list:
            r_rel = await dbresume.get_with_relations(
                session,
                db_resume.id
            )
            if not r_rel:
                continue
            resume = db_resume_to_resume(r_rel)
            resume_short = resume_to_resume_short(resume)
            resumes.append(resume_short)

    return ResumeList(
        count=resume_count,
        resumes=resumes
    )


@router.get("/resume/{id}", responses={
    200: {
        "model": Resume,
        "description": "Resume details"
    },
    404: {
        "model": ErrorResponse,
        "description": "Resume not found"
    }
})
async def resume(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> Resume:
    """Get a resume by ID."""
    db_resume = await dbresume.get_with_relations(session, id)
    if not db_resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db_resume_to_resume(db_resume)


def db_source_to_source(db_source: dbmodels.Source | None) -> Source | None:
    """Convert database Source model to API Source model."""
    if not db_source:
        return None
    return Source(
        name=db_source.name
    )


def db_company_to_company(
    db_company: dbmodels.Company | None
) -> Company | None:
    """Convert database Company model to API Company model."""
    if not db_company:
        return None
    return Company(
        name=db_company.name
    )


def db_experience_category_to_experience_category(
    db_experience_category: dbmodels.ExperienceCategory | None
) -> ExperienceCategory | None:
    """Convert database ExperienceCategory model to API \
    ExperienceCategory model."""
    if not db_experience_category:
        return None
    return ExperienceCategory(
        name=db_experience_category.name
    )


def db_location_to_location(
    db_location: dbmodels.Location | None
) -> Location | None:
    """Convert database Location model to API Location model."""
    if not db_location:
        return None
    return Location(
        region=db_location.region
    )


def db_specialization_to_specialization(
    db_specialization: dbmodels.Specialization | None
) -> Specialization | None:
    """Convert database Specialization model to API Specialization model."""
    if not db_specialization:
        return None
    return Specialization(
        specialization=db_specialization.specialization
    )


def db_employment_type_to_employment_type(
    db_empolyment_type: dbmodels.EmploymentType | None
) -> EmploymentType | None:
    """Convert database EmploymentType model to API \
    EmploymentType model."""
    if not db_empolyment_type:
        return None
    return EmploymentType(
        name=db_empolyment_type.name
    )


def db_employment_types_to_employment_type_list(
    db_employment_types
) -> List[EmploymentType]:
    """Convert database EmploymentType list to API \
    EmploymentType list."""
    return [db_employment_type_to_employment_type(x)
            for x in db_employment_types]


def db_timestamp_to_timestamp(
    db_timestamp
) -> TimeStamp | None:
    """Convert database TimeStamp model to API TimeStamp model."""
    if not db_timestamp:
        return None
    return TimeStamp(
        time_stamp=str(db_timestamp)
    )


def db_vacancy_to_vacancy(db_vacancy: dbmodels.Vacancy) -> Vacancy:
    """Convert database Vacancy model to API Vacancy model."""
    salary = Salary(
        currency=db_vacancy.salary_currency,
        value=db_vacancy.salary_value
    )
    if db_vacancy.salary_type:
        salary.type = db_vacancy.salary_type.name
    return Vacancy(
        id=db_vacancy.id,
        external_id=db_vacancy.external_id,
        source=db_source_to_source(db_vacancy.source),
        title=db_vacancy.title,
        description=db_vacancy.description,
        company=db_company_to_company(db_vacancy.company),
        salary=salary,
        experience_category=db_experience_category_to_experience_category(
            db_vacancy.experience_category
        ),
        location=db_location_to_location(db_vacancy.location),
        specialization=db_specialization_to_specialization(
            db_vacancy.specialization
        ),
        employment_types=db_employment_types_to_employment_type_list(
            db_vacancy.employment_types
        ),
        published_at=db_timestamp_to_timestamp(
            db_vacancy.published_at
        ),
        contacts=db_vacancy.contacts,
        url=db_vacancy.url
    )


def vacancy_to_vacancy_short(vacancy: Vacancy) -> VacancyShort:
    """Convert Vacancy to short representation."""
    return VacancyShort(
        id=vacancy.id,
        title=vacancy.title,
        description=vacancy.description,
        salary=vacancy.salary
    )


def db_resume_to_resume(db_resume: dbmodels.Resume) -> Resume:
    """Convert database Resume model to API Resume model."""
    salary = Salary(
        currency=db_resume.salary_currency,
        value=db_resume.salary_value
    )
    if db_resume.salary_type:
        salary.type = db_resume.salary_type.name
    return Resume(
        id=db_resume.id,
        external_id=db_resume.external_id,
        source=db_source_to_source(db_resume.source),
        title=db_resume.title,
        salary=salary,
        description=db_resume.description,
        location=db_location_to_location(db_resume.location),
        experience_category=db_experience_category_to_experience_category(
            db_resume.experience_category
        ),
        skills=db_resume.skills_text,
        education=db_resume.education,
        specialization=db_specialization_to_specialization(
            db_resume.specialization
        ),
        first_name=db_resume.first_name,
        last_name=db_resume.last_name,
        middle_name=db_resume.middle_name,
        email=db_resume.email,
        phone_number=db_resume.phone_number,
        published_at=db_timestamp_to_timestamp(
            db_resume.published_at
        )
    )


def resume_to_resume_short(resume: Resume) -> ResumeShort:
    """Convert Resume to short representation."""
    return ResumeShort(
        id=resume.id,
        title=resume.title,
        salary=resume.salary,
        description=resume.description,
        first_name=resume.first_name,
        last_name=resume.last_name,
        middle_name=resume.middle_name
    )
