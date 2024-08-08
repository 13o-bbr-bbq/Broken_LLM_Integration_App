FROM python:3.11.6

# Set environment variables.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create FastAPI directory.
ENV APP_HOME=/backend
RUN mkdir -p $APP_HOME

# Set work directory.
WORKDIR $APP_HOME

# Install dependencies.
COPY ./requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY ./secret.md .

# Copy project.
COPY . $APP_HOME

# Chown all the files.
RUN chown -R 1000:1000 $APP_HOME

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
