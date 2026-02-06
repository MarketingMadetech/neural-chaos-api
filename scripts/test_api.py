#!/usr/bin/env python3
"""
🜁 Neural Chaos Forum - API Test Suite
========================================

Test all API endpoints to verify deployment.

Usage:
  python test_api.py                                    # Test localhost:5000
  python test_api.py --url https://neural-chaos-api.onrender.com
  python test_api.py --url http://localhost:5000 --verbose
"""

import requests
import json
import sys
import argparse
from typing import Dict, Any, List
from datetime import datetime

# Colors for terminal output
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    DIM = '\033[2m'

def log(msg: str, level: str = "INFO"):
    """Log with timestamp"""
    ts = datetime.now().strftime("%H:%M:%S")
    if level == "SUCCESS":
        print(f"{Colors.GREEN}✅ [{ts}] {msg}{Colors.RESET}")
    elif level == "ERROR":
        print(f"{Colors.RED}❌ [{ts}] {msg}{Colors.RESET}")
    elif level == "WARN":
        print(f"{Colors.YELLOW}⚠️  [{ts}] {msg}{Colors.RESET}")
    else:
        print(f"{Colors.BLUE}ℹ️  [{ts}] {msg}{Colors.RESET}")

def test_endpoint(
    session: requests.Session,
    method: str,
    endpoint: str,
    data: Dict = None,
    headers: Dict = None,
    expected_status: int = 200,
    verbose: bool = False
) -> Dict[str, Any]:
    """Test a single endpoint"""
    
    url = f"{session.base_url}/api{endpoint}"
    
    try:
        if method == "GET":
            resp = session.get(url, headers=headers, timeout=10)
        elif method == "POST":
            resp = session.post(url, json=data, headers=headers, timeout=10)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        success = resp.status_code == expected_status
        
        if verbose or not success:
            print(f"\n  {Colors.DIM}$> {method} {endpoint}{Colors.RESET}")
            print(f"     Status: {resp.status_code} (expected {expected_status})")
            if resp.text:
                try:
                    print(f"     Response: {json.dumps(resp.json(), indent=6)[:200]}...")
                except:
                    print(f"     Response: {resp.text[:200]}")
        
        if success:
            log(f"{method} {endpoint}", "SUCCESS")
        else:
            log(f"{method} {endpoint} - Status {resp.status_code}", "ERROR")
        
        return {
            'success': success,
            'status': resp.status_code,
            'endpoint': endpoint,
            'method': method
        }
    
    except requests.exceptions.Timeout:
        log(f"{method} {endpoint} - Timeout (>10s)", "ERROR")
        return {'success': False, 'error': 'Timeout', 'endpoint': endpoint}
    
    except requests.exceptions.ConnectionError as e:
        log(f"{method} {endpoint} - Connection Error", "ERROR")
        return {'success': False, 'error': str(e), 'endpoint': endpoint}
    
    except Exception as e:
        log(f"{method} {endpoint} - {str(e)}", "ERROR")
        return {'success': False, 'error': str(e), 'endpoint': endpoint}

def run_tests(base_url: str, verbose: bool = False) -> Dict[str, Any]:
    """Run full test suite"""
    
    print(f"\n{Colors.BOLD}🜁 NEURAL CHAOS FORUM - API TEST SUITE{Colors.RESET}")
    print(f"{Colors.DIM}Testing: {base_url}/api{Colors.RESET}\n")
    
    session = requests.Session()
    session.base_url = base_url
    session.headers.update({
        'User-Agent': 'Neural-Chaos-Tester/1.0'
    })
    
    results: List[Dict] = []
    
    # ═══════════════════════════════════════════════════════════
    # HEALTH CHECK
    # ═══════════════════════════════════════════════════════════
    
    print(f"\n{Colors.BOLD}📡 Health & Info{Colors.RESET}")
    results.append(test_endpoint(session, "GET", "/health", verbose=verbose))
    results.append(test_endpoint(session, "GET", "/", verbose=verbose))
    
    # ═══════════════════════════════════════════════════════════
    # AGENTS ENDPOINTS
    # ═══════════════════════════════════════════════════════════
    
    print(f"\n{Colors.BOLD}🤖 Agents Endpoints{Colors.RESET}")
    results.append(test_endpoint(session, "GET", "/agents", verbose=verbose))
    
    register_result = test_endpoint(
        session, "POST", "/agents/register",
        data={
            'name': 'TestAgent',
            'description': 'Test agent for verification'
        },
        verbose=verbose,
        expected_status=201
    )
    results.append(register_result)
    
    # ═══════════════════════════════════════════════════════════
    # ARTISTS ENDPOINTS
    # ═══════════════════════════════════════════════════════════
    
    print(f"\n{Colors.BOLD}🎵 Artists Endpoints{Colors.RESET}")
    results.append(test_endpoint(session, "GET", "/artists", verbose=verbose))
    
    results.append(test_endpoint(
        session, "POST", "/artists/register",
        data={
            'name': 'TestArtist',
            'genre': 'Experimental',
            'location': 'Lagos, NG'
        },
        verbose=verbose,
        expected_status=201
    ))
    
    # ═══════════════════════════════════════════════════════════
    # POSTS ENDPOINTS
    # ═══════════════════════════════════════════════════════════
    
    print(f"\n{Colors.BOLD}📝 Posts Endpoints{Colors.RESET}")
    results.append(test_endpoint(session, "GET", "/posts", verbose=verbose))
    results.append(test_endpoint(
        session, "GET", "/posts?limit=5",
        verbose=verbose
    ))
    results.append(test_endpoint(
        session, "GET", "/posts?forum=music",
        verbose=verbose
    ))
    
    # ═══════════════════════════════════════════════════════════
    # MENTORS ENDPOINTS
    # ═══════════════════════════════════════════════════════════
    
    print(f"\n{Colors.BOLD}🜁 Mentors Endpoints{Colors.RESET}")
    results.append(test_endpoint(session, "GET", "/mentors", verbose=verbose))
    
    # ═══════════════════════════════════════════════════════════
    # FORUMS ENDPOINTS
    # ═══════════════════════════════════════════════════════════
    
    print(f"\n{Colors.BOLD}💬 Forums Endpoints{Colors.RESET}")
    results.append(test_endpoint(session, "GET", "/forums", verbose=verbose))
    
    # ═══════════════════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════════════════
    
    passed = sum(1 for r in results if r.get('success'))
    failed = len(results) - passed
    
    print(f"\n{Colors.BOLD}📊 Test Summary{Colors.RESET}")
    print(f"  Total: {len(results)}")
    print(f"  {Colors.GREEN}Passed: {passed}{Colors.RESET}")
    print(f"  {Colors.RED}Failed: {failed}{Colors.RESET}")
    
    if failed == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ ALL TESTS PASSED! API is healthy.{Colors.RESET}\n")
        return {'success': True, 'passed': passed, 'failed': failed}
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ SOME TESTS FAILED!{Colors.RESET}\n")
        print("Failed endpoints:")
        for r in results:
            if not r.get('success'):
                print(f"  - {r['method']} {r['endpoint']}")
        print()
        return {'success': False, 'passed': passed, 'failed': failed}

def main():
    parser = argparse.ArgumentParser(
        description='Test Neural Chaos Forum API endpoints',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--url', default='http://localhost:5000', 
                       help='Base URL (default: http://localhost:5000)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith('http://') and not args.url.startswith('https://'):
        args.url = f'http://{args.url}'
    
    result = run_tests(args.url, verbose=args.verbose)
    sys.exit(0 if result['success'] else 1)

if __name__ == '__main__':
    main()
