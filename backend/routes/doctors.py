from fastapi import APIRouter, Query
from models import DoctorsResponse, DoctorModel

router = APIRouter()

_ALL_DOCTORS: list[DoctorModel] = [
    DoctorModel(name="Dr. Aisha Patel",    spec="Cardiologist",       rating=4.9, avail="Today",     init="AP"),
    DoctorModel(name="Dr. Rajesh Kumar",   spec="General Physician",  rating=4.7, avail="Today",     init="RK"),
    DoctorModel(name="Dr. Priya Singh",    spec="Neurologist",        rating=4.8, avail="Tomorrow",  init="PS"),
    DoctorModel(name="Dr. Arjun Mehta",    spec="Pulmonologist",      rating=4.6, avail="Today",     init="AM"),
    DoctorModel(name="Dr. Sneha Rao",      spec="Gastroenterologist", rating=4.8, avail="In 2 days", init="SR"),
    DoctorModel(name="Dr. Vikram Nair",    spec="Orthopedist",        rating=4.7, avail="Today",     init="VN"),
    DoctorModel(name="Dr. Kavya Sharma",   spec="Dermatologist",      rating=4.9, avail="Tomorrow",  init="KS"),
    DoctorModel(name="Dr. Anand Gupta",    spec="ENT Specialist",     rating=4.5, avail="Today",     init="AG"),
    DoctorModel(name="Dr. Meena Joshi",    spec="Gynecologist",       rating=4.8, avail="Tomorrow",  init="MJ"),
    DoctorModel(name="Dr. Suresh Iyer",    spec="Endocrinologist",    rating=4.6, avail="In 2 days", init="SI"),
    DoctorModel(name="Dr. Divya Krishnan", spec="Psychiatrist",       rating=4.7, avail="Today",     init="DK"),
    DoctorModel(name="Dr. Rahul Verma",    spec="Urologist",          rating=4.5, avail="Tomorrow",  init="RV"),
]


@router.get("/doctors", response_model=DoctorsResponse)
async def get_doctors(specialty: str = Query(default="", description="Specialty filter keyword")):
    """
    Return up to 3 doctors matching the specialty keyword.
    Falls back to General Physician if no match found.
    """
    kw = specialty.lower().strip()

    if kw:
        matched = [
            d for d in _ALL_DOCTORS
            if kw in d.spec.lower() or d.spec.lower().split()[0] in kw
        ]
        if not matched:
            matched = [d for d in _ALL_DOCTORS if d.spec == "General Physician"]
    else:
        matched = list(_ALL_DOCTORS)

    return DoctorsResponse(specialty=specialty, doctors=matched[:3])
