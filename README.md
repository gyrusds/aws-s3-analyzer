# AWS S3 Analyzer

## Description

A program that analyzes files in specified S3 buckets and calculates the size of each directory would typically perform the following tasks:

Connect to AWS S3: Establish a connection with the AWS S3 service using appropriate credentials.

1. List Buckets: Retrieve a list of all specified S3 buckets to be analyzed.
2. List Objects: For each bucket, list all objects (files) and their respective paths.
3. Organize by Directory: Group the objects by their directory paths.
4. Calculate Sizes: Sum the sizes of all objects within each directory to determine the total size of each directory.
5. Output Results: Output the directory sizes in a readable format, such as a report or a JSON file.

There is a simple portal to see the information properly.

## Modules

- Analyzer. Run to generate S3 information.
- Backend. Just an API with FastAPI and python.
- Frontend. A portal to see information properly made with React.

## Execution

1. Install Docker.

2. Build the containers.

    ```sh
    docker compose build
    ```

3. Run the containers.

    ```sh
    docker compose up
    ```

4. Open the website: <http:0.0.0.0>

## HOW-TOs

### **HOWTO** Execute analyzer

Follow these steps inside the folder `analyzer`:

1. Install Poetry: If you haven't already, install Poetry by running the following command in your terminal:

    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```

2. . Install dependencies: Run the following command to install the dependencies specified in the `pyproject.toml` file:

    ```sh
    poetry install
    ```

3. Run the code: To run your Python code with Poetry, use the following command:

    ```sh
    poetry run python src/main.py
    ```

    Use `-h` option to see program options.

### **HOWTO** Run the backend

Follow this steps inside the folder `backend`.

1. Install poetry (like `analyzer` in the previous section).

2. Install dependencies:

    ```sh
    poetry install
    ```

3. Run the API:

    ```sh
    poetry run python src/main.py
    ```

### **HOWTO** Run the portal

Follow this steps inside the folder `frontend`.

1. Install dependencies.

    ```sh
    npm install
    ```

2. Run the portal.

    ```sh
    npm run
    ```
