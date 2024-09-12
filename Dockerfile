# syntax=docker/dockerfile:1

FROM python:3.9-bookworm

# Set the working directory inside the container
WORKDIR /python-docker

# Install the ODBC driver for SQL Server
RUN apt-get update && apt-get install -y unixodbc unixodbc-dev

# Install the Microsoft ODBC driver for SQL Server
RUN apt-get update && apt-get install -y gnupg2 curl
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Copy the Python requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy the local code to the container's work directory
COPY . .

# Get Environment variables
ENV DB_CONNECTION_STRING=
# Environment variable to hold the database connection string
# ENV DB_CONNECTION_STRING="mssql+pyodbc://sqladmin:P@ssw0rd1234!@wilde-mssql-server.database.windows.net/wilde-mssql-app-db?driver=ODBC+Driver+18+for+SQL+Server&trustServerCertificate=no"

# Add the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint to initialize the configuration
ENTRYPOINT ["/entrypoint.sh"]