#!/usr/bin/env python3
"""Setup script for task management automation."""

import os
import sys
from pathlib import Path
import subprocess

def setup_cron_job():
    """Set up cron job for daily file generation."""
    
    project_root = Path(__file__).parent.parent
    script_path = project_root / "automation" / "daily_generator.py"
    python_path = sys.executable
    
    # Create cron job command
    cron_command = f"0 7 * * * cd {project_root} && {python_path} {script_path} >> {project_root}/automation/cron.log 2>&1"
    
    print("To set up daily automation, add the following line to your crontab:")
    print("Run: crontab -e")
    print("Add this line:")
    print(f"  {cron_command}")
    print()
    print("This will run the daily file generator every day at 7:00 AM")
    print("Logs will be written to automation/cron.log")
    
    # Ask if user wants to add it automatically
    try:
        response = input("Would you like to add this cron job automatically? (y/n): ")
        if response.lower() == 'y':
            # Get current crontab
            try:
                current_crontab = subprocess.check_output(['crontab', '-l'], stderr=subprocess.DEVNULL)
                current_crontab = current_crontab.decode('utf-8')
            except subprocess.CalledProcessError:
                current_crontab = ""
            
            # Add our job if it's not already there
            if "daily_generator.py" not in current_crontab:
                new_crontab = current_crontab + "\n" + cron_command + "\n"
                
                # Write new crontab
                process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE)
                process.communicate(input=new_crontab.encode('utf-8'))
                
                if process.returncode == 0:
                    print("✅ Cron job added successfully!")
                else:
                    print("❌ Failed to add cron job")
            else:
                print("ℹ️  Cron job already exists")
                
    except KeyboardInterrupt:
        print("\nSetup cancelled")

def create_config_file():
    """Create configuration file for the automation."""
    
    config_path = Path(__file__).parent / "config.yaml"
    
    config_content = """# Task Management Automation Configuration

calendar:
  primary_calendar: "primary"
  timezone: "America/New_York"
  use_mcp: true
  fallback_to_sample: true

templates:
  daily_template: "system/templates/daily.md"
  meeting_template: "system/templates/meeting-v2.md"

paths:
  daily_dir: "work/daily"
  meetings_dir: "work/meetings"

automation:
  run_time: "07:00"
  check_existing_files: true
  create_meeting_stubs: true

logging:
  level: "INFO"
  file: "automation/automation.log"

# MCP Settings (when available)
mcp:
  server_url: "localhost:3000"  # Adjust as needed
  timeout: 30
"""
    
    if not config_path.exists():
        with open(config_path, 'w') as f:
            f.write(config_content)
        print(f"✅ Created configuration file: {config_path}")
    else:
        print(f"ℹ️  Configuration file already exists: {config_path}")

def install_dependencies():
    """Install required Python dependencies."""
    
    requirements_path = Path(__file__).parent.parent / "requirements.txt"
    
    if requirements_path.exists():
        print("Installing Python dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_path)])
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print(f"Please run manually: pip install -r {requirements_path}")
    else:
        print("❌ requirements.txt not found")

def test_automation():
    """Test the automation system."""
    
    script_path = Path(__file__).parent / "daily_generator.py"
    
    print("Testing automation system...")
    try:
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Automation test successful!")
            print("Check the daily/ folder for the generated file")
        else:
            print("❌ Automation test failed")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            
    except Exception as e:
        print(f"❌ Error running test: {e}")

def main():
    """Main setup function."""
    
    print("=== Task Management Automation Setup ===\n")
    
    # Install dependencies
    install_dependencies()
    print()
    
    # Create config file
    create_config_file()
    print()
    
    # Test the system
    test_automation()
    print()
    
    # Set up cron job
    setup_cron_job()
    print()
    
    print("=== Setup Complete ===")
    print("Your task management automation is ready!")
    print("\nNext steps:")
    print("1. Review the generated daily file in the daily/ folder")
    print("2. Customize automation/config.yaml as needed")
    print("3. Set up Google Workspace MCP integration if desired")
    print("4. The system will run automatically every morning at 7 AM")

if __name__ == "__main__":
    main()

