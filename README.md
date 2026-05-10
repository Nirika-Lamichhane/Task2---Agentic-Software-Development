# To run this project code

1. Make the python virutal environment and activate it as : 
python -m venv name
.\venv\Scripts\activate

2. Install the dependencies from the requirements.txt
pip install -r requirements.txt

3. Open the docker app and run this code in terminal as:
docker-compose up -d

4. Finally do:
uvicorn main:app --reload

## You have to create your own .env file in the format as:
POSTGRES_USER=username
POSTGRES_PASSWORD=Your_password
POSTGRES_DB=DB_name
POSTGRES_PORT=port_number

