from datetime import datetime, timezone
from enum import Enum

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema


description = """
API немного отличается от спецификации, а код немного отличается от изначального шаблона, так как: 
- некоторые вещи не описаны в спецификации;
- некоторые вещи не логичны. Например, при создании `Dog` не нужно прокидывать `pk`.
"""

app = FastAPI(
    title="MVP ДЗ3 Дадыков Артемий",
    description=description,
)


# ====================== Ping ======================


class RootResponse(BaseModel):
    message: str = "ping"


@app.get("/", tags=["Root"])
def root() -> RootResponse:
    return RootResponse()


# ====================== Posts ======================


class Timestamp(BaseModel):
    id: int
    timestamp: int


POSTS_DB = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10),
]


@app.post("/post", tags=["Post"])
def post() -> Timestamp:
    max_id = max(post.id for post in POSTS_DB)
    timestamp = round(datetime.now(tz=timezone.utc).timestamp())
    new_timestamp = Timestamp(
        id=max_id + 1,
        timestamp=timestamp,
    )
    return new_timestamp


# ====================== Dogs ======================


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class DogCreate(Dog):
    pk: SkipJsonSchema[int] = Field(default=-1, exclude=True)


class DogUpdate(Dog):
    pk: SkipJsonSchema[int] = Field(default=-1, exclude=True)


DOGS_DB = {
    0: Dog(name="Bob", pk=0, kind="terrier"),
    1: Dog(name="Marli", pk=1, kind="bulldog"),
    2: Dog(name="Snoopy", pk=2, kind="dalmatian"),
    3: Dog(name="Rex", pk=3, kind="dalmatian"),
    4: Dog(name="Pongo", pk=4, kind="dalmatian"),
    5: Dog(name="Tillman", pk=5, kind="bulldog"),
    6: Dog(name="Uga", pk=6, kind="bulldog"),
}


def generate_dog_pk() -> int:
    return max(DOGS_DB.keys()) + 1


@app.get("/dog", tags=["Dog"])
def read_dogs(
    kind: DogType | None = None,
) -> list[Dog]:
    dogs = DOGS_DB.values()
    if kind is not None:
        dogs = [dog for dog in dogs if dog.kind == kind]
    return dogs


@app.get("/dog/{pk}", tags=["Dog"])
def read_dog(
    pk: int,
) -> Dog:
    dog: Dog | None = DOGS_DB.get(pk, None)
    if dog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dog not found",
        )
    return dog


@app.post("/dog", tags=["Dog"])
def create_dog(
    dog_create: DogCreate,
) -> Dog:
    created_dog = Dog(
        pk=generate_dog_pk(),
        **dog_create.model_dump(),
    )
    DOGS_DB[created_dog.pk] = created_dog
    return created_dog


@app.patch("/dog/{pk}", tags=["Dog"])
def update_dog(
    pk: int,
    dog_update: DogUpdate,
) -> Dog:
    read_dog(pk=pk)  # Check dog existence.
    updated_dog = Dog(
        pk=pk,
        **dog_update.model_dump(),
    )
    DOGS_DB[updated_dog.pk] = updated_dog
    return updated_dog
