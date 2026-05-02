from datetime import timedelta


class TestLogin:
    """POST /auth/login"""

    def test_success(self, client):
        res = client.post("/auth/login", json={"username": "alice", "password": "alice123"})
        assert res.status_code == 200
        body = res.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"

    def test_wrong_password(self, client):
        res = client.post("/auth/login", json={"username": "alice", "password": "wrong"})
        assert res.status_code == 401

    def test_unknown_user(self, client):
        res = client.post("/auth/login", json={"username": "nobody", "password": "pass"})
        assert res.status_code == 401

    def test_missing_fields(self, client):
        res = client.post("/auth/login", json={})
        assert res.status_code == 422


class TestGetMe:
    """GET /auth/me"""

    def _login(self, client) -> str:
        res = client.post("/auth/login", json={"username": "alice", "password": "alice123"})
        return res.json()["access_token"]

    def test_valid_token_returns_user_info(self, client):
        token = self._login(client)
        res = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        body = res.json()
        assert body["username"] == "alice"
        assert body["email"] == "alice@example.com"

    def test_without_token(self, client):
        res = client.get("/auth/me")
        assert res.status_code == 401

    def test_invalid_token(self, client):
        res = client.get("/auth/me", headers={"Authorization": "Bearer invalid.token.here"})
        assert res.status_code == 401

    def test_expired_token(self, client):
        from app.auth import create_access_token
        token = create_access_token({"sub": "alice"}, expires_delta=timedelta(seconds=-1))
        res = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 401

    def test_inactive_user_is_rejected_at_login(self, client):
        # Login must fail for inactive users — no JWT should be issued
        res = client.post(
            "/auth/login", json={"username": "inactive_user", "password": "inactive123"}
        )
        assert res.status_code == 401
        assert "access_token" not in res.json()


class TestProtectedEndpoints:
    """All non-auth endpoints require a valid JWT."""

    def test_access_without_token_is_rejected(self, client):
        res = client.post("/prompt-leaking-lv1", json={"text": "hello"})
        assert res.status_code == 401

    def test_access_with_valid_token_passes_auth(self, client):
        login_res = client.post("/auth/login", json={"username": "alice", "password": "alice123"})
        token = login_res.json()["access_token"]
        res = client.post(
            "/prompt-leaking-lv1",
            json={"text": "hello"},
            headers={"Authorization": f"Bearer {token}"},
        )
        # LLM call is mocked, so the exact response varies — just confirm auth passed (not 401)
        assert res.status_code != 401
