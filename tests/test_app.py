import app as webapp

def test_home_page_returns_ok():
    client = webapp.app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Deli Downloader" in response.data

def test_invalid_url_is_rejected():
    client = webapp.app.test_client()
    response = client.post("/download", data={"url": "https://example.com/video"})
    assert response.status_code == 400
    assert b"URL HTTPS" in response.data
