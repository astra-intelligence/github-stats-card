# GitHub Stats Card

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-%24-blueviolet)](https://grantshatz.gumroad.com/l/github-stats-card-pro)

Generate a beautiful, real-time **profile stats card** for your GitHub README — with **total stars**, **top language**, followers, repos, and more.

## Live Demo

👉 **[https://167.233.135.161:8083](https://167.233.135.161:8083)**

## One-line embed

Add this to your profile README:

```markdown
![Your Name's GitHub Stats](https://167.233.135.161:8083/card?user=yourusername&theme=dark)
```

## What's on the card

- ⭐ **Total stars** across all public repos
- 🔤 **Top language** (with its GitHub color)
- 📦 Repository count
- 👥 Followers & following
- 💬 Gists
- 🎨 8 themes (Dark, Light + 6 premium)

## Free vs Pro

| Feature | Free | Pro ($1) |
|---------|------|----------|
| Dark & Light themes | ✅ | ✅ |
| Stars + language stats | ✅ | ✅ |
| 6 premium themes | ❌ | ✅ |
| No watermark | ❌ | ✅ |
| License activation | — | ✅ |

**Get Pro:** [grantshatz.gumroad.com/l/github-stats-card-pro](https://grantshatz.gumroad.com/l/github-stats-card-pro)

## API

```
GET /card?user=USERNAME&theme=dark|light|ocean|sunset|forest|midnight|copper|plasma&key=LICENSE_KEY
```

- `user` — required. GitHub username.
- `theme` — optional, defaults to `dark`. Premium themes require a license key.
- `key` — optional. Gumroad license key; removes watermark and unlocks premium themes.

## Activate your license

Send your Gumroad license key to `/api/activate` (POST, JSON `{"license_key": "..."}`) to register it, or pass it directly as `&key=...` on the card URL.

## Why it's different

- **Live data** — the SVG re-renders from GitHub's API, so it never goes stale
- **Zero config** — no token, no build step, just one line of markdown
- **Pretty** — gradient accents, clean typography, language-aware colors
- **Fair** — free forever, $1 one-time for premium

## License

MIT — free for any use. Premium features require a one-time license key.

---

*Built with ❤️ — [GitHub Stats Card](https://167.233.135.161:8083)*