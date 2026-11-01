<<<<<<< HEAD
# CampusDesk — Student Information & Course Registration

A small Flask + SQLite application for managing student records and registering students in courses. It is designed as a learning project for Git and GitHub workflows.

## Features

- Add students with name, email, and program; reject duplicate emails.
- Add courses with a unique code, title, and seat capacity.
- Register a student for a course; prevent duplicate registrations and full-course enrollment.
- View a student profile and their registered courses.
- Responsive dashboard with student, course, and registration counts.
- SQLite database is created automatically and excluded from Git.

## Run locally

Requires Python 3.10 or later and Git.

```powershell
cd student-course-registration
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py app.py
```

Open <http://127.0.0.1:5000>. The three sample courses are inserted on first start. Student records are created from the dashboard. To use a different database path, set `STUDENT_DB`; set `FLASK_SECRET_KEY` to a random value for deployment. `FLASK_DEBUG=1` enables Flask's development debugger and should only be used on a trusted local machine.

## Git workflow: initialize, track, stage, and commit

Run these from the project directory if you are starting from an untracked copy:

```powershell
git init -b main
git status
git add .
git status
git commit -m "Build student course registration app"
git log --oneline --decorate
```

`git status` before and after `git add` shows which files are untracked and staged. `.gitignore` keeps the local database, environment, and Python cache out of commits.

## (a) Branch, switch, merge, and delete

```powershell
git switch -c feature/student-profile
git status
# Make a change, for example improve templates/student.html
git add templates/student.html
git commit -m "Improve student profile"
git switch main
git merge --no-ff feature/student-profile -m "Merge student profile feature"
git branch -d feature/student-profile
git branch --list
git log --oneline --graph --decorate --all
```

If Git reports a merge conflict, edit the marked file, remove the conflict markers, then `git add <file>` and `git commit` to finish the merge. Do not delete a branch until its changes are merged; `-d` refuses to remove an unmerged branch. For an intentionally abandoned branch, use `git branch -D <branch>` only after confirming its commits are no longer needed.

## (b) Create a GitHub repository, clone it, and push

Install and authenticate GitHub CLI (`gh auth login`) or create an **empty** repository in GitHub in your browser. For a new private repository named `student-course-registration`, create it and push this local project with:

```powershell
gh repo create student-course-registration --private --source . --remote origin --push
```

That command creates the GitHub remote, names it `origin`, and pushes the current branch. If you created the empty repository in the browser instead, connect and push explicitly (replace `YOUR-USER`):

```powershell
git remote add origin https://github.com/YOUR-USER/student-course-registration.git
git remote -v
git push -u origin main
```

Clone to a second local directory, make a change there, and push it:

```powershell
cd ..
git clone https://github.com/YOUR-USER/student-course-registration.git student-course-registration-copy
cd student-course-registration-copy
# Edit a project file
git status
git add README.md
git commit -m "Document project setup"
git push
```

To bring the clone up to date in the original directory, use `git pull --rebase origin main`. HTTPS pushes use GitHub's browser/device sign-in or a credential manager; do not put a password or token in the remote URL.

## (c) Collaborative GitHub workflow

1. Each contributor clones the repository and creates a focused branch: `git switch -c feature/course-search`.
2. Contributors edit, review with `git diff`, stage only the intended files (`git add ...`), and commit (`git commit -m "Add course search"`).
3. Push the branch: `git push -u origin feature/course-search`.
4. Open a GitHub pull request from that branch into `main`. A teammate reviews the diff, requests changes if needed, and approves the update.
5. The contributor responds to review comments with additional commits and pushes. GitHub updates the pull request automatically.
6. Merge the approved pull request on GitHub, then synchronize and clean up locally:

```powershell
git switch main
git pull origin main
git branch -d feature/course-search
git fetch --prune
```

For two contributors, assign separate features/branches, push both, and use pull requests so changes are reviewed before they reach `main`. If both edit the same lines, resolve the conflict together and record the resolution before merging. Never commit `.env`, credentials, or the generated SQLite database.

## Project layout

```text
app.py                 Flask routes and SQLite setup
requirements.txt       Flask dependency
templates/index.html   Dashboard, forms, student and course lists
templates/student.html Student profile and course schedule
static/style.css       Responsive dashboard styling
.gitignore             Local database and environment exclusions
```

## Learning scope

This demo intentionally keeps authentication, role permissions, production hosting, email verification, and database migrations out of scope. Add those before using it with real student information.
=======
# student-course-registration
>>>>>>> 03181b38ee412a522b54cb27ebd0961a66fe31da
