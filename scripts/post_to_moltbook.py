"""
Post NINA's replies to Moltbook
================================
Reads nina_replies_music_discovery.json and posts each reply as a comment
on the original music discovery thread.

Usage: python post_to_moltbook.py
"""

import json
import os
from datetime import datetime

# Load NINA's replies
REPLIES_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'nina_replies_music_discovery.json')

def load_replies():
    with open(REPLIES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_reply_for_moltbook(reply):
    """Format a reply for posting to Moltbook"""
    
    # Header
    output = f"@{reply['to']}\n\n"
    
    # Main content
    output += reply['reply'] + "\n\n"
    
    # Action items if present
    if 'action_items' in reply and reply['action_items']:
        output += "**Action Items:**\n"
        for item in reply['action_items']:
            output += f"- {item}\n"
    
    return output

def generate_moltbook_post():
    """Generate formatted responses for manual posting"""
    
    replies = load_replies()
    
    output = "# NINA's Responses to Music Discovery Debate\n\n"
    output += f"Generated: {datetime.utcnow().isoformat()}\n"
    output += f"Total Replies: {len(replies)}\n\n"
    output += "---\n\n"
    
    for i, reply in enumerate(replies, 1):
        output += f"## Reply {i}/{len(replies)}\n\n"
        output += format_reply_for_moltbook(reply)
        output += "\n---\n\n"
    
    return output

def export_individual_replies():
    """Export each reply as a separate file for easy copy-paste"""
    
    replies = load_replies()
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'moltbook_replies')
    os.makedirs(output_dir, exist_ok=True)
    
    for i, reply in enumerate(replies, 1):
        filename = f"{i:02d}_reply_to_{reply['to']}.txt"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(format_reply_for_moltbook(reply))
        
        print(f"✓ Exported: {filename}")
    
    print(f"\n✅ {len(replies)} replies exported to: {output_dir}")

def main():
    """Main execution"""
    print("🔥 Neural Chaos Forum → Moltbook Replies\n")
    
    # Generate combined post
    combined = generate_moltbook_post()
    output_file = os.path.join(os.path.dirname(__file__), '..', 'MOLTBOOK_REPLIES.txt')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(combined)
    
    print(f"✓ Combined post saved: {output_file}\n")
    
    # Export individual replies
    export_individual_replies()
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. Go to Moltbook: m/music thread")
    print("2. Copy individual replies from moltbook_replies/ folder")
    print("3. Paste as comments, tagging each agent")
    print("4. Or post combined version as new thread")
    print("="*60)

if __name__ == '__main__':
    main()
