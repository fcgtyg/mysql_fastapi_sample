# Sample Program with FastAPI and MySQL

This project is a sample program developed using FastAPI and MySQL. It can be easily started with Docker Compose.

## Requirements

- Docker
- Docker Compose

## How to Run

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/fcgtyg/mysql_fastapi_sample.git
    cd your-repo
    ```

2. **Configure Environment Variables:**

    Create a `.env` file in the root directory and set the following environment variables. These are example values; do not use them in a real environment.

    ```env
    # MySQL Settings
    MYSQL_ROOT_PASSWORD=myrootpassword
    MYSQL_DATABASE=mydbname
    MYSQL_USER=mydbuser
    MYSQL_PASSWORD=mydbpassword
    ```

3. **Start the Project:**

    To start the project with Docker Compose, run the following command in the terminal:

    ```bash
    docker-compose up -d
    ```

    This command will start the FastAPI application and MySQL database.

4. **Access the API and Documentation:**

    Once the project is running, you can access the Swagger documentation at [http://localhost:8000/docs](http://localhost:8000/docs). The API is available at [http://localhost:8000](http://localhost:8000).

## Important Notes

- **Environment Variables:** Ensure that the environment variables in the `.env` file are set correctly. These values are examples and should not be used in a production environment.

- **Data Persistence:** By default, data in the MySQL container is not persistent. To make the data persistent, add the following line to the `docker-compose.yml` file under the `volumes` section for the MySQL service:

    ```yaml
    volumes:
      - ./mysql-data:/var/lib/mysql
    ```

    This will create a local `mysql-data` directory that stores the MySQL data and survives container restarts.

## More Information

For more information about the project, you can refer to the [FastAPI documentation](https://fastapi.tiangolo.com/) and [Docker Compose documentation](https://docs.docker.com/compose/).
