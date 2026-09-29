# GitHub Stats Card — Fix Your Broken Profile README Stats

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Buy me a coffee](https://img.shields.io/badge/Pro-%241-blueviolet)](https://grantshatz.gumroad.com/l/github-stats-card-pro)

**github-readme-stats returning 503?** Use this free, working alternative. Generate a beautiful real-time profile stats card for your GitHub README — with total stars, top language, followers, repos, and more.

No Vercel deploy needed. No account required. One line of markdown.

## 🔧 Why you're here

The public instance of `github-readme-stats` (`https://github-readme-stats.vercel.app/api?username=...`) has been returning **HTTP 503 (Service Unavailable)** on and off since November 2025, affecting millions of GitHub profile READMEs worldwide.

This service is a free, working replacement. Just swap the URL.

## 🚀 Live generator

👉 **[http://167.233.135.161:8085](http://167.233.135.161:8085)**

Enter your GitHub username, pick a theme, and copy the embed code.

## One-line embed

Replace your broken stats card with:

```markdown
![Your GitHub Stats](http://167.233.135.161:8085/card?user=YOUR_USERNAME&theme=dark)
```

### Query parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `user` | ✅ | — | Your GitHub username |
| `theme` | ❌ | `dark` | `dark`, `light`, `ocean`, `sunset`, `forest`, `midnight`, `copper`, `plasma` |
| `key` | ❌ | — | Gumroad Pro license key (removes watermark, unlocks premium themes) |

## What's on the card

- ⭐ **Total stars** across all public repos (paginated, up to 500 repos)
- 🔤 **Top language** (with official GitHub color)
- 📦 Repository count
- 👥 Followers & following
- 💬 Public gists count
- 🎨 8 themes total (Dark, Light + 6 premium)

## Free vs Pro

| Feature | Free | Pro ($1) |
|---------|------|----------|
| Dark & Light themes | ✅ | ✅ |
| Stars + language + followers | ✅ | ✅ |
| 6 premium themes (Ocean, Sunset, Forest, Midnight, Copper, Plasma) | ❌ | ✅ |
| No watermark | ❌ | ✅ |
| License activation | — | ✅ |

**Get Pro:** [grantshatz.gumroad.com/l/github-stats-card-pro](https://grantshatz.gumroad.com/l/github-stats-card-pro)

## Why use this instead of self-hosting

- **Zero config** — no Vercel deploy, no environment variables, no token setup
- **Live data** — the SVG re-renders from GitHub's API on each request, so it's always current
- **Paginated stars** — we fetch up to 5 pages of repos for accurate star counts
- **Language-aware** — each language renders with its official GitHub color
- **8 themes** — more variety than the original project
- **Premium SKU** — $1 one-time unlocks premium themes and removes the watermark

## FAQ

**Q: Is this free?**  
A: Yes. The basic card with Dark/Light themes and all stats is completely free, forever.

**Q: How is this different from github-readme-stats-action?**  
A: The Action commits a static SVG to your repo. This service serves a live SVG from an API — it always reflects your current stats without needing a rebuild. Use whichever works for you.

**Q: The URL is HTTP, not HTTPS. Won't GitHub block it?**  
A: GitHub renders HTTP images from profile READMEs. However, for production README embedding we recommend the HTTPS endpoint. Contact us for the current HTTPS URL (it rotates periodically for load balancing).

**Q: How do I support this project?**  
A: Purchase Pro ($1 one-time) at Gumroad, or contribute to the open-source repo.

## API

```
GET /card?user=USERNAME&theme=dark|light|ocean|sunset|forest|midnight|copper|plasma&key=LICENSE_KEY
```

Returns `image/svg+xml`. Cache headers set to 1 hour.

## Activate your license

POST your Gumroad license key to `/api/activate` with JSON body `{"license_key": "..."}`. Once activated, pass `&key=YOUR_KEY` on card requests to unlock premium themes and remove the watermark.

## License

MIT — free for any use. Premium features require a one-time $1 license key.

---

*Built with ❤️ — [Profile Card Pro](http://167.233.135.161:8085) · My [GitHub Stats Card](https://github.com/astra-intelligence/github-stats-card)*