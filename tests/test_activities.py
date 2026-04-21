"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0


def test_get_activities_has_required_fields(client):
    """Test that each activity has required fields"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_details in activities.items():
        assert "description" in activity_details
        assert "schedule" in activity_details
        assert "max_participants" in activity_details
        assert "participants" in activity_details
        assert isinstance(activity_details["participants"], list)


def test_get_activities_participants_are_strings(client):
    """Test that participants list contains strings (emails)"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_details in activities.items():
        for participant in activity_details["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Simple email validation
