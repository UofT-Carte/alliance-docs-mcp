import alliance_docs_mcp.server as server


def test_import_does_not_build_state():
    # After import, globals are unset until the lifespan runs.
    assert server.storage is None
    assert server.search_index is None
    assert server.related_index is None


def test_build_state_populates_storage(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    docs.mkdir()
    monkeypatch.setenv("DOCS_DIR", str(docs))
    monkeypatch.setenv("DISABLE_SEARCH_INDEX", "1")
    monkeypatch.setenv("DISABLE_RELATED_INDEX", "1")

    state = server.build_state()
    assert state.docs_path == docs.resolve()
    assert state.storage is not None
    assert state.search_index is None
    assert state.related_index is None


def test_apply_state_sets_globals(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    docs.mkdir()
    monkeypatch.setenv("DOCS_DIR", str(docs))
    monkeypatch.setenv("DISABLE_SEARCH_INDEX", "1")
    monkeypatch.setenv("DISABLE_RELATED_INDEX", "1")

    state = server.build_state()
    server._apply_state(state)
    try:
        assert server.storage is state.storage
        assert server.docs_path == docs.resolve()
    finally:
        server._apply_state(
            server.ServerState(server.docs_path, None, None, None)
        )
