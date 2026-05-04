# DNS-Switch: GoDaddy to Cloudflare Automation

A specialized Python toolkit for automating the migration of DNS records and nameservers from GoDaddy to Cloudflare. This tool was built to ensure zero-downtime migrations for domains using Google Workspace or Google Sites.

## 🚀 Features

- **Automated Zone Creation**: Automatically creates a Cloudflare zone if it doesn't exist.
- **Batch Record Migration**: Fetches all DNS records (A, CNAME, MX, TXT) from GoDaddy and pushes them to Cloudflare.
- **Smart Filtering**: Automatically skips legacy GoDaddy records (`NS`, `_domainconnect`) to prevent conflicts.
- **Root Domain Fixer**: Implements Google's recommended A records for "Naked Domain" redirects.
- **Health Checks**: Verification script to confirm Nameserver propagation, Web resolution, and Email (MX) health.

## 🛠️ Project Structure

- `godaddy.py`: Client for interacting with the GoDaddy V1 API.
- `cloudflare.py`: Client for interacting with the Cloudflare V4 API.
- `utils.py`: Shared utilities for configuration and client initialization.
- `audit.py`: Audits current DNS status and prepares the Cloudflare zone.
- `migrate.py`: Copies records from GoDaddy to Cloudflare.
- `finalize.py`: Flips the nameserver switch at GoDaddy.
- `fix_google_root.py`: Updates root A records to modern Google redirection IPs.
- `verify.py`: Post-migration health check tool.

## 📋 Prerequisites

- Python 3.10+
- GoDaddy API Key & Secret ([Get here](https://developer.godaddy.com/keys))
- Cloudflare API Token with `Zone:Edit` and `Account:Read` permissions ([Get here](https://dash.cloudflare.com/profile/api-tokens))

## ⚙️ Installation

1. **Clone the repository** (or copy the files).
2. **Create a virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

## 🔧 Configuration

Create a `.env` file in the root directory (use `.env.example` as a template):

```env
DOMAIN=yourdomain.com

# GoDaddy
GODADDY_API_KEY=your_key
GODADDY_API_SECRET=your_secret

# Cloudflare
CLOUDFLARE_API_TOKEN=your_token
```

## 📖 Usage Workflow

Follow these steps in order for a safe migration:

### 1. Audit & Setup
Checks your current nameservers and ensures the domain exists in Cloudflare.
```powershell
python audit.py
```

### 2. Migrate Records
Copies your existing DNS records to Cloudflare.
```powershell
python migrate.py
```

### 3. (Optional) Fix Google Root Domain
If using Google Sites, run this to update root A records to the correct redirection IPs.
```powershell
python fix_google_root.py
```

### 4. Finalize the Switch
Updates nameservers at GoDaddy to point to Cloudflare.
```powershell
python finalize.py
```

### 5. Verify Health
Check if the migration was successful and propagation is complete.
```powershell
python verify.py
```

## 🛡️ Security

- **`.env`**: Never commit this file. It is excluded by `.gitignore`.
- **API Tokens**: Always use the "Least Privilege" principle when creating Cloudflare tokens.

## ⚖️ License
MIT
