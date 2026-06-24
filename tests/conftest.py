"""
Test fixtures for the High School Management System API

Provides:
- TestClient configured with the FastAPI app
- Fresh activity data for each test to ensure isolation
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Default test data - clean slate for each test
DEFAULT_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": []
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": []
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": []
    },
    "Soccer Team": {
        "description": "Join the school soccer team for practices and matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": []
    },
    "Basketball Club": {
        "description": "Pick-up games and skill development for basketball players",
        "schedule": "Wednesdays and Fridays, 5:00 PM - 7:00 PM",
        "max_participants": 18,
        "participants": []
    },
    "Art Club": {
        "description": "Explore painting, drawing, and mixed media projects",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": []
    },
    "Drama Society": {
        "description": "Acting, play production, and stagecraft",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": []
    },
    "Debate Club": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": []
    },
    "Math Olympiad": {
        "description": "Prepare for math competitions and problem-solving sessions",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    }
}


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset the activities database to a clean state before each test.
    This ensures test isolation and prevents test order dependencies.
    
    Arrange: Initialize activities with default data
    """
    # Clear the in-memory activities dict
    activities.clear()
    
    # Populate with fresh, clean data
    for activity_name, activity_data in DEFAULT_ACTIVITIES.items():
        activities[activity_name] = {
            "description": activity_data["description"],
            "schedule": activity_data["schedule"],
            "max_participants": activity_data["max_participants"],
            "participants": activity_data["participants"].copy()
        }
    
    yield
    
    # Cleanup after test (optional, but good practice)
    activities.clear()


@pytest.fixture
def client():
    """
    Provide a TestClient for making requests to the FastAPI application.
    
    Uses the same app instance with reset activities from reset_activities fixture.
    """
    return TestClient(app)
