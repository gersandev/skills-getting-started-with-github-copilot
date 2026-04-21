"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_new_participant_success(client):
    """Test successfully signing up a new participant"""
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu",
        follow_redirects=False
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]


def test_signup_participant_added_to_activity(client):
    """Test that participant is actually added to the activity"""
    email = "newstudent@mergington.edu"
    
    # Sign up
    response = client.post(
        f"/activities/Chess Club/signup?email={email}"
    )
    assert response.status_code == 200
    
    # Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signing up for non-existent activity returns 404"""
    response = client.post(
        "/activities/NonexistentClub/signup?email=student@mergington.edu"
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_participant_returns_400(client):
    """Test that signing up twice with same email returns 400"""
    email = "michael@mergington.edu"  # Already signed up for Chess Club
    
    response = client.post(
        f"/activities/Chess Club/signup?email={email}"
    )
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_missing_email_parameter(client):
    """Test that missing email parameter returns validation error"""
    response = client.post("/activities/Chess Club/signup")
    assert response.status_code == 422  # Unprocessable Entity (validation error)
