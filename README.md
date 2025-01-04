# Temporary URL Shortener

This is an API project to generate temporary shortened URLs, which expire after 24 hours. The service allows shortening long URLs and redirecting them to their original versions while they are active.

## Features

- **Shortened URL generation**: Provides a short URL that redirects to a long URL.
- **Automatic expiration**: The shortened URLs are automatically deleted after 24 hours.
- **Simple API**: The API is built with FastAPI and MongoDB for temporary storage.

## Technologies

- **FastAPI**: A fast and modern web framework to build APIs with Python.
- **MongoDB**: A NoSQL database to store temporary URLs.
- **Uvicorn**: ASGI server to run the FastAPI application.
- **Pydantic**: Data validation and schema modeling.
- **Dotenv**: Environment variable management.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/DanielaGz/url_shortener.git
   cd url_shortener
