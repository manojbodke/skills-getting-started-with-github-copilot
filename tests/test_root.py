"""
Tests for the root endpoint (GET /)

This endpoint redirects to the static HTML page.
"""

import pytest


class TestRootEndpoint:
    """Test suite for GET / endpoint"""
    
    def test_root_redirects_to_static_index(self, client):
        """
        Test that GET / redirects to /static/index.html
        
        Arrange: No setup needed, using default client from fixture
        Act: Make GET request to root endpoint
        Assert: Verify redirect status code (307 temporary redirect) and location header
        """
        # Arrange
        expected_redirect_location = "/static/index.html"
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307, f"Expected 307 redirect, got {response.status_code}"
        assert response.headers["location"] == expected_redirect_location, \
            f"Expected redirect to {expected_redirect_location}, got {response.headers.get('location')}"
    
    def test_root_redirect_response_contains_location_header(self, client):
        """
        Test that the redirect response contains a valid location header
        
        Arrange: Prepare client
        Act: Make GET request to root
        Assert: Verify location header exists and is not empty
        """
        # Arrange
        # (setup handled by fixtures)
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert "location" in response.headers, "Response should contain location header for redirect"
        assert len(response.headers["location"]) > 0, "Location header should not be empty"
