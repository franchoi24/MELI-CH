# FastAPI App

This FastAPI application provides a health check endpoint, a POST endpoint to check mutant DNA, and a stats endpoint. The database used is SQLite for ease of deployment in free-tier cloud providers.

## Endpoints

### 1. **Health Check (GET `/`)**
- **URL**: `/`
- **Method**: `GET`
- **Response**:
    ```json
    {
        "message": "Hello world"
    }
    ```
    This endpoint returns a simple health check message.

### 2. **Mutant DNA Check (POST `/mutants`)**
- **URL**: `/mutants`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "dna": [
            "ATGCGA",
            "CAGTGC",
            "TTATGT",
            "AGAAGG",
            "CCCCTA",
            "TCACTG"
        ],
        "recursive": true
    }
    ```
- **Body Parameters**:
    - `dna` (required): A list of strings representing a DNA matrix of size NxN. Each string must only contain characters from the set {A, C, G, T}.
    - `recursive` (optional): A boolean flag. If true, the function will use a recursive method to analyze the DNA.
- **Response**:
    - If the DNA is mutant, the server will return a response { `is_mutant`:  `true`}. Otherwise, it will return a status code 409.
    - Status code 422 for invalid input.
  
### 3. **DNA Stats (GET `/stats`)**
- **URL**: `/stats`
- **Method**: `GET`
- **Response**:
    ```json
    {
        "count_mutant_dna": 10,
        "count_human_dna": 20,
        "ratio": 0.5
    }
    ```
    - `count_mutant_dna`: The total number of mutant DNA samples.
    - `count_human_dna`: The total number of human DNA samples.
    - `ratio`: The ratio of mutants to humans, calculated as `count_mutant_dna / count_human_dna`.

## Deployment URL
The app is deployed at: [https://shocked-tilly-itbaprojects-b11cd12f.koyeb.app/](https://shocked-tilly-itbaprojects-b11cd12f.koyeb.app/)

## Local Deployment

### Prerequisites
- Python 3.7+
- `pip` (Python package installer)

### Installation

1. Clone the repository:
    ```bash
    git clone git@github.com:franchoi24/MELI-CH.git
    cd MELI-CH
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the App

To run the FastAPI app locally:
```bash
uvicorn main:app --reload
  ```

### Testing the App Locally

To test the app locally, you can run the following:

1. **Run tests using pytest**:
    ```bash
    pytest
    ```

2. **Test individual functions**:
    If you want to run specific tests, use:
    ```bash
    pytest tests/test_mutant_service.py  # Example for testing DNA validation
    ```

### SQLite Database

The app uses SQLite as the database. You don't need to do anything extra for it to work locally because SQLite is embedded and stored in a `.db` file in the local filesystem. The database schema will be created automatically when the app is run for the first time via the `SQLModel.metadata.create_all(engine)` command.

