#!/usr/bin/env python3
"""
🜁 Neural Chaos Forum - Post NINA Replies to Moltbook
======================================================

Posts NINA's 10 replies from nina_replies_music_discovery.json
as comments on the music discovery debate thread.

Usage:
  python post_replies_moltbook.py                    # Post all 10 replies
  python post_replies_moltbook.py --dry-run          # Test without posting
  python post_replies_moltbook.py --limit 3          # Post only first 3 replies
"""

import json
import os
import sys
import argparse
import requests
import time
from datetime import datetime
from typing import List, Dict, Any

# Moltbook Configuration
MOLTBOOK_API_KEY = "moltbook_sk_JozR-ciKrRA5u5lS3a1Jj8PnUYluQFcX"
MOLTBOOK_POST_ID = "0c96c8da-84a7-48c9-978a-3af8bc9c5a77"  # Music discovery debate post
MOLTBOOK_API_URL = "https://www.moltbook.com/api/v1"

# File paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPLIES_FILE = os.path.join(os.path.dirname(SCRIPT_DIR), 'data', 'nina_replies_music_discovery.json')

# Rate limiting (Moltbook: 1 post per 30 minutes - but comments might be less restrictive)
# Starting conservatively with 5 seconds between comments
DELAY_BETWEEN_COMMENTS = 5  # seconds


def log(message: str, level: str = "INFO") -> None:
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


def load_replies() -> List[Dict[str, Any]]:
    """Load NINA's replies from JSON file"""
    try:
        with open(REPLIES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # JSON file is a direct array, not an object with 'replies' key
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        log(f"❌ Replies file not found: {REPLIES_FILE}", "ERROR")
        sys.exit(1)
    except json.JSONDecodeError as e:
        log(f"❌ Invalid JSON in replies file: {e}", "ERROR")
        sys.exit(1)


def format_comment(reply: Dict[str, Any]) -> str:
    """Format reply as Moltbook comment"""
    recipient = reply.get('to', '')
    content = reply.get('reply', '')
    action_items = reply.get('action_items', [])
    
    # Build comment text
    comment = f"@{recipient}\n\n{content}"
    
    # Add action items if present
    if action_items:
        comment += "\n\nAction items:\n"
        for item in action_items:
            comment += f"• {item}\n"
    
    return comment.strip()


def post_comment(comment: str, dry_run: bool = False) -> Dict[str, Any]:
    """Post comment to Moltbook"""
    if dry_run:
        log("🧪 DRY RUN: Would post this comment:", "INFO")
        print(f"\n{'-'*60}")
        print(comment)
        print(f"{'-'*60}\n")
        return {"success": True, "dry_run": True}
    
    try:
        headers = {
            'X-API-Key': MOLTBOOK_API_KEY,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'content': comment
        }
        
        url = f"{MOLTBOOK_API_URL}/posts/{MOLTBOOK_POST_ID}/comments"
        
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            log("✅ Comment posted successfully!", "SUCCESS")
            return {"success": True, "response": response.json()}
        else:
            log(f"❌ Failed to post comment. Status: {response.status_code}", "ERROR")
            log(f"Response: {response.text}", "ERROR")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": response.text
            }
            
    except requests.exceptions.RequestException as e:
        log(f"❌ Network error: {e}", "ERROR")
        return {"success": False, "error": str(e)}
    except Exception as e:
        log(f"❌ Unexpected error: {e}", "ERROR")
        return {"success": False, "error": str(e)}


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Post NINA replies as Moltbook comments',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--dry-run', action='store_true', help='Test without actually posting')
    parser.add_argument('--limit', type=int, help='Post only first N replies (for testing)')
    parser.add_argument('--delay', type=int, default=DELAY_BETWEEN_COMMENTS, 
                       help=f'Seconds to wait between comments (default: {DELAY_BETWEEN_COMMENTS})')
    
    args = parser.parse_args()
    
    log("🜁 Neural Chaos Forum - Moltbook Reply Poster", "INFO")
    log(f"Post ID: {MOLTBOOK_POST_ID}", "INFO")
    
    if args.dry_run:
        log("🧪 DRY RUN MODE - No comments will be posted", "WARN")
    
    # Load replies
    log("Loading replies...", "INFO")
    replies = load_replies()
    
    if not replies:
        log("❌ No replies found in file", "ERROR")
        sys.exit(1)
    
    # Apply limit if set
    if args.limit:
        replies = replies[:args.limit]
        log(f"Limiting to first {args.limit} replies", "INFO")
    
    log(f"Found {len(replies)} replies to post", "INFO")
    
    # Post each reply
    results = {
        "success": [],
        "failed": []
    }
    
    for i, reply in enumerate(replies, 1):
        recipient = reply.get('to', 'unknown')
        log(f"\n[{i}/{len(replies)}] Posting reply to @{recipient}...", "INFO")
        
        # Format and post comment
        comment = format_comment(reply)
        result = post_comment(comment, dry_run=args.dry_run)
        
        if result.get('success'):
            results["success"].append(recipient)
        else:
            results["failed"].append(recipient)
        
        # Wait between comments (except after last one)
        if i < len(replies) and not args.dry_run:
            log(f"Waiting {args.delay} seconds before next comment...", "INFO")
            time.sleep(args.delay)
    
    # Summary
    log("\n" + "="*60, "INFO")
    log("📊 POSTING SUMMARY", "INFO")
    log("="*60, "INFO")
    log(f"✅ Successfully posted: {len(results['success'])}", "SUCCESS")
    log(f"❌ Failed to post: {len(results['failed'])}", "ERROR" if results['failed'] else "INFO")
    
    if results['success']:
        log(f"\nSuccess: {', '.join(results['success'])}", "SUCCESS")
    
    if results['failed']:
        log(f"\nFailed: {', '.join(results['failed'])}", "ERROR")
    
    log("="*60 + "\n", "INFO")
    
    # Exit with appropriate code
    sys.exit(0 if not results['failed'] else 1)


if __name__ == '__main__':
    main()
