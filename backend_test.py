#!/usr/bin/env python3

import requests
import json
import sys
from datetime import datetime
import time

class GovernAIAPITester:
    def __init__(self, base_url="https://audit-first-ai.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        
        print(f"🚀 GOVERN.AI API Testing Suite")
        print(f"📡 Base URL: {self.base_url}")
        print("=" * 60)

    def log_test(self, name, success, response_data=None, error=None):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            self.failed_tests.append({"test": name, "error": str(error)})
            print(f"❌ {name} - {error}")
        
        if response_data and isinstance(response_data, dict):
            if "total" in response_data:
                print(f"   📊 Total records: {response_data.get('total', 'N/A')}")
            elif isinstance(response_data, list):
                print(f"   📊 Records returned: {len(response_data)}")
            elif "id" in response_data:
                print(f"   🆔 Created/Updated ID: {response_data.get('id', 'N/A')}")

    def test_api_endpoint(self, method, endpoint, expected_status=200, data=None, params=None):
        """Generic API test method"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            success = response.status_code == expected_status
            response_data = None
            
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text[:200]}
            
            return success, response_data, response.status_code
            
        except Exception as e:
            return False, None, f"Request failed: {str(e)}"

    def test_dashboard_stats(self):
        """Test dashboard statistics endpoint"""
        print("\n📊 Testing Dashboard Stats API")
        success, data, status = self.test_api_endpoint("GET", "/dashboard/stats")
        
        if success and data:
            # Validate expected fields
            required_fields = ["agents", "policies", "audit", "compliance_avg", "recent_audit", "risk_distribution"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                self.log_test("Dashboard Stats - Structure", False, error=f"Missing fields: {missing_fields}")
            else:
                self.log_test("Dashboard Stats - Structure", True, data)
                
                # Validate nested structure
                if "total" in data.get("agents", {}) and "active" in data.get("agents", {}):
                    self.log_test("Dashboard Stats - Agents Data", True)
                else:
                    self.log_test("Dashboard Stats - Agents Data", False, error="Missing agents total/active")
        else:
            self.log_test("Dashboard Stats", False, error=f"Status: {status}")

    def test_agents_crud(self):
        """Test Agents CRUD operations"""
        print("\n🤖 Testing Agents CRUD API")
        
        # Test GET agents list
        success, agents_data, status = self.test_api_endpoint("GET", "/agents")
        self.log_test("GET /agents", success, agents_data, f"Status: {status}")
        
        if not success:
            return
            
        initial_count = len(agents_data) if isinstance(agents_data, list) else 0
        
        # Test POST - Create new agent
        test_agent = {
            "name": "Test Compliance Bot",
            "description": "Testing agent for CRUD operations",
            "model_type": "GPT-5.2",
            "risk_level": "medium",
            "status": "active",
            "allowed_actions": ["read_policy", "generate_report"],
            "restricted_domains": ["external_api"],
            "data_classification": "internal",
            "owner": "Test Suite"
        }
        
        success, create_data, status = self.test_api_endpoint("POST", "/agents", 200, test_agent)
        self.log_test("POST /agents (Create)", success, create_data, f"Status: {status}")
        
        if not success:
            return
            
        created_id = create_data.get("id") if create_data else None
        
        if created_id:
            # Test GET specific agent
            success, get_data, status = self.test_api_endpoint("GET", f"/agents/{created_id}")
            self.log_test("GET /agents/{id}", success, get_data, f"Status: {status}")
            
            # Test PUT - Update agent
            update_data = test_agent.copy()
            update_data["description"] = "Updated test agent description"
            update_data["risk_level"] = "high"
            
            success, update_response, status = self.test_api_endpoint("PUT", f"/agents/{created_id}", 200, update_data)
            self.log_test("PUT /agents/{id} (Update)", success, update_response, f"Status: {status}")
            
            # Test DELETE agent
            success, delete_data, status = self.test_api_endpoint("DELETE", f"/agents/{created_id}")
            self.log_test("DELETE /agents/{id}", success, delete_data, f"Status: {status}")
            
            # Verify deletion
            success, verify_data, status = self.test_api_endpoint("GET", f"/agents/{created_id}", 404)
            self.log_test("Verify Agent Deletion", success, error=f"Status: {status}" if not success else None)

    def test_policies_crud(self):
        """Test Policies CRUD operations"""
        print("\n📜 Testing Policies CRUD API")
        
        # Test GET policies list
        success, policies_data, status = self.test_api_endpoint("GET", "/policies")
        self.log_test("GET /policies", success, policies_data, f"Status: {status}")
        
        if not success:
            return
        
        # Test POST - Create new policy
        test_policy = {
            "name": "Test Data Access Policy",
            "description": "Testing policy for CRUD operations",
            "rule_type": "restriction",
            "conditions": ["test_condition", "data_access"],
            "actions": ["log_attempt", "block_access"],
            "severity": "high",
            "regulation": "GDPR",
            "enforcement": "block"
        }
        
        success, create_data, status = self.test_api_endpoint("POST", "/policies", 200, test_policy)
        self.log_test("POST /policies (Create)", success, create_data, f"Status: {status}")
        
        if not success:
            return
            
        created_id = create_data.get("id") if create_data else None
        
        if created_id:
            # Test PUT - Update policy
            update_data = test_policy.copy()
            update_data["description"] = "Updated test policy description"
            update_data["severity"] = "critical"
            
            success, update_response, status = self.test_api_endpoint("PUT", f"/policies/{created_id}", 200, update_data)
            self.log_test("PUT /policies/{id} (Update)", success, update_response, f"Status: {status}")
            
            # Test DELETE policy
            success, delete_data, status = self.test_api_endpoint("DELETE", f"/policies/{created_id}")
            self.log_test("DELETE /policies/{id}", success, delete_data, f"Status: {status}")

    def test_audit_trail(self):
        """Test Audit Trail API"""
        print("\n📋 Testing Audit Trail API")
        
        # Test basic audit logs retrieval
        success, audit_data, status = self.test_api_endpoint("GET", "/audit")
        self.log_test("GET /audit (Basic)", success, audit_data, f"Status: {status}")
        
        if not success:
            return
        
        # Test with filters
        filter_params = {
            "outcome": "allowed",
            "limit": 10
        }
        success, filtered_data, status = self.test_api_endpoint("GET", "/audit", params=filter_params)
        self.log_test("GET /audit (Filtered - outcome)", success, filtered_data, f"Status: {status}")
        
        # Test search functionality
        search_params = {
            "search": "agent",
            "limit": 5
        }
        success, search_data, status = self.test_api_endpoint("GET", "/audit", params=search_params)
        self.log_test("GET /audit (Search)", success, search_data, f"Status: {status}")
        
        # Test risk level filter
        risk_params = {
            "risk_level": "high",
            "limit": 10
        }
        success, risk_data, status = self.test_api_endpoint("GET", "/audit", params=risk_params)
        self.log_test("GET /audit (Risk Filter)", success, risk_data, f"Status: {status}")

    def test_compliance_standards(self):
        """Test Compliance Standards API"""
        print("\n🛡️ Testing Compliance Standards API")
        
        success, compliance_data, status = self.test_api_endpoint("GET", "/compliance")
        self.log_test("GET /compliance", success, compliance_data, f"Status: {status}")
        
        if success and compliance_data and isinstance(compliance_data, list):
            # Check if we have expected compliance standards
            expected_standards = ["GDPR", "EU-AI-ACT", "ISO-27001", "ISO-42001", "DORA", "NIS2"]
            found_codes = [std.get("code", "") for std in compliance_data]
            
            missing_standards = [std for std in expected_standards if std not in found_codes]
            if missing_standards:
                self.log_test("Compliance Standards - Coverage", False, error=f"Missing: {missing_standards}")
            else:
                self.log_test("Compliance Standards - Coverage", True)
                
            # Test update functionality on first standard if available
            if compliance_data:
                first_standard = compliance_data[0]
                standard_id = first_standard.get("id")
                
                if standard_id:
                    update_data = {
                        "progress": 85,
                        "requirements_met": 30,
                        "status": "in_progress"
                    }
                    success, update_result, status = self.test_api_endpoint("PUT", f"/compliance/{standard_id}", 200, update_data)
                    self.log_test("PUT /compliance/{id} (Update)", success, update_result, f"Status: {status}")

    def test_ai_chat(self):
        """Test AI Chat Assistant API"""
        print("\n🤖 Testing AI Chat Assistant API")
        
        # Test simple chat message
        chat_request = {
            "message": "What are the key requirements of GDPR for AI systems?",
            "session_id": f"test_session_{int(time.time())}"
        }
        
        success, chat_response, status = self.test_api_endpoint("POST", "/chat", 200, chat_request)
        self.log_test("POST /chat (GDPR Query)", success, chat_response, f"Status: {status}")
        
        if success and chat_response:
            response_text = chat_response.get("response", "")
            if len(response_text) > 50:  # Basic check for meaningful response
                self.log_test("AI Chat - Response Quality", True)
                print(f"   💬 Response preview: {response_text[:100]}...")
            else:
                self.log_test("AI Chat - Response Quality", False, error="Response too short or empty")
        
        # Test Italian language query
        italian_chat_request = {
            "message": "Quali sono i principali obblighi dell'AI Act europeo?",
            "session_id": f"test_session_it_{int(time.time())}"
        }
        
        success, italian_response, status = self.test_api_endpoint("POST", "/chat", 200, italian_chat_request)
        self.log_test("POST /chat (Italian Query)", success, italian_response, f"Status: {status}")

    def test_root_endpoint(self):
        """Test root API endpoint"""
        print("\n🏠 Testing Root API Endpoint")
        
        success, root_data, status = self.test_api_endpoint("GET", "/")
        self.log_test("GET / (Root)", success, root_data, f"Status: {status}")

    def run_all_tests(self):
        """Run all API tests"""
        print(f"🧪 Starting GOVERN.AI API Test Suite at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all test methods
        self.test_root_endpoint()
        self.test_dashboard_stats()
        self.test_agents_crud()
        self.test_policies_crud()
        self.test_audit_trail()
        self.test_compliance_standards()
        self.test_ai_chat()
        
        # Print summary
        print("\n" + "=" * 60)
        print("🏁 Test Suite Completed")
        print(f"📊 Tests Run: {self.tests_run}")
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {len(self.failed_tests)}")
        
        if self.failed_tests:
            print("\n🔍 Failed Tests Details:")
            for failure in self.failed_tests:
                print(f"   • {failure['test']}: {failure['error']}")
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    tester = GovernAIAPITester()
    
    try:
        all_passed = tester.run_all_tests()
        return 0 if all_passed else 1
    except KeyboardInterrupt:
        print("\n⚠️ Test suite interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Test suite failed with error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())