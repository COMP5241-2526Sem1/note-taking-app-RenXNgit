# Lab 2 Exercise Technical Documentation: Notes App Cloud Deployment Implementation Report

## Project Overview

In this lab, we implemented GenAI features in the notes taking app (Translation and Notes Generation), successfully migrated a Flask notes app based on SQLite to a cloud database (PostgreSQL), and deployed it to the Vercel platform.

### Original Architecture
- **Backend Framework**: Flask + SQLAlchemy
- **Database**: SQLite (local file database)
- **Frontend**: Static HTML/CSS/JavaScript
- **Deployment Method**: Local development server

### Target Architecture
- **Backend Framework**: Flask + SQLAlchemy (unchanged)
- **Database**: PostgreSQL (Supabase cloud database)
- **Frontend**: Static files (unchanged)
- **Deployment Platform**: Vercel Serverless Functions

## Implementation Steps

### Step 1: Project Dependency Update

Update `requirements.txt` to add required dependencies:

```txt
# New dependencies
psycopg2-binary    # PostgreSQL database driver
python-dotenv==1.0.0      # Environment variable management
```

### Step 2: Database Configuration Refactoring

Modify `src/main.py` database configuration:

```python
# Add environment variable support
from dotenv import load_dotenv
load_dotenv()

# Flexible database configuration
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Cloud database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    if DATABASE_URL.startswith('postgres'):
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'connect_args': {'sslmode': 'require'}
        }
else:
    # Local development fallback
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
```
![alt text](image-10.png)

### Step 3: Setting Up Supabase

**3.1. Create a Supabase Project**
1. Visit [supabase.com](https://supabase.com)
2. Create a new project
3. Record the project information

**3.2. Obtain Connection Information**
1. Go to Project Settings > Database
2. Copy the connection string

Example:
```
DATABASE_URL=postgresql://postgres.rlhdtbbsgtsssindqbsw:202510note-taking-app@aws-1-ap-south-1.pooler.supabase.com:6543/postgres
```
![alt text](image-11.png)

### Step 4: Vercel Deployment

**4.1. Create `vercel.json` configuration file:**

```json
{
  "version": 2,
  "builds": [
    {"src": "src/main.py", "use": "@vercel/python"}
  ],
  "routes": [
    {"src": "/api/(.*)", "dest": "src/main.py"},
    {"src": "/(.*)", "dest": "src/main.py"}
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

**4.2. Environment Variable Management**
- Update `.env`, `.gitignore`
- Local testing and validation (environment setup + dependency installation + app launch test)

**4.3. GitHub Preparation**
```bash
git add .
git commit -m "feat: migrate to PostgreSQL and add Vercel support"
git push origin main
```

**4.4. Vercel Configuration**
1. Log in to [vercel.com](https://vercel.com)
2. Import GitHub repository
3. Configure environment variables:
   - `DATABASE_URL`: Supabase connection string
   - `SECRET_KEY`: Strong random string

**4.5. Deployment Verification**
- [x] Deployment succeeds without errors
- [x] Application is accessible
- [x] Database connection is normal
- [x] All features work, such as creating notes, drag-and-drop note reordering, translation feature, notes generation feature, and “Generate notes” function extended to extract date and time (if available) all work correctly

![alt text](image-14.png)

### Step 5: Handling API Keys

1. Generate Token
2. Add API key in Vercel ![alt text](image-12.png)
3. Store locally in `.env`, include `.env` in `.gitignore`

## Lessons Learned

1. AI can add new content to the app according to prompts, but if new features are not needed, it’s important to instruct AI not to add them.
![alt text](image-3.png)

2. First deployment failed because the AI-generated `psycopg2-binary` specified a version number.
![alt text](image-2.png)

3. After deploying based on AI’s prompts, the note_taking_app could not be opened via the link. The reason was local network did not support IPv6. Found an alternative in Supabase: changed its IPv6 to Supavisor transaction mode.
![alt text](image.png)

4. By following AI instructions, problems can be identified. After deploying to Vercel, the translation feature was not working. Running `echo $GITHUB_TOKEN` revealed that Codespaces used `ghu_` token, not the generated `GITHUB_TOKEN`. The previously generated `GITHUB_TOKEN` was not effective. Regenerated `GITHUB_TOKEN` and redeployed as per AI’s advice; translation feature then worked.
![alt text](image-8.png)
![alt text](image-16.png)

5. Practiced extending the “Generate notes” function to extract date and time (if available), and verified successful operation.
![alt text](image-13.png)

6. Added prompts such as "Translating...", "Translation successful", and "Generating notes. Wait for a moment, please...".