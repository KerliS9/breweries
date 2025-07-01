FROM python:3.8

WORKDIR /src

COPY . /src

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
