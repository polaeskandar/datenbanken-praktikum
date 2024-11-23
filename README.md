# Application Setup

Follow these steps to boot up the application:

1. **Install Docker**  
   Download and install Docker on your system: [Docker - Hompage](https://www.docker.com/).

2. **Start the Project**  
   Run the following command in the project directory:  
   ```bash
   docker-compose up -d --build
   ``` 

3. Access the Application 
Once the project is running, open your browser and navigate to:
http://127.0.0.1:8000/

# Important commands for development

- **Formulating** your code: 
   ```bash 
   docker exec -it app python3 -m black .
   ```

---

# Credits
This project was created by:

- **Nader Salib**
- **Mohamed Jawad**
- **Chuan Tian**
- **Pola Eskandar**
