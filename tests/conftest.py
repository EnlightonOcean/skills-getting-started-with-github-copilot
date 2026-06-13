import pytest
import copy
from fastapi.testclient import TestClient

from src.app import app, activities

@pytest.fixture
def client():
    # Arrange (fixture level) - save original state
    original_activities = copy.deepcopy(activities)
    
    # Yield test client
    with TestClient(app) as test_client:
        yield test_client
        
    # Teardown - restore state
    activities.clear()
    activities.update(original_activities)
