#!/usr/bin/env python3
"""
Test and validation script for MCP setup.
Verifies that the project is ready for Cursor-native daily file generation.
"""

from pathlib import Path
import json

def check_mcp_config():
    """Check if MCP servers are configured."""
    mcp_config_path = Path.home() / ".cursor" / "mcp.json"
    
    print("🔍 Checking MCP Configuration...")
    print(f"   Config path: {mcp_config_path}")
    
    if not mcp_config_path.exists():
        print("   ❌ MCP config not found")
        return False
    
    try:
        with open(mcp_config_path, 'r') as f:
            config = json.load(f)
        
        servers = config.get('mcpServers', {})
        
        # Check for gworkspace-mcp
        if 'gworkspace-mcp' in servers:
            print("   ✅ gworkspace-mcp configured")
            gw_config = servers['gworkspace-mcp']
            print(f"      Type: {gw_config.get('type')}")
            print(f"      Command: {gw_config.get('command')} {' '.join(gw_config.get('args', []))}")
        else:
            print("   ❌ gworkspace-mcp NOT configured")
        
        # Check for slack-mcp (optional)
        if 'slack-mcp' in servers:
            print("   ✅ slack-mcp configured")
            slack_config = servers['slack-mcp']
            print(f"      Type: {slack_config.get('type')}")
            has_token = bool(slack_config.get('env', {}).get('SLACK_TOKEN'))
            print(f"      Has Token: {has_token}")
        else:
            print("   ⚠️  slack-mcp NOT configured (optional)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error reading config: {e}")
        return False

def check_project_structure():
    """Check if project structure is correct."""
    print("\n🔍 Checking Project Structure...")
    
    # Script is in system/automation/, go up 2 levels to project root
    project_root = Path(__file__).parent.parent.parent
    
    required_paths = {
        'work/daily/': project_root / 'work' / 'daily',
        'work/meetings/': project_root / 'work' / 'meetings',
        'system/templates/daily.md': project_root / 'system' / 'templates' / 'daily.md',
        'system/automation/cursor_generate_daily.py': project_root / 'system' / 'automation' / 'cursor_generate_daily.py',
    }
    
    all_good = True
    for name, path in required_paths.items():
        if path.exists():
            print(f"   ✅ {name}")
        else:
            print(f"   ❌ {name} NOT FOUND")
            all_good = False
    
    return all_good

def check_for_mock_files():
    """Check if old mock files were cleaned up."""
    print("\n🔍 Checking for Redundant Mock Files...")
    
    project_root = Path(__file__).parent
    automation_dir = project_root / 'automation'
    
    mock_files = [
        'mcp_integration.py',
        'real_mcp_integration.py',
        'mcp_calendar_client.py',
        'daily_generator_mcp.py'
    ]
    
    found_mocks = []
    for filename in mock_files:
        filepath = automation_dir / filename
        if filepath.exists():
            found_mocks.append(filename)
            print(f"   ⚠️  Found old mock file: {filename}")
    
    if not found_mocks:
        print("   ✅ All mock files cleaned up")
        return True
    else:
        print(f"   ❌ {len(found_mocks)} old mock files still present")
        return False

def main():
    """Run all validation checks."""
    print("=" * 60)
    print("Task Management System - MCP Setup Validation")
    print("=" * 60)
    
    mcp_ok = check_mcp_config()
    structure_ok = check_project_structure()
    clean_ok = check_for_mock_files()
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    if mcp_ok and structure_ok and clean_ok:
        print("✅ All checks passed!")
        print("\n🚀 Ready to generate daily files!")
        print("\nNext steps:")
        print("1. Ask Claude in Cursor: 'Generate today's daily file'")
        print("2. Claude will call gworkspace-mcp for real calendar events")
        print("3. Your daily file will be created with actual meeting data")
        print("\nSee CURSOR_USAGE_GUIDE.md for more details.")
    else:
        print("⚠️  Some checks failed")
        if not mcp_ok:
            print("   - MCP configuration needs attention")
        if not structure_ok:
            print("   - Project structure incomplete")
        if not clean_ok:
            print("   - Old mock files should be deleted")
    
    print("=" * 60)

if __name__ == "__main__":
    main()


