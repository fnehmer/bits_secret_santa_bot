
FROM python:3.6.8

RUN mkdir -p /usr/src/app

# Update working directory
WORKDIR /usr/src/app

# copy everything from this directory to server/flask docker container
COPY . /usr/src/app/

# Give execute permission to below file, so that the script can be executed by docker.
RUN chmod 777 /usr/src/app/app.py

RUN chmod 777 /usr/src/app/start_server.sh

RUN chmod +x /usr/src/app/start_server.sh

# Install the Python libraries
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# run server
CMD ["./start_server.sh"]
