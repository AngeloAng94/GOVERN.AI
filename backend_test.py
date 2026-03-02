#!/usr/bin/env python3
"""
GOVERN.AI Step 2A Backend API Testing Suite
Tests JWT Authentication, RBAC, Rate Limiting, and ARIA Assistant
"""
import requests
import sys
import json
import time
from datetime import datetime

class GovernAITester:
    def __init__(self, base_url="https://audit-first-ai.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.user = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.session = requests.Session()
        
    def log(self, message):
        """Log with timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        if headers:
            test_headers.update(headers)

        self.tests_run += 1
        self.log(f"🔍 Test {self.tests_run}: {name}")
        
        try:
            if method == 'GET':
                response = self.session.get(url, headers=test_headers, params=params)
            elif method == 'POST':
                response = self.session.post(url, json=data, headers=test_headers)
            elif method == 'PUT':
                response = self.session.put(url, json=data, headers=test_headers)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=test_headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                self.log(f"✅ PASS - Status: {response.status_code}")
                try:
                    return True, response.json() if response.text else {}
                except:
                    return True, {}
            else:
                self.log(f"❌ FAIL - Expected {expected_status}, got {response.status_code}")
                try:
                    error_detail = response.json().get('detail', 'No detail')
                except:
                    error_detail = response.text
                self.log(f"   Response: {error_detail}")
                self.failed_tests.append({
                    "test": name,
                    "expected": expected_status,
                    "actual": response.status_code,
                    "error": error_detail
                })
                return False, {}

        except Exception as e:
            self.log(f"❌ FAIL - Exception: {str(e)}")
            self.failed_tests.append({
                "test": name,
                "error": str(e)
            })
            return False, {}

    def test_auth_flow(self):
        """Test authentication endpoints"""
        self.log("\n🔐 === AUTHENTICATION TESTS ===")
        
        # Test login with correct admin credentials
        success, response = self.run_test(
            "Login with admin credentials",
            "POST",
            "auth/login",
            200,
            data={"username": "admin", "password": "AdminGovern2026!"}
        )
        
        if success and 'token' in response and 'user' in response:
            self.token = response['token']
            self.user = response['user']
            self.log(f"   Token acquired for user: {self.user.get('username')} (role: {self.user.get('role')})")
        else:
            self.log("❌ CRITICAL: Cannot proceed without valid token")
            return False
            
        # Test login with wrong password
        self.run_test(
            "Login with wrong password",
            "POST", 
            "auth/login",
            401,
            data={"username": "admin", "password": "wrongpassword"}
        )
        
        # Test /auth/me with valid token
        self.run_test(
            "GET /auth/me with valid token",
            "GET",
            "auth/me", 
            200
        )
        
        return True

    def test_dashboard_endpoints(self):
        """Test dashboard and protected endpoints"""
        self.log("\n📊 === DASHBOARD & RBAC TESTS ===")
        
        # Test dashboard without token
        old_token = self.token
        self.token = None
        self.run_test(
            "GET /dashboard/stats without token",
            "GET",
            "dashboard/stats",
            401
        )
        self.token = old_token
        
        # Test dashboard with admin token
        self.run_test(
            "GET /dashboard/stats with admin token",
            "GET", 
            "dashboard/stats",
            200
        )

    def test_agents_crud(self):
        """Test agents CRUD operations"""
        self.log("\n🤖 === AGENTS CRUD TESTS ===")
        
        # List agents (admin has access)
        self.run_test(
            "GET /agents with admin token",
            "GET",
            "agents",
            200
        )
        
        # Create agent (admin has dpo+ permission)
        agent_data = {
            "name": "Test Agent",
            "description": "Test agent for API testing", 
            "model_type": "GPT-5.2",
            "risk_level": "medium",
            "status": "active",
            "allowed_actions": ["test_action"],
            "restricted_domains": [],
            "data_classification": "internal",
            "owner": "Test Suite"
        }
        
        success, response = self.run_test(
            "POST /agents with admin token", 
            "POST",
            "agents",
            201,
            data=agent_data
        )
        
        created_agent_id = response.get('id') if success else None
        
        # Test invalid enum value
        invalid_agent_data = agent_data.copy()
        invalid_agent_data['risk_level'] = 'banana'
        
        self.run_test(
            "POST /agents with invalid risk_level 'banana'",
            "POST",
            "agents", 
            422,
            data=invalid_agent_data
        )
        
        # Delete agent (admin only)
        if created_agent_id:
            self.run_test(
                "DELETE /agents/{id} with admin token",
                "DELETE",
                f"agents/{created_agent_id}",
                200
            )

    def test_policies_endpoint(self):
        """Test policies endpoint"""
        self.log("\n📋 === POLICIES TESTS ===")
        
        self.run_test(
            "GET /policies with token",
            "GET",
            "policies",
            200
        )

    def test_audit_endpoint(self):
        """Test audit trail endpoint"""
        self.log("\n🔍 === AUDIT TRAIL TESTS ===")
        
        self.run_test(
            "GET /audit with token",
            "GET", 
            "audit",
            200
        )

    def test_compliance_endpoint(self):
        """Test compliance standards endpoint"""
        self.log("\n✅ === COMPLIANCE TESTS ===")
        
        success, response = self.run_test(
            "GET /compliance with token",
            "GET",
            "compliance", 
            200
        )
        
        # Verify 6 compliance standards are returned
        if success and isinstance(response, list):
            if len(response) == 6:
                self.log(f"   ✅ Compliance standards count: {len(response)}")
            else:
                self.log(f"   ⚠️ Expected 6 compliance standards, got {len(response)}")

    def test_aria_chat(self):
        """Test ARIA AI assistant chat"""
        self.log("\n💬 === ARIA CHAT TESTS ===")
        
        # Test message too short
        self.run_test(
            "POST /chat with message < 5 chars",
            "POST",
            "chat",
            400,
            data={"message": "hi", "session_id": "test"}
        )
        
        # Test message too long
        long_message = "x" * 2001
        self.run_test(
            "POST /chat with message > 2000 chars", 
            "POST",
            "chat",
            400,
            data={"message": long_message, "session_id": "test"}
        )
        
        # Test valid compliance question
        compliance_msg = "What are the key requirements of the EU AI Act for high-risk systems?"
        success, response = self.run_test(
            "POST /chat with valid compliance question",
            "POST", 
            "chat",
            200,
            data={"message": compliance_msg, "session_id": "test_session"}
        )
        
        if success:
            self.log(f"   ARIA response preview: {response.get('response', '')[:100]}...")

    def test_rate_limiting(self):
        """Test rate limiting (basic check)"""
        self.log("\n🚦 === RATE LIMITING TESTS ===")
        
        # Quick test of chat rate limit (10/min)
        self.log("Testing chat rate limit...")
        for i in range(3):
            success, _ = self.run_test(
                f"Rate limit test {i+1}/3",
                "POST",
                "chat", 
                200,
                data={"message": f"Rate test {i+1}", "session_id": "rate_test"}
            )
            if not success:
                break
            time.sleep(1)

    def run_all_tests(self):
        """Run the complete test suite"""
        self.log("🚀 Starting GOVERN.AI Step 2A API Test Suite")
        self.log(f"Base URL: {self.base_url}")
        
        start_time = datetime.now()
        
        # Run test modules
        if not self.test_auth_flow():
            self.log("❌ CRITICAL: Authentication failed, stopping tests")
            return False
            
        self.test_dashboard_endpoints()
        self.test_agents_crud()
        self.test_policies_endpoint()
        self.test_audit_endpoint() 
        self.test_compliance_endpoint()
        self.test_aria_chat()
        self.test_rate_limiting()
        
        # Results summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        self.log(f"\n📊 === TEST RESULTS ===")
        self.log(f"Tests completed in {duration:.1f}s")
        self.log(f"Passed: {self.tests_passed}/{self.tests_run}")
        self.log(f"Failed: {len(self.failed_tests)}")
        
        if self.failed_tests:
            self.log(f"\n❌ FAILED TESTS:")
            for fail in self.failed_tests:
                self.log(f"  - {fail['test']}: {fail.get('error', 'Status code mismatch')}")
        
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        self.log(f"\nSuccess rate: {success_rate:.1f}%")
        
        return success_rate >= 80

def main():
    """Main test execution"""
    tester = GovernAITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())