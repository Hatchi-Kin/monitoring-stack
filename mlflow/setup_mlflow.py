import os
import time
import logging

import mlflow
from mlflow.server.auth.client import AuthServiceClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Wait for the MLflow server to start
time.sleep(20)

MLFLOW_TRACKIN_FULL_URL = os.getenv("MLFLOW_TRACKIN_FULL_URL")
NEW_USER_USERNAME = os.getenv("NEW_USER_USERNAME")
NEW_USER_PASSWORD = os.getenv("NEW_USER_PASSWORD")

# Set the tracking URI
mlflow.set_tracking_uri(MLFLOW_TRACKIN_FULL_URL)

# Set environment variables for authentication
os.environ['MLFLOW_TRACKING_USERNAME'] = "admin"
os.environ['MLFLOW_TRACKING_PASSWORD'] = "password"

# Initialize the AuthServiceClient with admin credentials
client = AuthServiceClient(MLFLOW_TRACKIN_FULL_URL)

# Create a new user
try:
    client.create_user(NEW_USER_USERNAME, NEW_USER_PASSWORD)
    logger.info("User created successfully.")
except Exception as e:
    logger.error(f"Failed to create user: {e}")

# Set the new user as admin
try:
    client.update_user_admin(NEW_USER_USERNAME, True)
    logger.info("User set as admin successfully.")
except Exception as e:
    logger.error(f"Failed to set user as admin: {e}")

# Delete the default admin user
try:
    client.delete_user("admin")
    logger.info("Default admin user deleted successfully.")
except Exception as e:
    logger.error(f"Failed to delete default admin user: {e}")