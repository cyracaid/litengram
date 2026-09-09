# Security & Privacy — LitEngram

---

## 🔒 Data Privacy Model

### What Data LitEngram Touches

Your Computer (Local - Never Leaves):
- Zotero SQLite database
  - PDF metadata (title, authors, DOI)
  - Your highlights (text you selected)
  - Your annotations (your thoughts)
  - Paper metadata
- Ollama (local LLM)
  - Temporary: passed to LLM for processing only
- Environment variables
  - NOTION_TOKEN (only if you enable Notion sync)
- Temporary files
  - Session logs (deleted after completion)

Optional: Notion (if you explicitly enable)
- You provide: NOTION_TOKEN (your choice)
- You control: what syncs and when

### Zero Data Collection

What we NEVER do:
- No telemetry or tracking
- No usage analytics
- No heartbeat calls
- No data logging to external servers
- No A/B testing
- No user profiling

Why? LitEngram is open-source. You can audit the code yourself.

---

## 🔐 Best Practices

### 1. Environment Variables

DO:
```bash
# Store tokens in .env (git-ignored)
cat > .env << EOF
ZOTERO_DB_PATH=~/Zotero/zotero.sqlite
NOTION_TOKEN=ntn_xxxxx_keep_secret
OLLAMA_MODEL=qwen2.5:0.5b
EOF

chmod 600 .env  # Only you can read
```

DONT:
```bash
# Don't commit .env to git
git add .env  # NO!

# Don't put tokens in code
export NOTION_TOKEN="ntn_xxxxx"  # Visible in history

# Don't share .env files
# Don't paste tokens in Slack/email
```

### 2. Git Security

Always use `.gitignore`:
```bash
# .gitignore
.env
*.log
*.db
zotero.sqlite*
token*
credentials*
secrets*
```

Verify:
```bash
# Check what's tracked
git ls-files | grep -E "(env|token|secret|password)"
# Should return nothing!
```

### 3. Notion Integration

If you enable Notion sync:

1. Create a NEW integration (not reusing existing ones)
   - https://www.notion.so/my-integrations
   - Name it "LitEngram" (descriptive)

2. Grant MINIMAL permissions needed:
   - Read: YES
   - Update: YES
   - Don't give Delete, Transfer, etc

3. Limit database access
   - In Notion: click "..." → Connections
   - Select ONLY the LitEngram database
   - Don't grant access to all databases

4. Rotate tokens periodically
   - Every 90 days: regenerate token
   - Every year: create new integration

5. Monitor usage
   - Check Notion audit log for unexpected access

### 4. Database Security

```bash
# Don't make Zotero database world-readable
ls -la ~/Zotero/zotero.sqlite
# Should show: -rw------- (600 permissions)

# If wrong permissions, fix:
chmod 600 ~/Zotero/zotero.sqlite

# Backup securely
# - Use encrypted backup (Time Machine, Backblaze, etc)
# - Don't backup to unencrypted USB or cloud without encryption
```

---

## 🚨 Threat Model

### Threat: Malicious Process on Your Computer

Risk: Someone with root access could read Zotero DB

Mitigation:
- Keep OS and software updated
- Use firewall
- Use antivirus
- Use full-disk encryption (FileVault on macOS, BitLocker on Windows)

### Threat: Notion Token Leakage

Risk: If NOTION_TOKEN exposed, attacker can read/modify your Notion

Mitigation:
- Keep .env in .gitignore
- Don't share token via Slack/email
- Rotate token every 90 days
- Use minimal-permission integration

### Threat: Ollama Network Exposure

Risk: If Ollama accidentally exposed to network, others could use it

Mitigation:
```bash
# Ollama listens on localhost:11434 by default
# Check it's NOT accessible from internet:

netstat -an | grep 11434
# Should show: 127.0.0.1:11434 (localhost only)
# NOT: 0.0.0.0:11434 (world-accessible)

# If world-accessible, use firewall
```

---

## 🔍 Audit Trail

### What LitEngram Logs (Optional)

```bash
# Enable detailed logging
export DEBUG=true

# What's logged:
# - Zotero connection success/failure
# - Annotation counts
# - Processing duration
# - Error messages

# NOT logged:
# - Highlight text
# - Your comments
# - Notion data
# - Personal information
```

---

## 🛡️ Security Update Policy

Check for updates monthly:
```bash
cd litengram
git fetch origin
git log origin/main --oneline -10
git pull origin main
pip install -r requirements.txt
```

Reporting Security Issues:
- DO NOT open public GitHub issue for security bugs
- Email: security@example.com
- OR: Create private GitHub security advisory

---

## ✅ Secure Setup Checklist

```bash
[ ] 1. OS Security
  [ ] Full-disk encryption enabled
  [ ] OS and software updated
  [ ] Firewall enabled

[ ] 2. Python & Dependencies
  [ ] Virtual environment created
  [ ] requirements.txt up-to-date
  [ ] pip check → no conflicts

[ ] 3. Zotero Security
  [ ] Database permissions: 600
  [ ] Password set (if cloud sync enabled)

[ ] 4. Environment Setup
  [ ] .env file created with tokens
  [ ] .env is git-ignored
  [ ] .env file permissions: 600

[ ] 5. Ollama Security
  [ ] Listening on localhost only
  [ ] Network firewall blocks port 11434

[ ] 6. Notion Security (if using)
  [ ] Integration has minimal permissions
  [ ] Database shared with integration only
  [ ] Token rotation scheduled

[ ] 7. Backup & Recovery
  [ ] Regular backups enabled
  [ ] Backups encrypted
  [ ] Can restore from backup

[ ] 8. Regular Maintenance
  [ ] Monthly: git pull for security updates
  [ ] Quarterly: rotate Notion token
  [ ] Annually: full security audit
```

---

For more on privacy, see BEST_PRACTICES.md
