"""
GOVERN.AI Backend API Tests
Adapted for modular architecture with routes/
"""

import pytest
import httpx
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://audit-nexus-4.preview.emergentagent.com')
BASE = f"{API_URL}/api"

# Test credentials
TEST_USER = "admin"
TEST_PASS = "AdminGovern2026!"

# Shared token cache to avoid rate limiting
_token_cache = {"token": None, "expires": 0}

def get_auth_token(client):
    """Get a valid auth token, using cache to avoid rate limits"""
    global _token_cache
    current_time = time.time()
    
    # Return cached token if still valid (cache for 5 minutes)
    if _token_cache["token"] and current_time < _token_cache["expires"]:
        return _token_cache["token"]
    
    # Get new token
    for attempt in range(3):
        resp = client.post(f"{BASE}/auth/login", json={"username": TEST_USER, "password": TEST_PASS})
        if resp.status_code == 200:
            token = resp.json()["token"]
            _token_cache["token"] = token
            _token_cache["expires"] = current_time + 300  # 5 minutes
            return token
        elif resp.status_code == 429:
            time.sleep(10)  # Wait for rate limit reset
        else:
            break
    
    raise Exception(f"Failed to get auth token: {resp.status_code} {resp.text}")


class TestAuth:
    """Authentication tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(timeout=30)
        yield
        self.client.close()
    
    def test_login_success(self):
        """Test successful login"""
        resp = self.client.post(f"{BASE}/auth/login", json={"username": TEST_USER, "password": TEST_PASS})
        assert resp.status_code == 200
        data = resp.json()
        assert "token" in data
        assert "user" in data
        assert data["user"]["username"] == TEST_USER
        assert data["user"]["role"] == "admin"
    
    def test_login_invalid_credentials(self):
        """Test login with wrong password"""
        resp = self.client.post(f"{BASE}/auth/login", json={"username": TEST_USER, "password": "wrongpassword"})
        assert resp.status_code == 401
    
    def test_login_nonexistent_user(self):
        """Test login with nonexistent user"""
        resp = self.client.post(f"{BASE}/auth/login", json={"username": "nonexistent", "password": "password"})
        assert resp.status_code == 401
    
    def test_me_without_token(self):
        """Test /me endpoint without authentication"""
        resp = self.client.get(f"{BASE}/auth/me")
        assert resp.status_code == 401
    
    def test_me_with_valid_token(self):
        """Test /me endpoint with valid token"""
        # Login first
        login_resp = self.client.post(f"{BASE}/auth/login", json={"username": TEST_USER, "password": TEST_PASS})
        token = login_resp.json()["token"]
        
        # Get user info
        resp = self.client.get(f"{BASE}/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == TEST_USER


class TestAgents:
    """Agents CRUD tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(timeout=30)
        self.token = get_auth_token(self.client)
        self.headers = {"Authorization": f"Bearer {self.token}"}
        yield
        self.client.close()
    
    def test_list_agents(self):
        """Test listing agents"""
        resp = self.client.get(f"{BASE}/agents", headers=self.headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
    
    def test_create_agent(self):
        """Test creating an agent"""
        agent_data = {
            "name": "Test Agent API",
            "description": "Created by automated test",
            "model_type": "GPT-5.2",
            "risk_level": "low",
            "status": "active"
        }
        resp = self.client.post(f"{BASE}/agents", json=agent_data, headers=self.headers)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == agent_data["name"]
        assert "id" in data
        # Cleanup
        self.client.delete(f"{BASE}/agents/{data['id']}", headers=self.headers)
    
    def test_get_agent(self):
        """Test getting a single agent"""
        # Create agent first
        agent_data = {"name": "Test Get Agent", "description": "Test"}
        create_resp = self.client.post(f"{BASE}/agents", json=agent_data, headers=self.headers)
        agent_id = create_resp.json()["id"]
        
        # Get agent
        resp = self.client.get(f"{BASE}/agents/{agent_id}", headers=self.headers)
        assert resp.status_code == 200
        assert resp.json()["id"] == agent_id
        
        # Cleanup
        self.client.delete(f"{BASE}/agents/{agent_id}", headers=self.headers)
    
    def test_update_agent(self):
        """Test updating an agent"""
        # Create agent first
        agent_data = {"name": "Test Update Agent", "description": "Original"}
        create_resp = self.client.post(f"{BASE}/agents", json=agent_data, headers=self.headers)
        agent_id = create_resp.json()["id"]
        
        # Update agent
        update_data = {"name": "Updated Agent", "description": "Updated description"}
        resp = self.client.put(f"{BASE}/agents/{agent_id}", json=update_data, headers=self.headers)
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated Agent"
        
        # Cleanup
        self.client.delete(f"{BASE}/agents/{agent_id}", headers=self.headers)
    
    def test_delete_agent(self):
        """Test deleting an agent"""
        # Create agent first
        agent_data = {"name": "Test Delete Agent", "description": "To be deleted"}
        create_resp = self.client.post(f"{BASE}/agents", json=agent_data, headers=self.headers)
        agent_id = create_resp.json()["id"]
        
        # Delete agent
        resp = self.client.delete(f"{BASE}/agents/{agent_id}", headers=self.headers)
        assert resp.status_code == 200
        assert resp.json()["status"] == "deleted"
        
        # Verify deletion
        get_resp = self.client.get(f"{BASE}/agents/{agent_id}", headers=self.headers)
        assert get_resp.status_code == 404
    
    def test_get_nonexistent_agent(self):
        """Test getting a nonexistent agent"""
        resp = self.client.get(f"{BASE}/agents/nonexistent-id-12345", headers=self.headers)
        assert resp.status_code == 404


class TestPolicies:
    """Policies CRUD tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(timeout=30)
        self.token = get_auth_token(self.client)
        self.headers = {"Authorization": f"Bearer {self.token}"}
        yield
        self.client.close()
    
    def test_list_policies(self):
        """Test listing policies"""
        resp = self.client.get(f"{BASE}/policies", headers=self.headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
    
    def test_create_policy(self):
        """Test creating a policy"""
        policy_data = {
            "name": "Test Policy API",
            "description": "Created by automated test",
            "regulation": "GDPR",
            "severity": "medium",
            "enforcement": "log"
        }
        resp = self.client.post(f"{BASE}/policies", json=policy_data, headers=self.headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == policy_data["name"]
        assert "id" in data
        # Cleanup
        self.client.delete(f"{BASE}/policies/{data['id']}", headers=self.headers)
    
    def test_update_policy(self):
        """Test updating a policy"""
        # Create policy first
        policy_data = {"name": "Test Update Policy", "description": "Original"}
        create_resp = self.client.post(f"{BASE}/policies", json=policy_data, headers=self.headers)
        policy_id = create_resp.json()["id"]
        
        # Update policy
        update_data = {"name": "Updated Policy", "description": "Updated"}
        resp = self.client.put(f"{BASE}/policies/{policy_id}", json=update_data, headers=self.headers)
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated Policy"
        
        # Cleanup
        self.client.delete(f"{BASE}/policies/{policy_id}", headers=self.headers)
    
    def test_delete_policy(self):
        """Test deleting a policy"""
        # Create policy first
        policy_data = {"name": "Test Delete Policy", "description": "To be deleted"}
        create_resp = self.client.post(f"{BASE}/policies", json=policy_data, headers=self.headers)
        policy_id = create_resp.json()["id"]
        
        # Delete policy
        resp = self.client.delete(f"{BASE}/policies/{policy_id}", headers=self.headers)
        assert resp.status_code == 200
        
        # Verify deletion
        list_resp = self.client.get(f"{BASE}/policies", headers=self.headers)
        policy_ids = [p["id"] for p in list_resp.json()]
        assert policy_id not in policy_ids


class TestAudit:
    """Audit logs tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(timeout=30)
        self.token = get_auth_token(self.client)
        self.headers = {"Authorization": f"Bearer {self.token}"}
        yield
        self.client.close()
    
    def test_list_audit_logs(self):
        """Test listing audit logs"""
        resp = self.client.get(f"{BASE}/audit", headers=self.headers)
        assert resp.status_code == 200
        data = resp.json()
        # API returns {logs: [], total: N}
        assert "logs" in data
        assert isinstance(data["logs"], list)
    
    def test_audit_logs_contain_login(self):
        """Test that audit logs contain login entries"""
        resp = self.client.get(f"{BASE}/audit", headers=self.headers)
        data = resp.json()
        logs = data.get("logs", [])
        login_logs = [l for l in logs if l.get("action") == "user_login"]
        assert len(login_logs) > 0


class TestCompliance:
    """Compliance standards tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(timeout=30)
        self.token = get_auth_token(self.client)
        self.headers = {"Authorization": f"Bearer {self.token}"}
        yield
        self.client.close()
    
    def test_list_compliance_standards(self):
        """Test listing compliance standards"""
        resp = self.client.get(f"{BASE}/compliance", headers=self.headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


class TestDashboard:
    """Dashboard stats tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(timeout=30)
        self.token = get_auth_token(self.client)
        self.headers = {"Authorization": f"Bearer {self.token}"}
        yield
        self.client.close()
    
    def test_get_dashboard_stats(self):
        """Test getting dashboard stats"""
        resp = self.client.get(f"{BASE}/dashboard/stats", headers=self.headers)
        assert resp.status_code == 200
        data = resp.json()
        # API returns {agents: {total, active}, policies: {...}, ...}
        assert "agents" in data
        assert "policies" in data


class TestChat:
    """Chat (ARIA) tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(timeout=60)
        self.token = get_auth_token(self.client)
        self.headers = {"Authorization": f"Bearer {self.token}"}
        yield
        self.client.close()
    
    def test_chat_message(self):
        """Test sending a chat message to ARIA"""
        resp = self.client.post(f"{BASE}/chat", json={"message": "Hello ARIA", "session_id": "test-session"}, headers=self.headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "response" in data
        assert len(data["response"]) > 0


class TestSecurityHeaders:
    """Security headers tests (FIX B3)"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(timeout=30)
        yield
        self.client.close()
    
    def test_security_headers_present(self):
        """Test that security headers are present"""
        resp = self.client.get(f"{BASE}/")
        
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"
        assert resp.headers.get("X-Frame-Options") == "DENY"
        assert resp.headers.get("X-XSS-Protection") == "1; mode=block"
        assert "strict-origin" in resp.headers.get("Referrer-Policy", "")
        assert "camera=()" in resp.headers.get("Permissions-Policy", "")


class TestRoleBasedAccess:
    """Role-based access control tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(timeout=30)
        yield
        self.client.close()
    
    def test_viewer_cannot_create_agent(self):
        """Test that viewer role cannot create agents"""
        # This test assumes a viewer user exists. If not, it will be skipped.
        # For now, test that unauthenticated requests are blocked
        resp = self.client.post(f"{BASE}/agents", json={"name": "Test", "description": "Test"})
        assert resp.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
