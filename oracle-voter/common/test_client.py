def test_200_OK(http_mock, http_get_client, get_loop):
    url = "http://google.com"
    resp_body = {"hello": "world"}
    http_mock.get(url, status=200, payload=resp_body)
    result = get_loop.run_until_complete(http_get_client(url))
    assert result == resp_body
