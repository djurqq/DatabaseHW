# DatabaseHW

Setup Instructions

1. Clone the Github Repository using Github Desktop
2. Create a database on MongoDB
3. Create a virtual environment via VS Code terminal
   python -m venv env
   env\Scripts\activate (on Windows)
4. Set the ExecutionPolicy to RemoteSigned
5. Install the necessary dependencies:
   pip install fastapi
   pip install uvicorn
   pip install motor
   pip install pydantic
   pip install python-dotenv
   pip install requests
   pip install python-multipart
7. Generate a requirements.txt file using:
   pip freeze > requirements.txt
8. Finally run the FastAPI by either running the program in VS Code or using the following command:
   uvicorn main:app --reload
