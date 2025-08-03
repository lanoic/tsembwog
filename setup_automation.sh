
#!/bin/bash

# Set your GitHub username and repository name
GITHUB_USER="lanoic"
REPO_NAME="tsembwog"

# Clone your GitHub repo (replace with your GitHub repo URL)
git clone https://github.com/$GITHUB_USER/$REPO_NAME.git
cd $REPO_NAME

# Unzip local project into repo folder (adjust path if needed)
unzip ../tsembwog.zip -d .
rm -rf __MACOSX

# Add GitHub remote and push
git init
git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git
git add .
git commit -m "Initial commit for tsembwog energy platform"
git push -u origin master
