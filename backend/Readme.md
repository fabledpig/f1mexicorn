**Setup and run the f1 mexicorn backend application**
- pip install -r requirements.txt
- Go into /backend folder and `uvicorn app.main:app --reload`

**DB setup**
mysql -u <username> -p < path/to/schema.sql