import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

DATA_FILE = Path("courses.json")


class Course(BaseModel):
    course_name: str = Field(..., min_length=1)
    year: str = Field(..., min_length=4, max_length=4)
    semester: str = Field(..., min_length=1)
    grade: str = Field(..., min_length=1)


def read_courses():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="JSON 파일 형식이 올바르지 않습니다.")


def write_courses(courses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)


@app.get("/")
def root():
    return {"message": "Course Record API"}


@app.get("/courses")
def get_courses():
    courses = read_courses()
    return courses


@app.post("/courses")
def add_course(course: Course):
    courses = read_courses()

    new_course = course.model_dump()
    courses.append(new_course)

    write_courses(courses)

    return {
        "message": "수강기록이 추가되었습니다.",
        "course": new_course
    }
    