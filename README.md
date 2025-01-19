# Application Setup

## Follow these steps to get the application up and running:

### 1. Install Docker & SQLite
- Download and install Docker on your system: [Docker - Homepage](https://www.docker.com/).
- Download and install SQLite on your system: [SQLite - Homepage](https://www.sqlite.org/).

### 2. Create Environment Variables
- Copy the `.env.example` file and rename it to `.env`.
- Fill in the required API keys and secret values in the `.env` file.

### 3. Start the Project
   Run the following command in the project directory to build and start the application:

   ```bash
   cd datenbank-praktikum && docker-compose up -d --build
   ```

### 4. **Running the fixtures**
   Run the following command in your terminal to load the fixtures:

   ```bash
   docker exec -it app python3 -m fixtures
   ```

### 5. **Access the Application**
   Once the project is running, open your browser and navigate to: http://127.0.0.1:8000/

---

# Important commands for development

- **Formulating** your code:
  ```bash
  docker exec -it app python3 -m black .
  ```

---

# Learning Outlines

- **Account Association:** Introducing a dedicated table to map each account to either
  a restaurant or a customer is highly beneficial. This approach ensures each account
  is uniquely tied to one entity, preventing accounts from serving multiple purposes
  and avoiding conflicts.

- **Sorting and Filtering:** Designing robust sorting and filtering mechanisms is
  complex and must be approached with care to minimize errors. Implementing a caching
  layer over the database can significantly optimize performance and support these
  operations.

- **Componentization:** Splitting the application into smaller, manageable components
  and services is a challenging task that demands thoughtful decision-making over time.
  Mistakes are inevitable, so regular refactoring sessions are essential to maintain
  a clean and consistent codebase.

- **Error Handling:** Building an efficient and effective error-handling system is
  critical for application uptime. A well-designed system ensures that if one component
  or page fails, other features and components continue functioning seamlessly.

---

# Credits

This project was created by:

- **Mohamad Ali Jawad**
- **Pola Eskandar**
