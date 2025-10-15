# Operator - Quick Reference Card

## 📱 SMS Commands

| Command | Description | Example |
|---------|-------------|---------|
| `help` | Show all commands | `help` |
| `status` | System overview | `status` |
| `health` | Check all systems | `health` |
| `health <system>` | Check specific system | `health prometheus` |
| `metrics <query>` | Query metrics | `metrics cpu_usage` |
| `logs <term>` | Search logs | `logs error` |
| `db` | Database stats | `db connections` |
| `gateway` | Gateway stats | `gateway status` |

## 🚀 Run Commands

```bash
# Start server
python app.py
# Or: ./run.sh app (Linux/Mac)
# Or: run.bat app (Windows)

# Test monitors
python test_monitors.py

# Test commands
python test_commands.py

# Send test SMS
python main.py
```

## 🔧 Configuration Checklist

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Edit .env and set:
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=your_token
TWILIO_MESSAGING_SERVICE_SID=MGxxxxx
TWILIO_FROM_NUMBER=+1234567890
AUTHORIZED_NUMBERS=+1234567890

# 3. Set monitoring URLs (optional)
PROMETHEUS_URL=http://localhost:9090
LOGS_URL=http://localhost:9200
GATEWAY_URL=http://localhost:8001
# ... etc
```

## 🌐 Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/sms` | POST | Twilio webhook |
| `/health` | GET | Health check |
| `/` | GET | Service info |

## 📂 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask server |
| `command_processor.py` | Command logic |
| `security.py` | Auth & verification |
| `config.py` | Configuration |
| `monitors/*` | Monitoring integrations |

## 🔐 Security

✅ Twilio signature verification
✅ Phone number authorization
✅ Environment-based secrets
⚠️ Use HTTPS in production

## 🧪 Testing

```bash
# Local webhook test
curl -X POST http://localhost:5000/sms \
  -d "From=+1234567890" \
  -d "Body=help"

# With ngrok
ngrok http 5000
# Use: https://abc123.ngrok.io/sms
```

## 📊 Monitoring Systems

| System | Config Needed |
|--------|---------------|
| Prometheus | `PROMETHEUS_URL` |
| Datadog | `DATADOG_API_KEY`, `DATADOG_APP_KEY` |
| Elasticsearch | `LOGS_URL`, `LOGS_TYPE=elasticsearch` |
| Loki | `LOGS_URL`, `LOGS_TYPE=loki` |
| Database | `DB_STATS_URL` |
| Kong | `GATEWAY_URL`, `GATEWAY_TYPE=kong` |

## 🐛 Common Issues

**Import errors?**
→ Activate venv: `source venv_operator/bin/activate`

**Twilio auth fails?**
→ Check `TWILIO_AUTH_TOKEN` matches console

**Monitor timeout?**
→ Verify URLs are accessible

**SMS not received?**
→ Check Twilio webhook is configured correctly

## 📚 Documentation

- `README.md` - Overview & quick start
- `SETUP.md` - Detailed setup guide
- `ADVANCED.md` - Advanced features & examples
- `IMPLEMENTATION.md` - Full implementation details

## 💡 Pro Tips

1. Use ngrok for local testing
2. Keep SMS responses < 160 chars
3. Monitor the monitor (set up /health checks)
4. Log everything for debugging
5. Test before going to production
6. Add rate limiting for production
7. Use gunicorn in production, not Flask dev server

## 🎯 Quick Start (30 seconds)

```bash
# 1. Configure
cp .env.example .env && nano .env

# 2. Install
pip install -r requirements.txt

# 3. Run
python app.py

# 4. Test
python test_commands.py

# 5. Configure Twilio webhook
# Point to: https://your-url.com/sms
```

## 📞 SMS Response Format

✅ Success: `📊 Metrics: cpu: 45%`
❌ Error: `❌ Error: Connection failed`
📋 Logs: `📋 Found 5 logs`
🗄️ Database: `🗄️ DB Connections: 45`
🌐 Gateway: `🌐 API Gateway: 156 requests`
🏥 Health: `🏥 Health Check: ✅ Healthy`

## 🔄 Development Workflow

1. Edit code
2. Test locally: `python test_commands.py`
3. Test monitors: `python test_monitors.py`
4. Run server: `python app.py`
5. Test via SMS or curl
6. Deploy to production

---

**Need help?** Check SETUP.md or ADVANCED.md
