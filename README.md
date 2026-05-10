# FastAPI CRUD API

## What is this project?
This is a simple API that lets you create, read, update, 
and delete items using FastAPI and SQLite database.

## How to Run this Project

First, install the required packages:
pip install fastapi uvicorn sqlalchemy

Then, run the server:
uvicorn main:app --reload

Open your browser and go to:
http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | What it does |
|--------|----------|--------------|
| POST | /items/ | Add a new item |
| GET | /items/ | See all items |
| GET | /items/{id} | See one item |
| PUT | /items/{id} | Update an item |
| DELETE | /items/{id} | Remove an item |

## Project Files

- main.py — starts the API
- database.py — connects to database
- models.py — defines the table
- schemas.py — checks the data
- crud.py — does the actual work
- database.db — stores the data