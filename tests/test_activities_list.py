"""
Tests for the activities list endpoint (GET /activities)

This endpoint returns all available extracurricular activities.
"""

import pytest


class TestActivitiesListEndpoint:
    """Test suite for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all 9 activities
        
        Arrange: Using default fixture with all 9 activities
        Act: Make GET request to /activities
        Assert: Verify we receive all 9 activities
        """
        # Arrange
        expected_activity_names = {
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Basketball Club",
            "Art Club",
            "Drama Society",
            "Debate Club",
            "Math Olympiad"
        }
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
        activities = response.json()
        assert len(activities) == 9, f"Expected 9 activities, got {len(activities)}"
        assert set(activities.keys()) == expected_activity_names, \
            f"Activity names don't match. Expected {expected_activity_names}, got {set(activities.keys())}"
    
    def test_get_activities_returns_correct_schema(self, client):
        """
        Test that each activity has the correct schema with all required fields
        
        Arrange: Prepare expected schema fields
        Act: Make GET request and inspect activity structure
        Assert: Verify each activity has description, schedule, max_participants, and participants
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict), \
                f"Activity {activity_name} should be a dictionary"
            activity_fields = set(activity_data.keys())
            assert activity_fields == required_fields, \
                f"Activity {activity_name} has incorrect fields. Expected {required_fields}, got {activity_fields}"
    
    def test_get_activities_returns_valid_field_types(self, client):
        """
        Test that all activity fields have the correct data types
        
        Arrange: Define expected types for each field
        Act: Fetch activities and check field types
        Assert: Verify description and schedule are strings, max_participants is int, participants is list
        """
        # Arrange
        # (types to validate)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["description"], str), \
                f"{activity_name} description should be a string"
            assert isinstance(activity_data["schedule"], str), \
                f"{activity_name} schedule should be a string"
            assert isinstance(activity_data["max_participants"], int), \
                f"{activity_name} max_participants should be an integer"
            assert isinstance(activity_data["participants"], list), \
                f"{activity_name} participants should be a list"
    
    def test_get_activities_participants_list_is_initially_empty(self, client):
        """
        Test that all activities start with empty participants list (test isolation)
        
        Arrange: Expect fresh data from fixture
        Act: Fetch activities
        Assert: Verify all participants lists are empty (test isolation working)
        """
        # Arrange
        # (expecting clean slate from fixture)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert len(activity_data["participants"]) == 0, \
                f"{activity_name} should start with empty participants list, but has: {activity_data['participants']}"
    
    def test_get_activities_has_valid_descriptions(self, client):
        """
        Test that all activities have non-empty descriptions
        
        Arrange: Prepare client
        Act: Fetch activities
        Assert: Verify all descriptions are non-empty strings
        """
        # Arrange
        # (setup handled by fixtures)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert len(activity_data["description"]) > 0, \
                f"{activity_name} should have a non-empty description"
    
    def test_get_activities_has_valid_schedules(self, client):
        """
        Test that all activities have non-empty schedules
        
        Arrange: Prepare client
        Act: Fetch activities
        Assert: Verify all schedules are non-empty strings
        """
        # Arrange
        # (setup handled by fixtures)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert len(activity_data["schedule"]) > 0, \
                f"{activity_name} should have a non-empty schedule"
