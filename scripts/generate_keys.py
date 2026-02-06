#!/usr/bin/env python3
"""
🔒 Neural Chaos Forum - Security Key Generator
===============================================

Generate secure random keys for production deployment.

Usage:
  python scripts/generate_keys.py
  python scripts/generate_keys.py --admin-only
  python scripts/generate_keys.py --flask-only
"""

import secrets
import argparse

def generate_admin_key():
    """Generate a secure admin API key"""
    return f"ncf_admin_{secrets.token_hex(32)}"

def generate_flask_secret():
    """Generate a secure Flask secret key"""
    return secrets.token_hex(32)

def generate_all_keys():
    """Generate all necessary keys"""
    print("🔒 Neural Chaos Forum - Security Key Generator")
    print("=" * 60)
    print()
    
    admin_key = generate_admin_key()
    flask_secret = generate_flask_secret()
    
    print("✅ Generated secure keys:")
    print()
    print("📌 ADMIN_API_KEY (for admin operations):")
    print(f"   {admin_key}")
    print()
    print("📌 SECRET_KEY (for Flask sessions):")
    print(f"   {flask_secret}")
    print()
    print("=" * 60)
    print()
    print("🚀 Next steps:")
    print()
    print("1. Copy these keys to your .env file:")
    print(f"   ADMIN_API_KEY={admin_key}")
    print(f"   SECRET_KEY={flask_secret}")
    print()
    print("2. Or set them in Render.com environment variables:")
    print("   Dashboard → Environment → Add Environment Variable")
    print()
    print("3. Keep these keys SECRET! Never commit them to git.")
    print()
    print("⚠️  WARNING: Save these keys now! They cannot be recovered.")
    print()

def main():
    parser = argparse.ArgumentParser(
        description='Generate secure keys for Neural Chaos Forum',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--admin-only', action='store_true', 
                       help='Generate only admin API key')
    parser.add_argument('--flask-only', action='store_true',
                       help='Generate only Flask secret key')
    
    args = parser.parse_args()
    
    if args.admin_only:
        print("🔑 ADMIN_API_KEY:")
        print(generate_admin_key())
    elif args.flask_only:
        print("🔑 SECRET_KEY:")
        print(generate_flask_secret())
    else:
        generate_all_keys()

if __name__ == '__main__':
    main()
