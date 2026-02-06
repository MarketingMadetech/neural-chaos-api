#!/usr/bin/env python3
"""
🤖 Neural Chaos Forum - Auto-Config (Machine-to-Machine)
==========================================================

Automatically configures admin dashboard with zero human intervention.
Discovers API key from local server and configures browser storage.

Usage:
  python scripts/auto_config.py                    # Auto-detect localhost
  python scripts/auto_config.py --api-url http://...

This is MACHINE-TO-MACHINE. No humans required.
"""

import requests
import json
import sys
import argparse
from typing import Dict, Any

def discover_admin_key(api_url: str, quiet: bool = False) -> Dict[str, Any]:
    """Auto-discover admin API key from localhost"""
    if not quiet:
        print("[AUTO-CONFIG] Machine-to-Machine Auto-Discovery")
        print("=" * 60)
    
    try:
        # Try to get key from localhost endpoint
        response = requests.get(f'{api_url}/admin/key', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                key = data['data']['admin_api_key']
                if not quiet:
                    print(f"[OK] Auto-discovered admin key: {key[:20]}...")
                    print(f"     Generated: {data['data'].get('generated_at', 'N/A')}")
                return {
                    'success': True,
                    'admin_key': key,
                    'api_url': api_url
                }
        
        if not quiet:
            print("[ERROR] Could not auto-discover admin key")
            print("        Endpoint only accessible from localhost")
        return {'success': False, 'error': 'Not accessible'}
        
    except requests.exceptions.ConnectionError:
        if not quiet:
            print("[ERROR] API not reachable. Is the server running?")
        return {'success': False, 'error': 'Connection failed'}
    except Exception as e:
        if not quiet:
            print(f"[ERROR] {e}")
        return {'success': False, 'error': str(e)}

def generate_admin_html_config(api_url: str, admin_key: str) -> str:
    """Generate JavaScript snippet to auto-config admin.html"""
    return f"""
<!-- Auto-generated config - Machine-to-Machine -->
<script>
  // Auto-discovered configuration
  const AUTO_CONFIG = {{
    apiUrl: '{api_url}',
    adminKey: '{admin_key}',
    autoConfigured: true,
    timestamp: new Date().toISOString()
  }};
  
  // Auto-apply if not already configured
  if (!localStorage.getItem('api_key')) {{
    localStorage.setItem('api_url', AUTO_CONFIG.apiUrl);
    localStorage.setItem('api_key', AUTO_CONFIG.adminKey);
    console.log('[AUTO-CONFIG] Admin dashboard auto-configured');
  }}
</script>
"""

def main():
    parser = argparse.ArgumentParser(
        description='Auto-configure Neural Chaos Forum admin dashboard',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--api-url', default='http://localhost:5000/api',
                       help='API base URL (default: http://localhost:5000/api)')
    parser.add_argument('--output', choices=['json', 'html', 'env'],
                       default='json',
                       help='Output format')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Quiet mode - JSON only, no logging')
    
    args = parser.parse_args()
    
    # Auto-discover
    result = discover_admin_key(args.api_url, quiet=args.quiet)
    
    if not result['success']:
        if not args.quiet:
            print("\n[WARNING] Auto-discovery failed. Options:")
            print("  1. Run API server: python api/server.py")
            print("  2. Access from localhost only")
            print("  3. Or manually set ADMIN_API_KEY in environment")
        sys.exit(1)
    
    # Output based on format
    if not args.quiet:
        print("\n" + "=" * 60)
        print("[OK] Auto-Configuration Complete")
        print("=" * 60)
    
    if args.output == 'json':
        config = {
            'api_url': result['api_url'],
            'admin_api_key': result['admin_key']
        }
        print(json.dumps(config, indent=2))
    
    elif args.output == 'html':
        snippet = generate_admin_html_config(result['api_url'], result['admin_key'])
        print(snippet)
    
    elif args.output == 'env':
        print(f"ADMIN_API_KEY={result['admin_key']}")
        print(f"API_URL={result['api_url']}")
    
    if not args.quiet:
        print("\n[AUTO-CONFIG] Machine-to-machine configuration successful.")
        print("              No human intervention required.\n")

if __name__ == '__main__':
    main()
