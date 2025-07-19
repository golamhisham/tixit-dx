FROM python:3.10-slim

# Set working dir
WORKDIR /app

# Install dependencies
COPY week2/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Start FastAPI with uvicorn (from week2 directory)
CMD ["uvicorn", "week2.main:app", "--host", "0.0.0.0", "--port", "8000"] 