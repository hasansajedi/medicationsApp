# Medication APP Documentation
Welcome to the Medication API documentation. This API provides endpoints for managing medication-related data.

# Build and Deployment 

## Start containers

Installing and deploying in a Docker containers is a straightforward process.
The API comes with default configurations, which are listed here:

| Name                       | App name | Default Value                                                                                                                      |
|----------------------------|----------|------------------------------------------------------------------------------------------------------------------------------------|
| TITLE                      | Backend  | Medications API                                                                                                                    |
| ENABLE_DOCUMENTATION       | Backend  | `True`                                                                                                                             |
| DEBUG                      | Backend  | `True`                                                                                                                             |
| BACKEND_PORT               | Backend  | `8005`                                                                                                                             |
| DATA_PATH                  | Backend  | `data/dataset.json`                                                                                                                |
| SHRED_ACCESS_KEY           | Backend  | `rRoFT3H6mzMrUW7XuaOGz7VEaFt42QZy8LVLeBCZBEHskm983gmMfb7nJUwmZr2I5NwzyaVSE8DeMeDB8mgmRIwVMuyGPYAOINbUlAFlPNcTUzodQ5VCFpRNNtMJjn4x` |
| FRONTEND_APP_PORT          | Frontend | `8006`                                                                                                                             |
| REACT_APP_BACKEND_URL      | Frontend | `http://127.0.0.1:8005/`                                                                                                           |
| REACT_APP_SHRED_ACCESS_KEY | Frontend | `rRoFT3H6mzMrUW7XuaOGz7VEaFt42QZy8LVLeBCZBEHskm983gmMfb7nJUwmZr2I5NwzyaVSE8DeMeDB8mgmRIwVMuyGPYAOINbUlAFlPNcTUzodQ5VCFpRNNtMJjn4x` |


```shell
cd medications
docker-compose up -d --build
```

then you have to wait to installing requirements and deploying api and frontend. Once process finished, you will see following result in output:
```shell
.
.
.
✔ Container medicationApi       Started                                                                                                                                                                                       3.7s 
✔ Container medicationFrontend  Started      
```
to see which services already created, use:
```shell
> docker-compose ps

# result
|NAME                |IMAGE                           |COMMAND                  |SERVICE               |CREATED             |STATUS              | PORTS                                               |                    
|--------------------|--------------------------------|-------------------------|----------------------|--------------------|--------------------|-----------------------------------------------------|
|medicationApi       |medications-medication_api      | "uvicorn --host 0.0.…"   | medication_api      | 20 minutes ago     | Up 20 minutes      | 0.0.0.0:8005->8005/tcp, :::8005->8005/tcp           |
|medicationFrontend  |medications-medication_frontend | "docker-entrypoint.s…"   | medication_frontend | 20 minutes ago     | Up 20 minutes      | 8006/tcp, 0.0.0.0:8006->3000/tcp, :::8006->3000/tcp |

```
to make sure api is started and ready to use, use:
```shell
> docker-compose logs medication_api

# result
medicationApi  | INFO:     Started server process [1]
medicationApi  | INFO:     Waiting for application startup.
medicationApi  | INFO:     Application startup complete.
medicationApi  | INFO:     Uvicorn running on http://0.0.0.0:8005 (Press CTRL+C to quit)
```

to make sure frontend app is started and ready to use, use:
```shell
> docker-compose logs medication_frontend

# result
medicationFrontend  | You can now view frontend in the browser.
medicationFrontend  | 
medicationFrontend  |   Local:            http://localhost:3000
medicationFrontend  |   On Your Network:  http://172.23.0.3:3000
medicationFrontend  | 
medicationFrontend  | Note that the development build is not optimized.
medicationFrontend  | To create a production build, use npm run build.
medicationFrontend  | 
medicationFrontend  | webpack compiled successfully
```

## Backend API

The Api is accessible at http://localhost:8005/docs.

### Run tests of API

```shell
docker-compose run medication_api pytest tests/

# result
======================================================================================================= test session starts ========================================================================================================
platform linux -- Python 3.11.4, pytest-7.4.1, pluggy-1.3.0
rootdir: /workspace
plugins: anyio-3.7.1, asyncio-0.21.1
asyncio: mode=Mode.STRICT
collected 17 items                                                                                                                                                                                                                 

tests/test_auth/test_api.py ...                                                                                                                                                                                              [ 17%]
tests/test_auth/test_utils.py ..                                                                                                                                                                                             [ 29%]
tests/test_drugs/test_api.py ..........                                                                                                                                                                                      [ 88%]
tests/test_drugs/test_utils.py ..                                                                                                                                                                                            [100%]

======================================================================================================== 17 passed in 0.67s ========================================================================================================
```
##
#### *Now apps are ready to use.*

## API Endpoints

### Get List of medications

Get a paginated list of possible medications.

- **URL:** `/api/drugs/`
- **Method:** GET
- **Query Parameters:**
  - `page`: Page number for pagination (optional)
  - `size`: Number of items per page (optional)
  - `search`: Search keyword to filter the data (optional)
- **Response:**
  - HTTP status code: 200 OK
  - Response body: Paginated list of Drugs models
  ```json
  {
    "items": [
        {
            "id": "b52d7619-da1f-4d63-805d-1d124fe53df4",
            "diseases": ["bladder disease", "cystitis", "acute cystitis"],
            "description": "Eum et quia aliquam fugiat. Ab est quam esse. Quia quibusdam sunt temporibus repudiandae doloremque ea. Nisi eum aperiam modi tempora blanditiis hic iure mollitia ut.",
            "name": "Folic Acid",
            "released": "29/12/1973",
        },
        ...
    ],
    "total": 200,
    "page": 1,
    "size": 10,
    "pages": 20,
  }
  ```  

### Auth

#### Get access token
This endpoint allows you to obtain an access token for making authenticated requests to the API. The `grant_type` must be set to `password` for a valid request.

- **URL:** `/api/auth/token`
- **Method:** POST
- **Path Parameters:**
  - `grant_type`: Must be `password`
  - `username`: Username 
  - `password`: Password 
  - `client_secret`: SHARED_TOKEN
- **Request Body:**
  - To obtain an access token, send a POST request with the following JSON data:
    ```json
      data = {
          "grant_type": "password",
          "username": "username",
          "password": "password",
          "client_secret": "rRoFT3H6mzMrUW7XuaOGz7VEaFt42QZy8LVLeBCZBEHskm983gmMfb7nJUwmZr2I5NwzyaVSE8DeMeDB8mgmRIwVMuyGPYAOINbUlAFlPNcTUzodQ5VCFpRNNtMJjn4x",
      }
      ```
- **Response:**
  - HTTP status code: 201
  - Response body: Token model
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhIiwiZXhwIjoxNjkzOTQyMTgxfQ.-ftneJbPNdoxwrddc-4KeuWMdg3BFcHawTVAFI7T6oA",
    "token_type": "bearer"
  }
  ```

## Docs
The documentation endpoint is available under docs endpoint.
URL: http://127.0.0.1:8005/docs

## Frontend
The frontend is accessible at http://localhost:3000/.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
