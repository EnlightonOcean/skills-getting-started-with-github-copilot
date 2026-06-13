from src.app import activities

def test_read_root_redirects(client):
    # Arrange
    url = "/"

    # Act
    response = client.get(url, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    assert response.json() == activities


def test_signup_for_activity_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    url = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_for_activity_not_found(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "test@mergington.edu"
    url = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_for_activity_already_signed_up(client):
    # Arrange
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]  # Get an already signed-up student
    url = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_unregister_from_activity_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]  # Get an existing student
    url = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]


def test_unregister_from_activity_not_found(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "test@mergington.edu"
    url = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_from_activity_not_signed_up(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not_in_club@mergington.edu"
    url = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student not signed up for this activity"}
