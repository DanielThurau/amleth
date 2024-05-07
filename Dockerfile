# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /amleth

# Copy the current directory contents into the container at /app
COPY . /amleth

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r /amleth/requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

VOLUME /amleth/data

CMD ["python3", "/amleth/amleth/main.py"]

