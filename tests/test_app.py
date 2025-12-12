from fastapi.testclient import TestClient
from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Should return a dict of activities
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    test_activity = "Gym Class"
    test_email = "test_student@example.com"

    # Ensure test email not present
    if test_email in activities[test_activity]["participants"]:
        activities[test_activity]["participants"].remove(test_email)

    # Signup
    signup_resp = client.post(f"/activities/{test_activity}/signup?email={test_email}")
    assert signup_resp.status_code == 200
    assert test_email in activities[test_activity]["participants"]

    # Duplicate signup should fail
    dup_resp = client.post(f"/activities/{test_activity}/signup?email={test_email}")
    assert dup_resp.status_code == 400

    # Unregister
    unregister_resp = client.delete(f"/activities/{test_activity}/unregister?email={test_email}")
    assert unregister_resp.status_code == 200
    assert test_email not in activities[test_activity]["participants"]
