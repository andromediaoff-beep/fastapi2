from fastapi import FastAPI, Form, HTTPException
from fastapi import File, UploadFile
from models.models import Movietop
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
import os

import json

#uvicorn main:app --reload --port 8165

image = "C:/Users/Student/Desktop/FastApi8165/bgitu2.png"

app = FastAPI()

movie1 = Movietop(**{
    "name": "Deadpool",
    "id": 1,
    "cost": 202,
    "director": "JS",
    "watched" : True
})

movie2 = Movietop(**{
    "name": "Spider Man",
    "id": 2,
    "cost": 422,
    "director": "DK",
    "watched" : True
})

movie3 = Movietop(**{
    "name": "Formula 1",
    "id": 3,
    "cost": 600,
    "director": "IO",
    "watched" : True
})

movie4 = Movietop(**{
    "name": "Breaking Bad",
    "id": 4,
    "cost": 700,
    "director": "CC",
    "watched" : True
})

movies_dict = {
    "movie1": movie1,
    "movie2": movie2,
    "movie3": movie3,
    "movie4": movie4
}

movie_count = len(movies_dict) + 1

@app.get("/study", response_class=HTMLResponse)
async def get_university():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI HTML Response</title>
    </head>
    <body>
        <h1>БГИТУ</h1>
        <img src="/image"> 
    </body>
    </html>
    """
    return HTMLResponse(html_content)


@app.get("/movietop")
async def get_movietop():
    return movies_dict;

@app.get("/image")
async def get_image():
    return FileResponse(image);

@app.get("/movietop/{movie_id}")
async def get_movie_by_id(movie_id: int):
    for key, value in movies_dict.items():
        if value.id == movie_id:
            return {
                "name": value.name,
                "id": value.id,
                "cost": value.cost,
                "director": value.director,
                "watched" : value.watched
            }
    raise HTTPException(status_code=424, detail="Error, this movie doesn't exist")


@app.get("/movieform/")
async def show_movie_form():
    return FileResponse("templayts/movie_form.html")

@app.post("/movieform/")
async def formfilm(
    name: str = Form(...),
    id: int = Form(...),
    cost: int = Form(...),
    director: str = Form(...),
    watched: bool = Form(False)
):
    global movie_count

    for key, movie in movies_dict.items():
        if movie.id == id:
            raise HTTPException(
                status_code=560,
                detail="Ошибка, фильм с данным id уже существует"
            )

    movie = Movietop(
        name=name,
        id=id,
        cost=cost,
        director=director,
        watched=watched
    )
    movie_key = f"movie{movie_count}"
    movies_dict[movie_key] = movie
    movie_count += 1

    return {
        "movie_key" : movie_key,
        "name": movie.name,
        "id": movie.id,
        "cost": movie.cost,
        "director": movie.director,
        "watched": movie.watched
    }