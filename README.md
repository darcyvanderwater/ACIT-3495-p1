# Project Overview

This project is a small microservice-based web application built using Docker Compose.
The system collects simple numeric measurements, processes them to generate summary
statistics, and displays the results through a small web interface.

The application is made up of four services:

1. **enter-data**  
   A small Flask application used to enter measurements into a MySQL database.

2. **analytics-service**  
   A Python service that reads data from MySQL, computes summary statistics (count, min,
   max, average), and stores the summarized result in MongoDB.

3. **show-results**  
   A Node.js application that displays the most recent analytics result, with an option
   to trigger the analytics process manually.

4. **auth-service**  
   A simple authentication service that validates usernames and passwords before
   allowing other services to perform protected actions.

Two databases are used:

- **MySQL** for raw measurement data  
- **MongoDB** for saving analytics summaries

---

## How to Run the System

Make sure Docker and Docker Compose are installed.

1. Place all project files in a folder  
2. Open a terminal or PowerShell in that folder  
3. Run:

```
docker compose up --build
```

This will start all services and databases.

Once everything is running, the system can be accessed through the following URLs:

- **Enter Data:**  
  http://localhost:5000/

- **Show Results Page:**  
  http://localhost:5001/

- **Analytics Service (direct access):**  
  http://localhost:5003/run-once  
  (POST only — Also a link on the results page)

---

## Credentials

Two users were used for testing:

| Username | Password |
|----------|----------|
| darcy    | weakpass |
| darcy2   | weakpass |

These are authenticated through the **auth-service**. when 

---

## How It All Works!

### 1. Entering Data  
The user visits the **enter-data page**, then enters their credentials, along with the label and value for the data they want to provide.
This information is saved into the MySQL database.

### 2. Running Analytics  
The analytics service reads all measurements from MySQL and calculates:

- How many values were entered  
- The smallest value  
- The largest value  
- The average value  

It stores this summary in MongoDB as a single document.

Analytics can be triggered in two ways:

- By clicking “Compute Analytics Now” on the results page. This makes a POST request to `/run-once` on the analytics-service

### 3. Viewing Results  
The **show-results** service retrieves the most recent analytics entry from MongoDB and
displays it to the user. Authentication is required before results can be viewed.

---

## Service Ports

These are the ports used by the services.

| Service           | Port on Host | Description            |
|-------------------|--------------|------------------------|
| enter-data        | 5000         | Data entry UI          |
| show-results      | 5001         | Results UI             |
| auth-service      | 5002         | Authentication API     |
| analytics-service | 5003         | Analytics API          |
| MySQL             | 3306         | Raw data storage       |
| MongoDB           | 27017        | Analytics storage      |

---

## Folder Structure

This shows the layout of our files and folders

```
.
├── docker-compose.yml
├── auth-service/
│   ├── app.py
│   └── Dockerfile
├── enter-data/
│   ├── app.py
│   └── Dockerfile
├── analytics-service/
│   ├── app.py
│   └── Dockerfile
└── show-results/
    ├── server.js
    ├── package.json
    └── Dockerfile
```

---

## Next Steps

While functioning, the application of pretty basic. Here are the next steps that could be taken to improve it further.

- Make it pretty (very limited CSS currently)
- Use templates rather than returning HTML
- Allow deleting or updating measurements (currently can only see)  
- Improve navigation UI  

---

