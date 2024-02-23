## Post Management System
The Post Management System is a web application developed to facilitate the management of posts with CRUD (Create, Read, Update, Delete) operations. It leverages the FastAPI framework for backend development, SQLAlchemy for efficient database management, and OAuth2 for secure user authentication. The system ensures robust authorization mechanisms to maintain data integrity and security, allowing only authorized users to modify their respective posts.
 
### Features
* CRUD Operations: Users can create, read, update, and delete posts through the intuitive interface provided by the system.
* Secure Authentication: OAuth2 is implemented to ensure secure user authentication, preventing unauthorized access to sensitive data.
* Authorization Mechanisms: Robust authorization mechanisms are in place to guarantee that only authorized users can modify their own posts, enhancing data integrity and security.
* Efficient Database Management: SQLAlchemy is utilized for efficient management of the PostgreSQL database, ensuring optimal performance and scalability.
* API Documentation: FastAPI's automatic API documentation feature provides comprehensive documentation for easy understanding and integration.

● Technologies utilized: FastAPI, PostgreSQL, Pydantic, OAuth2, SQLAlchemy, jose (JWT), Postman.

### Getting Started
1. Clone the repository to your local machine.
```
git clone https://github.com/akshaypatel774/Post-Management-System.git
```
2. Install the required dependencies.
```
pip install -r requirements.txt
```
3. Set up a PostgreSQL database and update the database connection settings in the configuration file. (Create `.env` file with all the required variables from `config.py`)
4. Run the application.
```
uvicorn main:app --reload
```
5. Access the API documentation and explore the features.