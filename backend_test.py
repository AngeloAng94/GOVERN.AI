#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class GovAITester:
    def __init__(self, base_url="https://audit-first-ai.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}" if not endpoint.startswith('http') else endpoint
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        self.log(f"🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                self.log(f"✅ {name} - Status: {response.status_code}")
                try:
                    return True, response.json() if response.content else {}
                except:
                    return True, {}
            else:
                self.log(f"❌ {name} - Expected {expected_status}, got {response.status_code}")
                try:
                    error_content = response.json() if response.content else response.text
                    self.log(f"    Response: {error_content}")
                except:
                    self.log(f"    Response: {response.text[:200]}")
                self.failed_tests.append(f"{name}: Expected {expected_status}, got {response.status_code}")
                return False, {}

        except Exception as e:
            self.log(f"❌ {name} - Error: {str(e)}")
            self.failed_tests.append(f"{name}: Exception - {str(e)}")
            return False, {}

    def test_dashboard_stats(self):
        """Test GET /api/dashboard/stats returns valid KPIs"""
        success, data = self.run_test(
            "Dashboard Stats", "GET", "dashboard/stats", 200
        )
        if success:
            required_keys = ["agents", "policies", "audit", "compliance_avg"]
            for key in required_keys:
                if key not in data:
                    self.log(f"❌ Dashboard Stats - Missing key: {key}")
                    return False
            self.log(f"    Found KPIs: {list(data.keys())}")
            return True
        return False

    def test_agents_list(self):
        """Test GET /api/agents lists agents with correct enum values"""
        success, data = self.run_test(
            "Agents List", "GET", "agents", 200
        )
        if success and data:
            # Check first agent for enum validation
            agent = data[0] if data else {}
            valid_statuses = ["active", "inactive", "suspended"]
            valid_risks = ["low", "medium", "high", "critical"]
            
            if agent.get("status") not in valid_statuses:
                self.log(f"❌ Invalid agent status: {agent.get('status')}")
                return False
            if agent.get("risk_level") not in valid_risks:
                self.log(f"❌ Invalid agent risk_level: {agent.get('risk_level')}")
                return False
            
            self.log(f"    First agent status: {agent.get('status')}, risk: {agent.get('risk_level')}")
            return True
        return success

    def test_agent_enum_validation(self):
        """Test POST /api/agents with invalid risk_level='banana' returns HTTP 422"""
        invalid_agent = {
            "name": "Test Agent",
            "description": "Test description", 
            "risk_level": "banana"
        }
        success, data = self.run_test(
            "Agent Invalid Enum", "POST", "agents", 422, data=invalid_agent
        )
        return success

    def test_agent_valid_creation(self):
        """Test POST /api/agents with valid enum values creates agent successfully"""
        valid_agent = {
            "name": "Test Valid Agent",
            "description": "Test agent with valid enums",
            "risk_level": "medium", 
            "status": "active"
        }
        success, data = self.run_test(
            "Agent Valid Creation", "POST", "agents", 200, data=valid_agent
        )
        if success:
            self.created_agent_id = data.get("id")
            return True
        return False

    def test_agent_update(self):
        """Test PUT /api/agents/{id} updates agent correctly"""
        if not hasattr(self, 'created_agent_id'):
            self.log("❌ Agent Update - No agent ID from previous test")
            return False
            
        update_data = {
            "name": "Updated Test Agent",
            "description": "Updated description",
            "risk_level": "high",
            "status": "suspended"
        }
        success, data = self.run_test(
            "Agent Update", "PUT", f"agents/{self.created_agent_id}", 200, data=update_data
        )
        return success

    def test_agent_delete(self):
        """Test DELETE /api/agents/{id} deletes agent correctly"""
        if not hasattr(self, 'created_agent_id'):
            self.log("❌ Agent Delete - No agent ID from previous test")
            return False
            
        success, data = self.run_test(
            "Agent Delete", "DELETE", f"agents/{self.created_agent_id}", 200
        )
        return success

    def test_policies_list(self):
        """Test GET /api/policies lists policies with enum-validated fields"""
        success, data = self.run_test(
            "Policies List", "GET", "policies", 200
        )
        if success and data:
            policy = data[0] if data else {}
            valid_severities = ["low", "medium", "high", "critical"]
            valid_enforcements = ["block", "log", "throttle", "auto"]
            
            if policy.get("severity") not in valid_severities:
                self.log(f"❌ Invalid policy severity: {policy.get('severity')}")
                return False
            if policy.get("enforcement") not in valid_enforcements:
                self.log(f"❌ Invalid policy enforcement: {policy.get('enforcement')}")
                return False
                
            self.log(f"    First policy severity: {policy.get('severity')}, enforcement: {policy.get('enforcement')}")
            return True
        return success

    def test_policy_invalid_enum(self):
        """Test POST /api/policies with invalid enforcement='zap' returns HTTP 422"""
        invalid_policy = {
            "name": "Test Policy",
            "description": "Test policy with invalid enum",
            "enforcement": "zap"
        }
        success, data = self.run_test(
            "Policy Invalid Enum", "POST", "policies", 422, data=invalid_policy
        )
        return success

    def test_policy_valid_creation(self):
        """Test POST /api/policies with valid data creates policy successfully"""
        valid_policy = {
            "name": "Test Valid Policy", 
            "description": "Test policy with valid enums",
            "severity": "high",
            "enforcement": "block"
        }
        success, data = self.run_test(
            "Policy Valid Creation", "POST", "policies", 200, data=valid_policy
        )
        if success:
            self.created_policy_id = data.get("id")
            return True
        return False

    def test_audit_regex_safety(self):
        """Test GET /api/audit with regex special chars (.*[]) does NOT crash (regex sanitized)"""
        # Test with dangerous regex patterns
        dangerous_patterns = [".*", ".*[]", "[", "(", ".*.*.*"]
        
        for pattern in dangerous_patterns:
            success, data = self.run_test(
                f"Audit Regex Safety ({pattern})", "GET", "audit", 200, 
                params={"search": pattern}
            )
            if not success:
                return False
        return True

    def test_audit_filters(self):
        """Test GET /api/audit with outcome/risk_level filters works correctly"""
        # Test outcome filter
        success1, data1 = self.run_test(
            "Audit Outcome Filter", "GET", "audit", 200,
            params={"outcome": "allowed", "limit": 10}
        )
        
        # Test risk_level filter
        success2, data2 = self.run_test(
            "Audit Risk Filter", "GET", "audit", 200,
            params={"risk_level": "medium", "limit": 10}
        )
        
        return success1 and success2

    def test_compliance_standards(self):
        """Test GET /api/compliance returns 6 compliance standards"""
        success, data = self.run_test(
            "Compliance Standards", "GET", "compliance", 200
        )
        if success:
            if len(data) != 6:
                self.log(f"❌ Expected 6 compliance standards, got {len(data)}")
                return False
            self.log(f"    Found {len(data)} compliance standards")
            return True
        return False

    def test_chat_functionality(self):
        """Test POST /api/chat sends message and gets AI response (GPT-5.2)"""
        chat_request = {
            "message": "What are the key requirements of the EU AI Act?",
            "session_id": "test_session"
        }
        success, data = self.run_test(
            "Chat Functionality", "POST", "chat", 200, data=chat_request
        )
        if success:
            if "response" not in data:
                self.log("❌ Chat response missing 'response' field")
                return False
            self.log(f"    Chat response length: {len(data.get('response', ''))}")
            return True
        return False

    def run_all_tests(self):
        """Run all backend API tests"""
        self.log("🚀 Starting GOVERN.AI Step 1 Fixes Verification")
        self.log(f"   Testing against: {self.base_url}")
        print("="*60)

        # Test all core functionality
        test_methods = [
            self.test_dashboard_stats,
            self.test_agents_list, 
            self.test_agent_enum_validation,
            self.test_agent_valid_creation,
            self.test_agent_update,
            self.test_agent_delete,
            self.test_policies_list,
            self.test_policy_invalid_enum, 
            self.test_policy_valid_creation,
            self.test_audit_regex_safety,
            self.test_audit_filters,
            self.test_compliance_standards,
            self.test_chat_functionality
        ]

        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.log(f"❌ {test_method.__name__} - Exception: {str(e)}")
                self.failed_tests.append(f"{test_method.__name__}: Exception - {str(e)}")
            print("-" * 60)

        # Print summary
        self.log(f"📊 Tests completed: {self.tests_passed}/{self.tests_run} passed")
        
        if self.failed_tests:
            self.log("❌ Failed tests:")
            for failed in self.failed_tests:
                self.log(f"   • {failed}")
        else:
            self.log("🎉 All tests passed!")

        return self.tests_passed == self.tests_run

def main():
    tester = GovAITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())