FROM python:3.10-slim

# Set working dir to week2 where the app is located
WORKDIR /app/week2

# Install dependencies
COPY week2/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the week2 directory contents to the working directory
COPY week2/ .

# Start FastAPI with uvicorn (from week2 directory)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 