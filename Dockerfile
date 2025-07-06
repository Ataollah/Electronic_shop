# Stage 1: Base build stage
#FROM python:3.13-slim AS builder
# Stage 1: Base build stage
FROM python:3.13-slim AS builder

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

# Copy the requirements file first (better caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt



# Stage 2: Production stage
FROM python:3.13-slim

RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser . .

# Copy the templates directory
COPY --chown=appuser:appuser templates /app/templates

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set ownership and permissions for media directory
RUN mkdir -p /app/media/website && \
    chown -R appuser:appuser /app/media && \
    chmod -R 755 /app/media

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000


COPY entrypoint.sh /app/entrypoint.sh

# Temporarily switch to root user to change permissions
USER root

# Make the script executable
RUN chmod +x /app/entrypoint.sh

# Switch back to non-root user
USER appuser
# Copy the entrypoint script


# Use the script as the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]


# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "sufficient.wsgi:application"]
#CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "sufficient.asgi:application"]
