FROM python:3.7-alpine

# Set virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy packages
COPY app/ app/

# Run app
CMD ["python", "app"]