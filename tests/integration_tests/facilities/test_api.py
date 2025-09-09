

async def test_add_facility(ac):
    facility_title = "WiFi"
    resp = await ac.post("/facilities/", json={"name": facility_title})
    assert resp.status_code == 200
    res = resp.json()
    assert isinstance(res, dict)
    assert res["data"]["name"] == facility_title
    assert "data" in res


async def test_get_facilities(ac):
    resp = await ac.get("/facilities/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
