"""
Tests for the activity signup endpoint (POST /activities/{activity_name}/signup)

This endpoint allows students to sign up for extracurricular activities.
"""

import pytest


class TestSignupEndpoint:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""
    
    # ==================== SUCCESS SCENARIOS ====================
    
    def test_successful_signup_single_student(self, client):
        """
        Test that a student can successfully sign up for an activity
        
        Arrange: Prepare email and activity name
        Act: Make POST request to signup endpoint
        Assert: Verify response status 200 and student appears in participants list
        """
        # Arrange
        email = "alice@example.com"
        activity = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
        assert response.json()["message"] == f"Signed up {email} for {activity}"
        
        # Verify student was added to participants list
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity]["participants"], \
            f"Student {email} should be in participants list for {activity}"
    
    def test_successful_signup_returns_confirmation_message(self, client):
        """
        Test that successful signup returns appropriate confirmation message
        
        Arrange: Prepare test data
        Act: Sign up student
        Assert: Verify response contains confirmation message with email and activity name
        """
        # Arrange
        email = "bob@example.com"
        activity = "Programming Class"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert "message" in response_data
        assert email in response_data["message"]
        assert activity in response_data["message"]
    
    def test_multiple_students_can_signup_for_same_activity(self, client):
        """
        Test that multiple different students can sign up for the same activity
        
        Arrange: Prepare multiple email addresses
        Act: Sign up each student to the same activity
        Assert: Verify all students appear in the participants list
        """
        # Arrange
        emails = ["student1@example.com", "student2@example.com", "student3@example.com"]
        activity = "Art Club"
        
        # Act
        for email in emails:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200, f"Failed to sign up {email}"
        
        # Assert
        activities_response = client.get("/activities")
        activities = activities_response.json()
        participants = activities[activity]["participants"]
        
        for email in emails:
            assert email in participants, f"Student {email} should be in {activity} participants"
        
        assert len(participants) == len(emails), \
            f"Expected {len(emails)} participants, got {len(participants)}"
    
    def test_one_student_can_signup_for_multiple_activities(self, client):
        """
        Test that a single student can sign up for multiple different activities
        
        Arrange: Prepare one email and multiple activities
        Act: Sign up same student to different activities
        Assert: Verify student appears in participants list for each activity
        """
        # Arrange
        email = "charlie@example.com"
        activities_to_join = ["Chess Club", "Gym Class", "Drama Society"]
        
        # Act
        for activity in activities_to_join:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200, f"Failed to sign up for {activity}"
        
        # Assert
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        for activity in activities_to_join:
            assert email in activities[activity]["participants"], \
                f"Student {email} should be in {activity} participants"
    
    # ==================== ERROR SCENARIOS ====================
    
    def test_signup_to_nonexistent_activity_returns_404(self, client):
        """
        Test that attempting to sign up for a non-existent activity returns 404
        
        Arrange: Prepare invalid activity name
        Act: Attempt signup with invalid activity
        Assert: Verify response status is 404 and error message is appropriate
        """
        # Arrange
        email = "david@example.com"
        invalid_activity = "Nonexistent Club"
        
        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404, f"Expected 404 Not Found, got {response.status_code}"
        assert "Activity not found" in response.json()["detail"]
    
    def test_duplicate_signup_returns_400_error(self, client):
        """
        Test that attempting to sign up twice for the same activity returns 400
        
        Arrange: Sign up a student first
        Act: Attempt to sign up the same student again
        Assert: Verify second signup returns 400 and appropriate error message
        """
        # Arrange
        email = "eve@example.com"
        activity = "Soccer Team"
        
        # First signup should succeed
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200, "First signup should succeed"
        
        # Act: Attempt duplicate signup
        response2 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response2.status_code == 400, f"Expected 400 Bad Request, got {response2.status_code}"
        assert "already signed up" in response2.json()["detail"]
    
    def test_duplicate_signup_does_not_add_duplicate_participant(self, client):
        """
        Test that duplicate signup attempts don't add duplicate entries to participants list
        
        Arrange: Sign up a student once
        Act: Attempt duplicate signup (will fail)
        Assert: Verify participants list contains only one instance of the email
        """
        # Arrange
        email = "frank@example.com"
        activity = "Basketball Club"
        
        # Sign up once
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Act: Attempt duplicate signup
        response2 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response2.status_code == 400
        
        # Assert
        activities_response = client.get("/activities")
        activities = activities_response.json()
        participants = activities[activity]["participants"]
        
        count = participants.count(email)
        assert count == 1, f"Expected email to appear once, but it appears {count} times"
    
    # ==================== STATE VERIFICATION SCENARIOS ====================
    
    def test_signup_preserves_other_activities_unchanged(self, client):
        """
        Test that signing up for one activity doesn't affect other activities
        
        Arrange: Get initial state of all activities
        Act: Sign up for one activity
        Assert: Verify only that activity was modified, others remain unchanged
        """
        # Arrange
        email = "grace@example.com"
        target_activity = "Debate Club"
        
        initial_response = client.get("/activities")
        initial_activities = initial_response.json()
        
        # Act
        response = client.post(
            f"/activities/{target_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        
        final_response = client.get("/activities")
        final_activities = final_response.json()
        
        for activity_name, activity_data in final_activities.items():
            if activity_name == target_activity:
                assert email in activity_data["participants"], \
                    f"Email should be in {target_activity} participants"
            else:
                assert activity_data["participants"] == initial_activities[activity_name]["participants"], \
                    f"Participants in {activity_name} should not have changed"
    
    def test_participant_count_increments_correctly(self, client):
        """
        Test that participant count increases correctly with each successful signup
        
        Arrange: Track participant count after each signup
        Act: Sign up multiple students sequentially
        Assert: Verify count increases by 1 with each signup
        """
        # Arrange
        emails = ["h@example.com", "i@example.com", "j@example.com"]
        activity = "Math Olympiad"
        
        # Act & Assert
        for idx, email in enumerate(emails):
            # Check count before signup
            response_before = client.get("/activities")
            activities_before = response_before.json()
            count_before = len(activities_before[activity]["participants"])
            
            # Perform signup
            signup_response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert signup_response.status_code == 200
            
            # Check count after signup
            response_after = client.get("/activities")
            activities_after = response_after.json()
            count_after = len(activities_after[activity]["participants"])
            
            # Verify count increased by 1
            assert count_after == count_before + 1, \
                f"After signup #{idx + 1}, count should be {count_before + 1}, got {count_after}"
            assert email in activities_after[activity]["participants"]
    
    def test_signup_response_does_not_leak_other_participants(self, client):
        """
        Test that signup response only contains confirmation, not full activity data
        
        Arrange: Sign up student
        Act: Check signup response
        Assert: Verify response contains message but not sensitive participant data
        """
        # Arrange
        email = "kate@example.com"
        activity = "Programming Class"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        
        # Response should have message but not activity details
        assert "message" in response_data
        assert "description" not in response_data
        assert "schedule" not in response_data
        assert "max_participants" not in response_data
        assert "participants" not in response_data
