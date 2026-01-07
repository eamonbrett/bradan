#!/bin/bash
# Quick Push Script for Export Package
# Make executable: chmod +x READY-TO-PUSH.sh

echo "🚀 Task Management System Export - Ready to Push!"
echo ""
echo "Choose your path:"
echo ""
echo "1. Public Template (for sharing with others)"
echo "2. Private Repo (for personal backup/use)"
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" == "1" ]; then
    REPO_NAME="cursor-task-management-template"
    echo ""
    echo "📋 Steps for PUBLIC TEMPLATE:"
    echo ""
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: $REPO_NAME"
    echo "3. Make it PUBLIC"
    echo "4. DON'T initialize with README"
    echo "5. Create repository"
    echo ""
    read -p "Press ENTER when repo is created..."
    
    echo ""
    echo "🔧 Initializing git and pushing..."
    git init
    git add .
    git commit -m "Task management system - ready to share"
    git remote add origin git@github.com:eamonbrett/$REPO_NAME.git
    git push -u origin main
    
    echo ""
    echo "✅ Pushed successfully!"
    echo ""
    echo "📝 Final step:"
    echo "1. Go to https://github.com/eamonbrett/$REPO_NAME/settings"
    echo "2. Check 'Template repository' under Template repository section"
    echo "3. Save"
    echo ""
    echo "🎉 Done! Share this link:"
    echo "https://github.com/eamonbrett/$REPO_NAME"
    echo ""

elif [ "$choice" == "2" ]; then
    REPO_NAME="my-task-management"
    echo ""
    echo "📋 Steps for PRIVATE REPO:"
    echo ""
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: $REPO_NAME"
    echo "3. Make it PRIVATE"
    echo "4. DON'T initialize with README"
    echo "5. Create repository"
    echo ""
    read -p "Press ENTER when repo is created..."
    
    echo ""
    echo "🔧 Initializing git and pushing..."
    git init
    git add .
    git commit -m "Task management system - personal backup"
    git remote add origin git@github.com:eamonbrett/$REPO_NAME.git
    git push -u origin main
    
    echo ""
    echo "✅ Pushed successfully!"
    echo ""
    echo "📝 To use on personal computer:"
    echo "git clone git@github.com:eamonbrett/$REPO_NAME.git"
    echo "cd $REPO_NAME"
    echo "pip install -r requirements.txt"
    echo "# Then follow SETUP_GUIDE.md"
    echo ""

else
    echo "Invalid choice. Run script again."
    exit 1
fi

echo "🎊 All done!"

