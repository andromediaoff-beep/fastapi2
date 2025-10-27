from fastapi import FastAPI, Form, HTTPException
from fastapi import File, UploadFile
from models.models import Movietop
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pathlib import Path
import os

import json

#uvicorn main:app --reload --port 8165

image = "C:/Users/Student/Desktop/FastApi8165/bgitu2.png"
film_img_path = "/film_files/"

app = FastAPI()
app.mount("/film_files", StaticFiles(directory=film_img_path), name="film_files")


movie1 = Movietop(**{
    "name": "Deadpool",
    "id": 1,
    "cost": 202,
    "director": "JS",
    "watched" : True,
    "file_path" : "film_files/movie1_Deadpool.jpg"
})

movie2 = Movietop(**{
    "name": "Spider Man",
    "id": 2,
    "cost": 422,
    "director": "DK",
    "watched" : True,
    "file_path" : "film_files/movie1_Deadpool.jpg"
})

movie3 = Movietop(**{
    "name": "Formula 1",
    "id": 3,
    "cost": 600,
    "director": "IO",
    "watched" : True,
    "file_path" : "film_files/movie1_Deadpool.jpg"
})

movie4 = Movietop(**{
    "name": "Breaking Bad",
    "id": 4,
    "cost": 700,
    "director": "CC",
    "watched" : True,
    "file_path" : "film_files/movie1_Deadpool.jpg"
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

@app.get("/movietop/{movie_id}",  response_class=HTMLResponse)
async def get_movie_by_id(movie_id: int):
    for key, value in movies_dict.items():
        if value.id == movie_id:
            return f"""
                        <html>
                        <head><title>{value.name}</title></head>
                        <body style="font-family: Arial; margin: 20px;">
                            <h1>Информация о фильме</h1>
                            <p><b>Название:</b> {value.name}</p>
                            <p><b>ID:</b> {value.id}</p>
                            <p><b>Стоимость:</b> {value.cost}</p>
                            <p><b>Режиссёр:</b> {value.director}</p>
                            <p><b>Просмотрен:</b> {"Да" if value.watched else "Нет"}</p>
                            <p><b>Файл:</b></p>
                            <img src="/{value.file_path}" alt="{value.name}" style="max-width:300px;">
                        </body>
                        </html>
                        """
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
    watched: bool = Form(...),
    file: UploadFile = File(...)
):

    global movie_count

    for key, movie in movies_dict.items():
        if movie.id == id:
            raise HTTPException(
                status_code=560,
                detail="Ошибка, фильм с данным id уже существует"
            )

    filename = f'movie_{movie_count}_{file.filename}'
    file_save = os.path.join(film_img_path, filename)

    with open(file_save, "wb") as f:
        content = await file.read()
        f.write(content)

    movie = Movietop(
        name=name,
        id=id,
        cost=cost,
        director=director,
        watched=watched,
        file_path=file_save
    )

    movie_key = f"movie{movie_count}"
    movies_dict[movie_key] = movie
    movie_count += 1

    return movie
