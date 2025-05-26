

async def test_add_facility(ac):
    resp = await ac.post("/facilities/", json={"name": "WiFi"})
    assert resp.status_code == 200


async def test_get_facilities(ac):
    resp = await ac.get("/facilities/")
    assert resp.status_code == 200
