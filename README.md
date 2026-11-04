# Panther Parking

COMP 3322 Software Engineering, Fall 2026. Team: **<team 3>**

| Member | GitHub username | Story I own |
| --- | --- | --- |
| Esiri Ediri | ediriebizimo-design | Story 2 - Register a vehicle |
| Srivenkat Basava | Srivenkat2021 | Story 6 - Manage Lots |
| Kennedy Henry | KenRH21 | Story 3 - Apply for a permit |
| Baron Noi | Baronnoi | Story 4 - Approve permits |

## Set up your team repo (week 0, one member does steps 1-3)

1. On the starter template page, click **Use this template -> Create a new repository**.
   Do **not** fork. Name it `panther-parking-<team-name>`, set it to **Public**.
2. **Settings -> Collaborators**: add your teammates and the instructor.
3. **Settings -> Branches -> Add rule** for `main`:
   - Require a pull request before merging, with **1 approval**
   - Require status checks to pass: **`test`** (it appears after CI has run once)
   - Do not allow bypassing the above settings (applies to admins too)
4. **Everyone**: clone, branch, add your row to the team table above, open a PR,
   get it reviewed, merge. That is your first PR.

Then enter the four required stories as Issues using the *User story* template.

Submit the repo link on Canvas.

## Run it locally

Requires Python 3.12+ and git.

```bash
git clone <your repo URL>
cd <repo folder>
python -m venv .venv
# Windows:  .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
flask --app app init-db      # creates the database with sample lots
flask --app app run --debug  # open http://127.0.0.1:5000
```

Run the tests:

```bash
pytest -v
```

GitHub Actions runs the same tests on every push and pull request.

## Where things go

```
app/
  routes/        HTTP only: read the request, call a service, render a page
  services/      business rules (no SQL, no Flask request objects)
  repositories/  all SQL lives here
  templates/     HTML pages
  schema.sql     database tables
tests/           one test per acceptance criterion
docs/            architecture reference + your change-request note
.github/         CI workflow, PR template, user-story issue template
```

Read `docs/architecture.md` before adding code. The starter has two worked examples that follow the rules:
**Story #1** (register/log in) and **Story #5** (lot status). Copy their pattern: each has a route, a service, a repository and a test file whose tests are named after acceptance criteria.

## How we work

1. Pick an issue from the board and assign yourself.
2. Make a branch named for it: `git checkout -b 12-issue-citation`
3. Write the test(s) for the acceptance criteria, then the code. Commit small and often.
4. Push and open a pull request. Fill in the template, including the AI-use line.
5. A teammate reviews. Fix what they find. Merge when CI is green.
6. Nobody pushes to `main` directly.

## New to Flask?

The official tutorial builds an app with the same structure as this one in about two hours:
https://flask.palletsprojects.com/en/stable/tutorial/
