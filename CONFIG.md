# GPT-5 Mini Configuration Guide

## Overview

This document describes how to configure and deploy GPT-5 mini support for the Task Manager application.

## Current Configuration Status

✅ **GPT-5 mini is ENABLED for all clients globally**

- **Model**: gpt-5-mini
- **Status**: Active
- **Scope**: Global (all clients have access)
- **All Clients Enabled**: true

## Configuration Files

### 1. `config.yaml` (Main Configuration)

Located at: `c:\Formation\githubcopilot\config.yaml`

This is the primary configuration file containing all AI model settings:

```yaml
ai_model:
  enabled: true
  model: "gpt-5-mini"
  all_clients_enabled: true
  scope: "global"
```

**Key Settings:**
- `enabled`: Activates/deactivates the AI model integration
- `model`: Specifies which AI model to use (currently: gpt-5-mini)
- `all_clients_enabled`: When true, all clients can access GPT-5 mini
- `scope`: Deployment scope ("global" = all clients, "regional" = specific regions)

### 2. `.env.gpt5` (Runtime Environment Variables)

Located at: `tp2_task_manager\.env.gpt5`

Auto-generated environment variables for application runtime:

```
AI_MODEL_ENABLED=true
AI_MODEL_NAME=gpt-5-mini
AI_MODEL_ALL_CLIENTS=true
AI_MODEL_SCOPE=global
CONFIG_SOURCE=config.yaml
```

## Deployment Process

### Manual Deployment

To deploy the GPT-5 mini configuration:

```powershell
# Navigate to the workspace
cd c:\Formation\githubcopilot

# Run the deployment script
.\deploy-config.ps1 -Validate

# This will:
# 1. Validate prerequisites
# 2. Parse the configuration file
# 3. Generate .env.gpt5 with runtime variables
# 4. Create a deployment report
```

### Running the Application with Configuration

```powershell
# Load the environment variables
. .\tp2_task_manager\.env.gpt5

# Start the Task Manager application
python tp2_task_manager\app.py
```

## Configuration Modification

### To Disable GPT-5 Mini for All Clients

Edit `config.yaml`:

```yaml
ai_model:
  enabled: false  # Set to false to disable
  model: "gpt-5-mini"
  all_clients_enabled: false
  scope: "global"
```

Then re-run deployment:
```powershell
.\deploy-config.ps1 -Validate
```

### To Enable Only for Specific Clients

Edit `config.yaml`:

```yaml
ai_model:
  enabled: true
  model: "gpt-5-mini"
  all_clients_enabled: false  # Disable global access
  scope: "regional"

clients:
  gpt5_mini_access:
    whitelist:
      - "client-1"
      - "client-2"
      - "client-3"
    blacklist: []
```

### To Switch to a Different AI Model

Edit `config.yaml`:

```yaml
ai_model:
  enabled: true
  model: "gpt-4"  # Change to desired model
  all_clients_enabled: true
  scope: "global"
```

## Verification

### Verify Configuration Syntax

```powershell
cd c:\Formation\githubcopilot
.\deploy-config.ps1 -Validate
```

### Verify Runtime Configuration

Once the application is running with `.env.gpt5` loaded, verify GPT-5 mini is active by:

1. Checking application logs for: `AI_MODEL_NAME=gpt-5-mini`
2. Testing AI model endpoints (if applicable)
3. Confirming all clients can access the model

## Troubleshooting

### Issue: PyYAML Not Installed

**Error**: "WARNING: Could not validate YAML (PyYAML may not be installed)"

**Solution**: Install PyYAML for YAML validation (optional):
```powershell
pip install pyyaml
```

### Issue: .env.gpt5 Not Loading

**Problem**: Environment variables not set after sourcing `.env.gpt5`

**Solution**: Verify the file exists and is readable:
```powershell
Test-Path .\tp2_task_manager\.env.gpt5
Get-Content .\tp2_task_manager\.env.gpt5
```

### Issue: Configuration Not Applied

**Problem**: Application still using default model after deployment

**Solution**: 
1. Verify `.env.gpt5` exists in the application directory
2. Source the environment file before starting the app:
   ```powershell
   . .\tp2_task_manager\.env.gpt5
   python app.py
   ```

## Files Reference

| File | Location | Purpose |
|------|----------|---------|
| `config.yaml` | `c:\Formation\githubcopilot\config.yaml` | Main configuration (edit here for changes) |
| `.env.gpt5` | `tp2_task_manager\.env.gpt5` | Runtime environment variables (auto-generated) |
| `deploy-config.ps1` | `c:\Formation\githubcopilot\deploy-config.ps1` | Deployment script (run to apply changes) |
| `deployment-report.txt` | `tp2_task_manager\deployment-report.txt` | Deployment status and summary |

## Best Practices

1. **Always validate before deployment**:
   ```powershell
   .\deploy-config.ps1 -Validate
   ```

2. **Keep `config.yaml` version controlled**: Track changes to `config.yaml` in your repository for audit trail.

3. **Review deployment report**: Check `deployment-report.txt` after each deployment to confirm settings.

4. **Test after configuration changes**: Always test the application with new configuration to ensure it works correctly.

5. **Use `.env.gpt5` for development**: Keep the generated `.env.gpt5` in `.gitignore` as it contains runtime-specific settings.

## Advanced Configuration

For advanced scenarios (multiple regions, client whitelisting, etc.), edit `config.yaml` directly:

```yaml
ai_model:
  enabled: true
  model: "gpt-5-mini"
  all_clients_enabled: false
  scope: "regional"
  regions:
    - name: "us-east-1"
      enabled: true
    - name: "eu-west-1"
      enabled: true

clients:
  gpt5_mini_access:
    whitelist:
      - "client-prod-1"
      - "client-prod-2"
    blacklist:
      - "client-test-1"
```

## Support

For issues or questions about the GPT-5 mini configuration:

1. Check this documentation
2. Review the deployment report: `tp2_task_manager\deployment-report.txt`
3. Verify configuration syntax with: `.\deploy-config.ps1 -Validate`
4. Check application logs for error messages

---

**Last Updated**: 2025-12-02  
**Configuration Version**: 1.0  
**Status**: ✅ Active
