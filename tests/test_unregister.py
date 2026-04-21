"""
Tests for the POST /activities/{activity_name}/unregister endpoint.
"""

import pytest


def test_unregister_existing_participant_success(client):
    """Test successfully unregistering an existing participant"""
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.post(
        f"/activities/Chess Club/unregister?email={email}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]


def test_unregister_participant_removed_from_activity(client):
    """Test that participant is actually removed from the activity"""
    email = "michael@mergington.edu"
    
    # Unregister
    response = client.post(
        f"/activities/Chess Club/unregister?email={email}"
    )
    assert response.status_code == 200
    
    # Verify participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_nonexistent_activity_returns_404(client):
    """Test that unregistering from non-existent activity returns 404"""
    response = client.post(
        "/activities/NonexistentClub/unregister?email=student@mergington.edu"
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_non_registered_participant_returns_400(client):
    """Test that unregistering a non-registered participant returns 400"""
    response = client.post(
        "/activities/Chess Club/unregister?email=notamember@mergington.edu"
    )
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"]


def test_unregister_missing_email_parameter(client):
    """Test that missing email parameter returns validation error"""
    response = client.post("/activities/Chess Club/unregister")
    assert response.status_code == 422  # Unprocessable Entity (validation error)
