"""API routes."""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from .models import AccessToken, Login, Register, Resume, ResumeList, \
                    ResumeShort, ResumesView, Salary, Tokens, RefreshToken, \
                    UpdateMe, User, Vacancy, VacancyList, VacancyShort, \
                    VacanciesView, View


router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register")
def register(register: Register) -> Tokens:
    """Register a user."""
    return Tokens(
        access_token="access_token", # nosec
        refresh_token="refresh_token"
    )


@router.post("/login")
def login(login: Login) -> Tokens:
    """Login."""
    return Tokens(
        access_token="access_token", # nosec
        refresh_token="refresh_token"
    )


@router.post("/refresh_token")
def refresh_token(refresh_token: RefreshToken) -> AccessToken:
    """Refresh expired access token."""
    return AccessToken(access_token="access_token") # nosec


@router.post("/update_me")
def update_me(update_me: UpdateMe, token: str = Depends(oauth2_scheme)):
    """Update user information. Requires authentication."""
    pass


@router.post("/get_me")
def get_me(token: str = Depends(oauth2_scheme)) -> User:
    """Get user information. Requires authentication."""
    return User(
        first_name="John",
        last_name="Doe",
        email="john_doe@example.com"
    )


@router.post("/liked_vacancies")
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


@router.get("/like_vacancy/{id}")
def like_vacancy(id: int, token: str = Depends(oauth2_scheme)):
    """Add a vacancy to liked. Requires authentication."""
    pass


@router.get("/unlike_vacancy/{id}")
def unlike_vacancy(id: int, token: str = Depends(oauth2_scheme)):
    """Remove a vacancy from liked. Requires authentication."""
    pass


@router.post("/liked_resumes")
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


@router.get("/like_resume/{id}")
def like_resume(id: int, token: str = Depends(oauth2_scheme)):
    """Add a resume to liked. Requires authentication."""
    pass


@router.get("/unlike_resume/{id}")
def unlike_resume(id: int, token: str = Depends(oauth2_scheme)):
    """Remove a resume from liked. Requires authentication."""
    pass


@router.post("/vacancies")
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


@router.get("/vacancy/{id}")
def vacancy(id: int) -> Vacancy:
    """Get a vacancy by ID."""
    return Vacancy(
        id=id,
        external_id="0",
        title="Programmer",
        salary=Salary(type="monthly"),
        employment_types=[]
    )


@router.post("/resumes")
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


@router.get("/resume/{id}")
def resume(id: int) -> Resume:
    """Get a resume by ID."""
    return Resume(
        id=id,
        external_id="0",
        title="Programmer",
        salary=Salary(type="monthly")
    )
