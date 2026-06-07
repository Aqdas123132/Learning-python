from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import models, crud, schemas
from database import engine, get_db
from groq import Groq
from pydantic import BaseModel
import json

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates")
groq_client = Groq(api_key="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")

def seed_data(db: Session):
    if db.query(models.Student).count() == 0:
        students = [
            {"name":"Ali Hassan","email":"CS Group","department":"Grade 9","marks":84.7,"status":"Pass","description":'{"English":78,"Urdu":82,"Islamiat":90,"Pakistan Studies":85,"Tarjuma-tul-Quran":88,"Computer Science":91,"Chemistry":79,"Physics":83,"Mathematics":86}'},
            {"name":"Sara Khan","email":"General","department":"Grade 7","marks":35.2,"status":"Fail","description":'{"English":35,"Urdu":38,"Mathematics":30,"Science":32,"Islamiat":40,"Pakistan Studies":36}'},
            {"name":"Ayesha Malik","email":"Biology Group","department":"Grade 10","marks":91.0,"status":"Topper","description":'{"English":92,"Urdu":88,"Islamiat":95,"Pakistan Studies":91,"Tarjuma-tul-Quran":93,"Biology":94,"Chemistry":89,"Physics":87,"Mathematics":90}'},
            {"name":"Ahmed Raza","email":"General","department":"Grade 8","marks":70.2,"status":"Pass","description":'{"English":65,"Urdu":70,"Mathematics":72,"Science":68,"Islamiat":75,"Pakistan Studies":71}'},
            {"name":"Nimra Baig","email":"General","department":"Grade 6","marks":29.8,"status":"Fail","description":'{"English":28,"Urdu":32,"Mathematics":25,"Science":30,"Islamiat":35,"Pakistan Studies":29}'},
        ]
        for s in students:
            db.add(models.Student(**s))
        db.commit()

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    seed_data(db)
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/students/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db=db, student=student)

@app.get("/students/", response_model=list[schemas.StudentResponse])
def read_students(db: Session = Depends(get_db)):
    return crud.get_all_students(db=db)

@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    s = crud.get_student(db=db, student_id=student_id)
    if not s:
        raise HTTPException(status_code=404, detail="Student not found")
    return s

@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    updated = crud.update_student(db=db, student_id=student_id, student=student)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_student(db=db, student_id=student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

class ChatRequest(BaseModel):
    message: str

@app.post("/chat/")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    students = crud.get_all_students(db)
    if not students:
        return {"reply": "No students found in the database."}

    def get_status(marks):
        if marks >= 80: return "Topper"
        if marks >= 60: return "Average"
        if marks >= 40: return "Pass"
        return "Fail"

    def get_grade(marks):
        if marks >= 80: return "A+"
        if marks >= 70: return "A"
        if marks >= 60: return "B"
        if marks >= 50: return "C"
        if marks >= 40: return "D"
        return "F"

    student_details = []
    for s in students:
        try:
            subject_marks = json.loads(s.description) if s.description else {}
        except:
            subject_marks = {}
        subjects_str = ", ".join([f"{k}:{v}" for k, v in subject_marks.items()]) if subject_marks else "Not provided"
        student_details.append({
            "id": s.id,
            "name": s.name,
            "class": s.department,
            "group": s.email,
            "percentage": s.marks,
            "grade": get_grade(s.marks),
            "status": get_status(s.marks),
            "subjects": subjects_str
        })

    ranked = sorted(student_details, key=lambda x: x["percentage"], reverse=True)
    top = ranked[0]
    bottom = ranked[-1]
    total = len(student_details)
    passing = [s for s in student_details if s["percentage"] >= 40]
    failing = [s for s in student_details if s["percentage"] < 40]
    toppers = [s for s in student_details if s["percentage"] >= 80]
    avg = sum(s["percentage"] for s in student_details) / total

    classes = {}
    for s in student_details:
        c = s["class"]
        if c not in classes:
            classes[c] = []
        classes[c].append(s)

    class_summary = "\n".join([
        f"  {cls}: {len(studs)} students | Avg: {sum(x['percentage'] for x in studs)/len(studs):.1f}% | Top: {max(studs, key=lambda x: x['percentage'])['name']} | Failing: {len([x for x in studs if x['percentage'] < 40])}"
        for cls, studs in sorted(classes.items())
    ])

    ranked_list = "\n".join([
        f"  Rank {i+1}. {s['name']} | Class:{s['class']} | Group:{s['group']} | {s['percentage']}% | Grade:{s['grade']} | {s['status']} | Subjects:[{s['subjects']}]"
        for i, s in enumerate(ranked)
    ])

    prompt = f"""You are EduTrack school AI assistant with REAL-TIME database access.

STATS: Total:{total} | Passing:{len(passing)} | Failing:{len(failing)} | Avg:{avg:.1f}%
Top: {top['name']} {top['percentage']}% | Lowest: {bottom['name']} {bottom['percentage']}%

ALL STUDENTS:
{ranked_list}

CLASS BREAKDOWN:
{class_summary}

Question: {req.message}

Rules: Answer from data only. Give full details for any student mentioned. English only. Be accurate."""

    response = groq_client.chat.completions.create(
      model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"reply": response.choices[0].message.content}