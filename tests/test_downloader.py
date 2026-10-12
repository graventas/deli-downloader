from downloader import validate_url

def test_allows_https_supported_host():
    assert validate_url("https://youtu.be/dQw4w9WgXcQ")

def test_rejects_http():
    assert not validate_url("http://youtube.com/watch?v=abc")

def test_rejects_unsupported_host():
    assert not validate_url("https://example.com/video")

def test_rejects_lookalike_domain():
    assert not validate_url("https://youtube.com.evil.example/video")

def test_rejects_credentials():
    assert not validate_url("https://user:pass@youtube.com/watch?v=abc")

def test_rejects_nonstandard_port():
    assert not validate_url("https://youtube.com:8443/watch?v=abc")

def test_rejects_empty_and_too_long():
    assert not validate_url("")
    assert not validate_url("https://youtube.com/" + "a" * 2100)
