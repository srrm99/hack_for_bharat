# GitHub Repository Setup Guide

## Quick Setup

### 1. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `bharat-context-adaptive-engine`
3. Description: `Inference Engine for Day-0 Cold Start Problem - Tier-2/3/4 Indian Users`
4. Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### 2. Connect Local Repository to GitHub

After creating the repository on GitHub, run these commands:

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/bharat-context-adaptive-engine.git

# Or if using SSH:
git remote add origin git@github.com:YOUR_USERNAME/bharat-context-adaptive-engine.git

# Verify remote
git remote -v
```

### 3. Make Initial Commit

```bash
# Commit all files
git commit -m "Initial commit: Bharat Context-Adaptive Engine

- Complete inference engine with signal analysis
- Web intelligence, app context, and LLM reasoning modules
- FastAPI REST API with enhanced inference
- Comprehensive test suite
- Full documentation and examples"

# Push to GitHub
git branch -M main
git push -u origin main
```

### 4. Verify

Check your GitHub repository - all files should be visible!

## Repository Structure

```
bharat-context-adaptive-engine/
├── src/                    # Source code
│   ├── __init__.py
│   ├── main.py            # FastAPI app
│   ├── models.py          # Pydantic models
│   ├── inference_engine.py
│   ├── inference_engine_enhanced.py
│   ├── router_inference.py
│   ├── web_intelligence.py
│   ├── app_context.py
│   ├── llm_reasoning.py
│   ├── explanation_models.py
│   └── rules.yaml
├── tests/                  # Test files
│   ├── __init__.py
│   ├── test_inference_engine.py
│   ├── test_enhanced_engine.py
│   └── test_manual.py
├── docs/                   # Documentation
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── TESTING_GUIDE.md
│   └── ...
├── examples/               # Example payloads
├── scripts/                # Utility scripts
├── main.py                # Entry point
├── requirements.txt
├── setup.py
└── README.md
```

## Next Steps After Push

1. **Add Repository Topics**: Go to repository settings and add topics:
   - `python`
   - `fastapi`
   - `inference-engine`
   - `machine-learning`
   - `context-aware`
   - `india`

2. **Add License**: Consider adding a LICENSE file (MIT, Apache 2.0, etc.)

3. **Set Up GitHub Actions** (Optional): For CI/CD
   - Create `.github/workflows/ci.yml`
   - Run tests on push
   - Check code quality

4. **Add Badges** (Optional): Add to README.md
   - Build status
   - Test coverage
   - Python version

5. **Create Releases**: Tag versions
   ```bash
   git tag -a v1.0.0 -m "Initial release"
   git push origin v1.0.0
   ```

## Troubleshooting

### Authentication Issues

If you get authentication errors:

1. **Use Personal Access Token**:
   - GitHub Settings → Developer settings → Personal access tokens
   - Generate token with `repo` scope
   - Use token as password when pushing

2. **Use SSH**:
   ```bash
   # Generate SSH key
   ssh-keygen -t ed25519 -C "your_email@example.com"
   
   # Add to GitHub: Settings → SSH and GPG keys
   # Test connection
   ssh -T git@github.com
   ```

### Push Rejected

If push is rejected:
```bash
# Pull first (if repository was initialized with files)
git pull origin main --allow-unrelated-histories

# Then push
git push -u origin main
```

## Useful Git Commands

```bash
# Check status
git status

# View changes
git diff

# Add specific file
git add filename.py

# Commit with message
git commit -m "Your commit message"

# View commit history
git log

# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Merge branch
git merge feature/new-feature
```

