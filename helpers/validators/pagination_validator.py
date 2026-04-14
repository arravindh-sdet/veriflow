def validate_pagination(response_json, page, size):
    resp = response_json["responseObject"]

    # Page meta
    assert resp["number"] == page
    assert resp["size"] == size
    assert resp["pageable"]["pageNumber"] == page
    assert resp["pageable"]["pageSize"] == size

    # Content count
    assert len(resp["content"]) == resp["numberOfElements"]
    assert resp["numberOfElements"] <= size

    # Offset check
    assert resp["pageable"]["offset"] == page * size

    # Total pages calculation validation
    expected_total_pages = (resp["totalElements"] + size - 1) // size
    assert resp["totalPages"] == expected_total_pages

    # first/last flags logical
    assert resp["first"] == (page == 0)
    assert resp["last"] == (page == resp["totalPages"] - 1)

    # Content schema validation
    for item in resp["content"]:
        assert "organizationId" in item
        assert "name" in item
