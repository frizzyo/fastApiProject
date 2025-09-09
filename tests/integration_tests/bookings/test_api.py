import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2024-01-01", "2025-01-01", 200),
    (1, "2024-01-02", "2025-01-02", 200),
    (1, "2024-01-03", "2025-01-03", 200),
    (1, "2024-01-04", "2025-01-04", 200),
    (1, "2024-01-05", "2025-01-05", 200),
    (1, "2024-01-06", "2025-01-06", 500),
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db, authenticated_ac):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post('/bookings/', json={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to
    })
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "success"
        assert "data" in res
