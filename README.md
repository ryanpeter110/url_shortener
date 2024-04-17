# URL Shortener API

## Overview

The **URL Shortener API** provides endpoints to shorten URLs and redirect to the original URLs using short keys.

## Installation

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/ryanpeter110/url_shortener.git
    cd url-shortener
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Start the FastAPI application:
    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000
    ```


## Endpoints

### 1. Shorten URL

Shortens a given URL and optionally allows custom shortening.

- **URL**: `/shorten_url`
- **Method**: `POST`

#### Parameters

- **Headers**
  - `x-custom-shorten`: Flag to indicate custom shortening (Default: `false`)

#### Request Body

The request body should be one of the following schemas:

1. **SystemShortenUrlRequest**
    ```json
    {
        "target_url": "string",
        "tags": ["string", null],
        "short_key_length": "integer"
    }
    ```

2. **CustomShortenUrlRequest**
    ```json
    {
        "target_url": "string",
        "tags": ["string", null],
        "custom_key": "string"
    }
    ```

#### Responses


- **200 OK / 201 Created**
    ```json
    {
        "meta": {
            "successful": true,
            "request_id": "UUID",
            "message": "string",
            "create_date": "datetime"
        },
        "data": {
            "mapping_id": "string",
            "target_url": "string",
            "short_key": "string",
            "hits": "integer",
            "is_active": "boolean",
            "is_custom_key": "boolean",
            "tags": ["string"],
            "app_version": "string"
        }
    }
    ```
    - **Note**: You'll get `200 OK` if the target URL already exists and `201 Created` if a new mapping is created for the first time.


- **400 Bad Request**
    ```json
    {
        "meta": {
            "successful": false,
            "request_id": "UUID",
            "message": "string",
            "create_date": "datetime"
        },
        "data": null
    }
    ```
    - **Note**: Returned when `x-custom-shorten` is `true` and the `short_key` exists in database.


- **422 Unprocessable Entity**
    ```json
    {
        "meta": {
            "successful": false,
            "request_id": "UUID",
            "message": "string",
            "create_date": "datetime"
        },
        "data": List[Dict]
    }
    ```
    - **Note**: Returned in case of validation errors.


### 2. Redirect To Target URL

Redirects to the original URL associated with a given short key.

- **URL**: `/{short_key}`
- **Method**: `GET`

#### Parameters

- **Path**
  - `short_key`: The short key to look up in the database.

#### Responses

- **200 OK**
  - Successful redirection to the target URL.

- **422 Unprocessable Entity**
    ```json
    {
        "meta": {
            "successful": false,
            "request_id": "UUID",
            "message": "string",
            "create_date": "datetime"
        },
        "data": List[Dict]
    }
    ```
    - **Note**: Returned in case of validation errors.
