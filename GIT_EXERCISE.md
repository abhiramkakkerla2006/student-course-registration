# Git exercise record

This repository is intended for the following local demonstration:

```powershell
git init -b main
git add .
git commit -m "Build student course registration app"
git switch -c feature/student-profile
# edit a tracked file, then stage and commit
git add templates/student.html
git commit -m "Improve student profile"
git switch main
git merge --no-ff feature/student-profile -m "Merge student profile feature"
git branch -d feature/student-profile
git log --oneline --graph --decorate --all
```

The full GitHub creation, clone, push, and pull request sequence is in the project README.
