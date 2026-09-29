# GitHub Stats Card — Fix Your Broken Profile README Stats

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-%24-blueviolet)](https://grantshatz.gumroad.com/l/github-stats-card-pro)

**github-readme-stats returning 503?** Use this free, working alternative. Generate a beautiful real-time profile stats card for your GitHub README — with total stars, top language, followers, repos, and more.

No Vercel deploy needed. No account required. One line of markdown.

## 🔧 Why you're here

The public instance of `github-readme-stats` (`https://github-readme-stats.vercel.app/api?username=...`) is returning **HTTP 503 (Service Unavailable)**. This affects millions of GitHub profile READMEs.

This service is a free, working replacement. Just swap the URL.

## Try it now

👉 **Live demo:** [http://167.233.135.161:8085](http://167.233.135.161:8085)

Enter your GitHub username, pick a theme, and copy the embed code.

## One-line embed

Replace your broken stats card with:

```markdown
![Your GitHub Stats](http://167.233.135.161:8085/card?user=YOUR_USERNAME&theme=dark)
```

### Options

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `user` | ✅ | — | Your GitHub username |
| `theme` | ❌ | `dark` | `dark`, `light`, `ocean`, `sunset`, `forest`, `midnight`, `copper`, `plasma` |
| `key` | ❌ | — | Gumroad Pro license key (removes watermark) |

## What's on the card

- ⭐ **Total stars** across all public repos
- 🔤 **Top language** (with GitHub color)
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

## Why this is different from github-readme-stats

- **Live data** — the SVG re-renders from GitHub's API, so it never goes stale
- **Zero config** — no token, no Vercel deploy, no build step
- **Drop-in replacement** — same URL pattern, just a different host
- **8 themes** — more variety than the original
- **Fair** — free forever, $1 one-time for premium themes + watermark removal

## API

```
GET /card?user=USERNAME&theme=dark|light|ocean|sunset|forest|midnight|copper|plasma&key=LICENSE_KEY
```

Returns `image/svg+xml`.

## Activate your license

Send your Gumroad license key to `/api/activate` (POST, JSON `{"license_key": "..."}`) to register it, or pass it directly as `&key=...` on the card URL.

## License

MIT — free for any use. Premium features require a one-time $1 license key.

---

*Built with ❤️ — [GitHub Stats Card](http://167.233.135.161:8085)*