"""API routes."""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from .models import AccessToken, Login, Register, Resume, ResumeList, \
    ResumeShort, ResumesView, Salary, Tokens, RefreshToken, \
    UpdateMe, User, Vacancy, VacancyList, VacancyShort, \
    VacanciesView, View, ErrorResponse

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
def register(register: Register) -> Tokens:
    """Register a user."""
    return Tokens(
        access_token="access_token",  # nosec
        refresh_token="refresh_token"
    )


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
def login(login: Login) -> Tokens:
    """Login."""
    return Tokens(
        access_token="access_token",  # nosec
        refresh_token="refresh_token"
    )


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
def refresh_token(refresh_token: RefreshToken) -> AccessToken:
    """Refresh expired access token."""
    return AccessToken(access_token="access_token")  # nosec


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
def update_me(update_me: UpdateMe, token: str = Depends(oauth2_scheme)):
    """Update user information. Requires authentication."""
    pass


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
def get_me(token: str = Depends(oauth2_scheme)) -> User:
    """Get user information. Requires authentication."""
    return User(
        first_name="John",
        last_name="Doe",
        email="john_doe@example.com"
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
def liked_vacancies(
        view: View,
        token: str = Depends(oauth2_scheme)
) -> VacancyList:
    """View the list of liked vacancies. Requires authentication."""
    return VacancyList(
        count=0,
        vacancies=[
            VacancyShort(
                id=0,
                title="Programmer",
                salary=Salary(type="monthly")
            )
        ]
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
def like_vacancy(id: int, token: str = Depends(oauth2_scheme)):
    """Add a vacancy to liked. Requires authentication."""
    pass


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
def unlike_vacancy(id: int, token: str = Depends(oauth2_scheme)):
    """Remove a vacancy from liked. Requires authentication."""
    pass


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
def liked_resumes(
        view: View,
        token: str = Depends(oauth2_scheme)
) -> ResumeList:
    """View the list of liked resumes. Requires authentication."""
    return ResumeList(
        count=0,
        resumes=[
            ResumeShort(
                id=0,
                title="Programmer",
                salary=Salary(type="monthly")
            )
        ]
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
def like_resume(id: int, token: str = Depends(oauth2_scheme)):
    """Add a resume to liked. Requires authentication."""
    pass


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
def unlike_resume(id: int, token: str = Depends(oauth2_scheme)):
    """Remove a resume from liked. Requires authentication."""
    pass


@router.post("/vacancies", responses={
    200: {
        "model": VacancyList,
        "description": "List of all available vacancies"
    },
})
def vacancies(vacancies_view: VacanciesView) -> VacancyList:
    """List all available vacancies."""
    return VacancyList(
        count=0,
        vacancies=[
            VacancyShort(
                id=0,
                title="Programmer",
                salary=Salary(type="monthly")
            )
        ]
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
def vacancy(id: int) -> Vacancy:
    """Get a vacancy by ID."""
    return Vacancy(
        id=id,
        external_id="0",
        title="Programmer",
        salary=Salary(type="monthly"),
        employment_types=[]
    )


@router.post("/resumes", responses={
    200: {
        "model": ResumeList,
        "description": "List of all available resumes"
    },
})
def resumes(resumes_view: ResumesView) -> ResumeList:
    """List all available resumes."""
    return ResumeList(
        count=0,
        resumes=[
            ResumeShort(
                id=0,
                title="Programmer",
                salary=Salary(type="monthly")
            )
        ]
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
def resume(id: int) -> Resume:
    """Get a resume by ID."""
    return Resume(
        id=id,
        external_id="0",
        title="Programmer",
        salary=Salary(type="monthly")
    )
