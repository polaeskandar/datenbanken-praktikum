# Application Setup

Follow these steps to boot up the application:

1. **Install Docker**  
   Download and install Docker on your system: [Docker - Homepage](https://www.docker.com/).
   Download and install SQLite on your system: [SQLite - Homepage](https://www.sqlite.org/).

2. **Start the Project**  
   Run the following command in the project directory:
   ```bash
   cd datenbank-praktikum && docker-compose up -d --build
   ``` 

3. **Import the sample data**
   Run the following command to run the SQL scripts in data.sql:
   ```bash
   sqlite3 instance/restaurant.db < data.sql
   ```

4. Access the Application
   Once the project is running, open your browser and navigate to:
   http://127.0.0.1:8000/

# Important commands for development

- **Formulating** your code:
   ```bash 
   docker exec -it app python3 -m black .
   ```

---

# Learning Outlines

- It is beneficial to introduce a new table that maps each account to either a restaurant or a customer. This ensures
  that each account is uniquely associated with one entity, preventing any account from being used for multiple
  purposes.

---

# Credits

This project was created by:

- **Mohamed Jawad**
- **Chuan Tian**
- **Pola Eskandar**
