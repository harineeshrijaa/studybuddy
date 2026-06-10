from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "StudyBuddy is running!"}

@app.get("/note")
def get_notes():
    with open("data/aws.txt", "r") as file:
        content = file.read()
    return {"note": content}

