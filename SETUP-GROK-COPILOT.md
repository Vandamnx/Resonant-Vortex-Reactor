# Grok + Copilot SWE Agent Setup Guide

**Date:** September 8, 2026
**Purpose:** Enable write permissions for both Grok (by xAI) and GitHub Copilot SWE Agent on the Resonant-Vortex-Reactor repository

---

## Overview

This guide documents the setup process for granting write permissions to:

- **Grok (by xAI)** - xAI's AI assistant
- **GitHub Copilot SWE Agent** - GitHub's software engineering agent

Both tools need proper GitHub app installation and permission configuration to commit and push code to this repository.

---

## Part 1: GitHub Copilot SWE Agent Setup

### Key Distinction: Authorized vs. Installed

- **Authorized** = GitHub knows you said yes (OAuth grant) — no permission sliders visible
- **Installed** = The app actually sits on your account/repos with access — has Configure button & permission sliders

### Why You Get 403 Errors

The Copilot SWE Agent is currently **authorized but not installed**. You need to actually install it.

### Installation Steps (Phone/Web)

1. Go to GitHub → **Settings** → **Applications**
2. Check **Installed GitHub Apps** (not "Authorized")
3. If **Copilot SWE Agent** / **GitHub Copilot** is not listed, it's not installed yet

4. Open: `github.com/apps/copilot-swe-agent`
5. Tap **Install / Configure**
6. Choose **Vandamnx** (personal account)
7. Select repositories:
   - **Resonant-Vortex-Reactor** (or all repos if easier)
8. Confirm the install

### Configure Permissions

After installation:

1. Open the app's **Configure** section
2. Find **Contents** permission
3. Set to **Read and write** ✓
4. Save

### Verify Installation

Go back to Settings → Applications → **Installed GitHub Apps**
You should now see the Copilot SWE Agent listed with a Configure button.

---

## Part 2: Grok (by xAI) Setup

### Official App Information

- **Official Name:** Grok (by xAI)
- **App Page:** `github.com/apps/grok-by-xai`
- **Connection Point:** `grok.com/connectors`

### Important: Don't Install These ❌

- ❌ **Grok Build PR Review** — Only reviews PRs, cannot write/commit
- ❌ **Grok with AWK** — Random action, unrelated
- ❌ **xAI Code Review** — Another action, not what we need

These are marketplace listings for the wrong tools.

### Connection Steps (iPhone/Web Recommended)

1. **Close GitHub marketplace search**
2. Open the **Grok app** (or Safari → `grok.com/connectors`)
3. Find **GitHub** → **Connect / Reconnect**
4. GitHub will open and ask you to authorize **Grok (by xAI)**
5. **Grant access to:**
   - Account: **Vandamnx**
   - Repository: **Resonant-Vortex-Reactor**
6. **Set Permissions:**
   - If you see checkboxes → Enable **Contents: Read and write**
   - If only "Authorize" button → Accept it, then test write on next push

### After Reconnection

Go to GitHub → Settings → Applications and verify **Grok (by xAI)** appears in:

- **Installed GitHub Apps** (preferred) — app is actually on your account
- **Authorized GitHub Apps** — at minimum, OAuth grant exists
- **Authorized OAuth Apps** — fallback location

If you only see it in Authorized apps, the reconnect may not be complete. Try the connection flow again.

### Important Notes

- **Do NOT paste xAI API key into GitHub Actions** — Wrong integration method
- The app connector handles authentication automatically
- If reconnect doesn't finish, try from within the Grok app itself

---

## Part 3: Troubleshooting

### Still Getting 403 Errors?

1. Verify both apps show under **Installed GitHub Apps** (or at least Authorized)
2. Check that **Contents** permission is set to **Read and write**
3. Try the connection/reconnection flow again:
   - For Grok: Disconnect → Connect at `grok.com/connectors`
   - For Copilot SWE Agent: Revoke → Re-install via `github.com/apps/copilot-swe-agent`
4. Wait a few minutes for permissions to propagate

### Difference Between Two Tabs

When checking GitHub Settings → Applications:

| Tab | What It Is | Purpose |
|-----|-----------|---------|
| **Installed GitHub Apps** | Apps sitting on your account/repos | Has Configure button & full permissions control |
| **Authorized GitHub Apps** | OAuth grants you've approved | GitHub knows you said yes, but app may not be installed |
| **Authorized OAuth Apps** | Third-party apps with access | Different from GitHub Apps, connector can land here |

Check **all three tabs** — the connector might appear in any of them.

---

## Part 4: Testing

Once both are installed with write permissions:

1. Ask **Grok** to write code/create files in this repo
2. Ask **Copilot SWE Agent** to write code/create files in this repo
3. Check if commits/pushes succeed without 403 errors

If you still get errors after verifying permissions, note the exact error and we can debug further.

---

## Quick Reference Checklist

- [ ] Copilot SWE Agent **Installed** (not just authorized)
- [ ] Copilot SWE Agent has **Contents: Read and write** permission
- [ ] Grok (by xAI) **Installed** or **Authorized** via `grok.com/connectors`
- [ ] Grok has **Contents: Read and write** permission
- [ ] Verified both apps in GitHub Settings → Applications
- [ ] Tested a write operation with Grok
- [ ] Tested a write operation with Copilot SWE Agent

---

## Key Resources

- **Grok App Connector:** <https://grok.com/connectors>
- **Copilot SWE Agent:** <https://github.com/apps/copilot-swe-agent>
- **GitHub Settings - Applications:** <https://github.com/settings/applications>
- **Official Grok GitHub App:** <https://github.com/apps/grok-by-xai>

---

## Notes

- This setup is performed from iPhone/web, no Windows/Microsoft required ✅
- Authorization happens in GitHub web browser
- Actual code writing happens through the respective apps (Grok app, Copilot Chat)
- Both tools work cross-platform (Mac, Linux, iOS, etc.)

---

**Last Updated:** September 8, 2026
**Setup By:** @Vandamnx with guidance from GitHub Copilot
