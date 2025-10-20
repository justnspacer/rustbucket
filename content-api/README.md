# content-api/content-api/README.md

# Content API

## Overview

Content API is a backend application built with FastAPI that provides a RESTful API for managing posts. It allows users to create, update, delete, and search for posts. The application interacts with a Supabase database to store and retrieve post data.

## Features

- Create, update, and delete posts
- Search for posts based on various criteria
- User authentication and authorization (to be implemented)
- Easy integration with frontend applications

## Project Structure

```
content-api
├── app
│   ├── __init__.py          # Initializes the app package
│   ├── main.py              # Entry point of the application
│   ├── api                  # Contains API routes
│   │   ├── __init__.py
│   │   └── routes           # API route definitions
│   │       ├── __init__.py
│   │       ├── posts.py     # Endpoints for managing posts
│   │       └── search.py    # Endpoints for searching posts
│   ├── models               # Database models
│   │   ├── __init__.py
│   │   └── post.py          # Post model definition
│   ├── services             # Business logic and services
│   │   ├── __init__.py
│   │   └── supabase_service.py # Interactions with Supabase
│   └── schemas              # Pydantic schemas for validation
│       ├── __init__.py
│       └── post_schema.py    # Schemas for post data
├── requirements.txt          # Python dependencies
├── .env.example              # Example environment variables
└── README.md                 # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd  content-api
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables by copying `.env.example` to `.env` and updating the values as needed.

## Usage

To run the application, execute the following command:

```
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

- **Posts**
  - `POST /posts` - Create a new post
  - `GET /posts` - Retrieve all posts
  - `GET /posts/{id}` - Retrieve a specific post
  - `PUT /posts/{id}` - Update a specific post
  - `DELETE /posts/{id}` - Delete a specific post

- **Search**
  - `GET /search` - Search for posts based on query parameters

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.