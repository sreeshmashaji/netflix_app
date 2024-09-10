

cd Back

py -m venv movie-venv


movie-venv\Scripts\activate.bat



pip install  -r requirements.txt


uvicorn main:app --reload

