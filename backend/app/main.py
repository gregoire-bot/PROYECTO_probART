
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import BodyProfile, Clothing
from .schemas import BodyProfileCreate, BodyProfileResponse
from pydantic import BaseModel

# ============================================================
# DATABASE
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="VirtualFit API",
    description="Sistema de probador virtual de ropa",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# FRONTEND
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)

MODELS_DIR = BASE_DIR / "models"

app.mount(
    "/models",
    StaticFiles(directory=MODELS_DIR),
    name="models"
)
@app.get("/", include_in_schema=False)
def home():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


# ============================================================
# ROOT
# ============================================================

@app.get("/api")
def api_root():

    return {
        "project": "VirtualFit",
        "status": "online",
        "version": "1.0.0"
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/api/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# BODY PROFILE
# ============================================================

@app.post(
    "/api/body-profile",
    response_model=BodyProfileResponse
)
def create_body_profile(
    profile: BodyProfileCreate,
    db: Session = Depends(get_db)
):

    new_profile = BodyProfile(
        name=profile.name,
        height=profile.height,
        weight=profile.weight,
        chest=profile.chest,
        waist=profile.waist,
        hip=profile.hip,
        shoulders=profile.shoulders,
        skin_tone=profile.skin_tone
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


# ============================================================
# GET BODY PROFILES
# ============================================================

@app.get("/api/body-profiles")
def get_body_profiles(
    db: Session = Depends(get_db)
):

    profiles = db.query(BodyProfile).all()

    return profiles


# ============================================================
# GET ONE PROFILE
# ============================================================

@app.get("/api/body-profile/{profile_id}")
def get_body_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):

    profile = (
        db.query(BodyProfile)
        .filter(BodyProfile.id == profile_id)
        .first()
    )

    if not profile:

        raise HTTPException(
            status_code=404,
            detail="Perfil no encontrado"
        )

    return profile


# ============================================================
# BMI
# ============================================================

@app.get("/api/body-profile/{profile_id}/bmi")
def calculate_bmi(
    profile_id: int,
    db: Session = Depends(get_db)
):

    profile = (
        db.query(BodyProfile)
        .filter(BodyProfile.id == profile_id)
        .first()
    )

    if not profile:

        raise HTTPException(
            status_code=404,
            detail="Perfil no encontrado"
        )

    height_meters = profile.height / 100

    bmi = profile.weight / (
        height_meters * height_meters
    )

    return {
        "profile_id": profile.id,
        "bmi": round(bmi, 2)
    }


# ============================================================
# CLOTHING
# ============================================================

@app.get("/api/clothing")
def get_clothing(
    db: Session = Depends(get_db)
):

    clothing = db.query(Clothing).all()

    return clothing


# ============================================================
# CREATE CLOTHING
# ============================================================

@app.post("/api/clothing")
def create_clothing(
    name: str,
    category: str,
    brand: str,
    price: float,
    color: str,
    size: str,
    model_path: str = "",
    db: Session = Depends(get_db)
):

    clothing = Clothing(
        name=name,
        category=category,
        brand=brand,
        price=price,
        color=color,
        size=size,
        model_path=model_path
    )

    db.add(clothing)
    db.commit()
    db.refresh(clothing)

    return clothing


# ============================================================
# SIZE RECOMMENDATION
# ============================================================

@app.get("/api/recommend-size/{profile_id}")
def recommend_size(
    profile_id: int,
    db: Session = Depends(get_db)
):

    profile = (
        db.query(BodyProfile)
        .filter(BodyProfile.id == profile_id)
        .first()
    )

    if not profile:

        raise HTTPException(
            status_code=404,
            detail="Perfil no encontrado"
        )

    chest = profile.chest

    if chest < 90:
        size = "S"

    elif chest < 100:
        size = "M"

    elif chest < 110:
        size = "L"

    else:
        size = "XL"

    return {
        "profile_id": profile.id,
        "recommended_size": size,
        "chest": chest
    }
# ============================================================
# GENERAR AVATAR 3D
# ============================================================

import subprocess
import os


# ============================================================
# DATOS DEL AVATAR
# ============================================================

class AvatarRequest(BaseModel):

    genero: str = "male"
    edad: str = "young"

    altura: str = "average"
    peso: str = "averageweight"
    musculo: str = "averagemuscle"
    proporciones: str = "average"

    # Apariencia
    piel: str = "#D9A27F"

    # Identificador de color MPFB
    ojos: str = "brown"

    # Modelo de cabello MPFB
    cabello: str = "short01"

    # Color del cabello
    colorCabello: str = "#3A2418"


# ============================================================
# GENERAR AVATAR
# ============================================================

@app.post("/api/avatar")
def generate_avatar(data: AvatarRequest):

    project_dir = BASE_DIR

    script = (
        project_dir
        / "blender"
        / "create_avatar.py"
    )

    blender = (
        "/opt/blender-4.5.11-linux-x64/blender"
    )

    # --------------------------------------------------------
    # VERIFICAR SCRIPT
    # --------------------------------------------------------

    if not script.exists():

        raise HTTPException(
            status_code=500,
            detail=f"No existe el script: {script}"
        )

    # --------------------------------------------------------
    # VERIFICAR BLENDER
    # --------------------------------------------------------

    if not os.path.exists(blender):

        raise HTTPException(
            status_code=500,
            detail=f"No se encontró Blender: {blender}"
        )

    # --------------------------------------------------------
    # VALORES PERMITIDOS
    # --------------------------------------------------------

    permitidos = {

        "genero": {
            "neutral",
            "male",
            "female"
        },

        "edad": {
            "old",
            "young",
            "child",
            "baby"
        },

        "altura": {
            "minheight",
            "average",
            "maxheight"
        },

        "peso": {
            "minweight",
            "averageweight",
            "maxweight"
        },

        "musculo": {
            "minmuscle",
            "averagemuscle",
            "maxmuscle"
        },

        "proporciones": {
            "min",
            "average",
            "max"
        },

        "ojos": {
            "brown",
            "brownlight",
            "blue",
            "bluegreen",
            "deepblue",
            "green",
            "grey",
            "ice",
            "lightblue"
        },

        "cabello": {
            "short01",
            "short02",
            "short03",
            "short04",
            "bob01",
            "bob02",
            "long01",
            "ponytail01",
            "braid01",
            "afro01"
        }
    }

    # --------------------------------------------------------
    # VALIDAR OPCIONES
    # --------------------------------------------------------

    for campo, valores in permitidos.items():

        valor = getattr(data, campo)

        if valor not in valores:

            raise HTTPException(
                status_code=422,
                detail=(
                    f"Valor inválido para "
                    f"{campo}: {valor}"
                )
            )

    # --------------------------------------------------------
    # MOSTRAR CONFIGURACIÓN
    # --------------------------------------------------------

    print("================================")
    print("GENERANDO AVATAR")
    print("================================")

    print("Parámetros:")
    print(data.model_dump())

    # --------------------------------------------------------
    # COMANDO BLENDER
    # --------------------------------------------------------

    comando = [

        blender,

        "--background",

        "--python",

        str(script),

        "--",

        "--genero",
        data.genero,

        "--edad",
        data.edad,

        "--altura",
        data.altura,

        "--peso",
        data.peso,

        "--musculo",
        data.musculo,

        "--proporciones",
        data.proporciones,

        "--piel",
        data.piel,

        "--ojos",
        data.ojos,

        "--cabello",
        data.cabello,

        "--colorCabello",
        data.colorCabello
    ]

    # --------------------------------------------------------
    # EJECUTAR BLENDER
    # --------------------------------------------------------

    try:

        result = subprocess.run(

            comando,

            cwd=str(project_dir),

            capture_output=True,

            text=True,

            timeout=120
        )

        # ----------------------------------------------------
        # MOSTRAR LOG
        # ----------------------------------------------------

        print("------ BLENDER STDOUT ------")
        print(result.stdout)

        print("------ BLENDER STDERR ------")
        print(result.stderr)

        # ----------------------------------------------------
        # ERROR DE BLENDER
        # ----------------------------------------------------

        if result.returncode != 0:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Blender no pudo generar "
                    "el avatar"
                )
            )

        # ----------------------------------------------------
        # VERIFICAR GLB
        # ----------------------------------------------------

        avatar_path = (

            project_dir
            / "models"
            / "avatars"
            / "avatar.glb"
        )

        if not avatar_path.exists():

            raise HTTPException(
                status_code=500,
                detail=(
                    "Blender terminó pero "
                    "no creó avatar.glb"
                )
            )

        # ----------------------------------------------------
        # RESPUESTA
        # ----------------------------------------------------

        return {

            "success": True,

            "message":
                "Avatar creado correctamente",

            "avatar_url":
                "/models/avatars/avatar.glb"
        }

    except subprocess.TimeoutExpired:

        raise HTTPException(
            status_code=500,
            detail=(
                "Blender tardó demasiado "
                "en generar el avatar"
            )
        )

    except HTTPException:

        raise

    except Exception as error:

        print(
            "Error generando avatar:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
