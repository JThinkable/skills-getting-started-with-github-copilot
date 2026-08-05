from urllib.parse import quote

from src.app import activities


def test_get_activities(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert activity_name in data
    assert isinstance(data[activity_name]["participants"], list)


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "test.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    updated = client.get("/activities").json()
    assert email in updated[activity_name]["participants"]


def test_duplicate_signup_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate.student@mergington.edu"
    client.post(
        f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
    )

    # Act
    response = client.post(
        f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"

    updated = client.get("/activities").json()
    assert updated[activity_name]["participants"].count(email) == 1


def test_delete_participant(client):
    # Arrange
    activity_name = "Basketball"
    email = "alex@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name)}/participants?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]

    updated = client.get("/activities").json()
    assert email not in updated[activity_name]["participants"]


def test_delete_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Basketball"
    email = "unknown@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name)}/participants?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
