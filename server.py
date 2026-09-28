"""GitHub Profile README Stats Card Generator — free SVG with premium upsell."""
import json, os, sys, urllib.request, urllib.error, hashlib, time
from flask import Flask, Response, request, send_from_directory, jsonify

app = Flask(__name__, static_folder='.', static_url_path='')
GITHUB_API = "https://api.github.com"
SPONSOR_LINK = "https://grantshatz.gumroad.com/l/github-stats-card-pro"
CARD_W = 540
CARD_H = 270

# Premium themes + hex colors
THEMES = {
    "dark":       {"bg":"#0d1117","text":"#c9d1d9","dim":"#8b949e","accent":"#58a6ff","card":"#161b22","border":"#30363d"},
    "light":      {"bg":"#ffffff","text":"#1f2328","dim":"#656d76","accent":"#0969da","card":"#f6f8fa","border":"#d0d7de"},
    "ocean":      {"bg":"#0a1628","text":"#e0f0ff","dim":"#7aa2f7","accent":"#41a6f0","card":"#0f1f3d","border":"#1a3a6b"},
    "sunset":     {"bg":"#1a0f0a","text":"#ffe0c0","dim":"#c89070","accent":"#e06a4a","card":"#2a1a10","border":"#4a3020"},
    "forest":     {"bg":"#0a1a0a","text":"#d0f0c0","dim":"#70a860","accent":"#3fb950","card":"#102a10","border":"#1a4a1a"},
    "midnight":   {"bg":"#0a0a1a","text":"#c0c0e0","dim":"#6060a0","accent":"#8888ff","card":"#12122a","border":"#2a2a4a"},
    "copper":     {"bg":"#14100a","text":"#e0d4c0","dim":"#a09070","accent":"#c07a4a","card":"#1e1812","border":"#3a2e1e"},
    "plasma":     {"bg":"#0d0d1a","text":"#d0d0ff","dim":"#8080cc","accent":"#d040ff","card":"#181830","border":"#3a1a5a"},
}

# Valid premium license keys (sha256 fingerprints of known keys)
VALID_KEYS = set()


def load_license_keys():
    """Load valid license keys from a file managed by cron."""
    keyfile = os.path.join(os.path.dirname(__file__), "valid_keys.txt")
    if os.path.exists(keyfile):
        with open(keyfile) as f:
            VALID_KEYS.update(line.strip() for line in f if line.strip())


def is_premium(license_key=None):
    """Check if a license key unlocks premium features."""
    if not license_key:
        return False
    # Simple hash check — matches Gumroad license key
    h = hashlib.sha256(license_key.strip().encode()).hexdigest()[:16]
    return h in VALID_KEYS


def fetch_json(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "stats-card/2.0", "Accept": "application/vnd.github.v3+json"
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def fetch_stars(username, token=None):
    """Fetch total stargazer count across all public repos."""
    page = 1
    total = 0
    headers = {"User-Agent": "stats-card/2.0", "Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    while page <= 5:  # max 5 pages = 500 repos
        try:
            req = urllib.request.Request(
                f"{GITHUB_API}/users/{username}/repos?per_page=100&page={page}&sort=pushed", headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                repos = json.loads(resp.read())
                if not repos:
                    break
                total += sum(r.get("stargazers_count", 0) for r in repos)
                page += 1
        except Exception:
            break
    return total


def top_language(username, token=None):
    """Find the most-used language across public repos."""
    from collections import Counter
    langs = Counter()
    headers = {"User-Agent": "stats-card/2.0", "Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    page = 1
    while page <= 3:
        try:
            req = urllib.request.Request(
                f"{GITHUB_API}/users/{username}/repos?per_page=100&page={page}&sort=pushed", headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                repos = json.loads(resp.read())
                if not repos:
                    break
                for r in repos:
                    lang = r.get("language")
                    if lang:
                        langs[lang] += 1
                page += 1
        except Exception:
            break
    return langs.most_common(1)[0][0] if langs else ""


LANG_COLORS = {
    "Python": "#3572A5", "JavaScript": "#f1e05a", "TypeScript": "#3178c6",
    "Go": "#00ADD8", "Rust": "#dea584", "Java": "#b07219", "C": "#555555",
    "C++": "#f34b7d", "Ruby": "#701516", "PHP": "#4F5D95", "Swift": "#ffac45",
    "Kotlin": "#A97BFF", "Scala": "#c22d40", "HTML": "#e34c26", "CSS": "#563d7c",
    "Shell": "#89e051", "Dockerfile": "#384d54", "Makefile": "#427819",
    "Lua": "#000080", "R": "#198CE7", "Haskell": "#5e5086", "Elixir": "#4e2a59",
    "Vue": "#41b883", "Solidity": "#AA6746", "Zig": "#ec915c",
}


def generate_svg(username, data, theme="dark", premium=False):
    """Generate an SVG profile card. Premium removes watermark."""
    t = THEMES.get(theme, THEMES["dark"])
    avatar = data.get("avatar_url", "")
    name = data.get("name") or data.get("login", username)
    bio = (data.get("bio") or "")[:100]
    login = data.get("login", username)

    # Fetch extra data
    stars = fetch_stars(login)
    top = top_language(login)
    lang_color = LANG_COLORS.get(top, "#586069")
    followers = data.get("followers", 0)
    following = data.get("following", 0)
    repos = data.get("public_repos", 0)
    gists = data.get("public_gists", 0)

    accent = t["accent"]
    green = "#3fb950"
    w, h = CARD_W, CARD_H

    svg_parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="gh" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{accent};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{green};stop-opacity:1" />
    </linearGradient>
    <clipPath id="c"><circle cx="40" cy="36" r="28"/></clipPath>
  </defs>
  <rect x="0" y="0" width="{w}" height="{h}" rx="12" fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1"/>
  <rect x="0" y="0" width="{w}" height="4" rx="2" fill="url(#gh)"/>
  <!-- Avatar -->
  <image href="{escape(avatar)}" x="12" y="12" width="56" height="56" rx="28" clip-path="url(#c)"/>
  <circle cx="40" cy="40" r="28" fill="none" stroke="{t["border"]}" stroke-width="1"/>
  <!-- Name -->
  <text x="82" y="34" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="16" font-weight="700" fill="{t["text"]}">{escape(name)}</text>
  <text x="82" y="50" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="11" fill="{t["dim"]}">@{escape(login)}</text>
  <text x="82" y="66" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="11" fill="{t["dim"]}">{escape(bio[:60])}</text>
  <!-- Stats row -->''']

    # Row of stats
    stats_data = [
        ("★ Stars", str(stars)),
        ("Repos", str(repos)),
        ("Followers", str(followers)),
        ("Following", str(following)),
    ]
    sbox_w = 118
    gap = 10
    start_x = 14
    for i, (label, value) in enumerate(stats_data):
        x = start_x + i * (sbox_w + gap)
        svg_parts.append(f'''
    <rect x="{x}" y="78" width="{sbox_w}" height="58" rx="6" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="0.5"/>
    <text x="{x + sbox_w // 2}" y="99" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="18" font-weight="700" fill="{t["text"]}" text-anchor="middle">{value}</text>
    <text x="{x + sbox_w // 2}" y="118" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="10" fill="{t["dim"]}" text-anchor="middle">{label}</text>''')

    # Language bar
    if top:
        svg_parts.append(f'''
  <g transform="translate(14, 150)">
    <rect x="0" y="0" width="{w - 28}" height="28" rx="6" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="0.5"/>
    <rect x="0" y="0" width="4" height="28" fill="{lang_color}" rx="2"/>
    <text x="14" y="19" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="12" font-weight="600" fill="{t["text"]}">{escape(top)}</text>
    <text x="14" y="36" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="9" fill="{t["dim"]}">Most-used language</text>
  </g>''')
    else:
        svg_parts.append(f'''
  <g transform="translate(14, 150)">
    <rect x="0" y="0" width="{w - 28}" height="28" rx="6" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="0.5"/>
    <text x="14" y="19" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="12" fill="{t["dim"]}">No language data</text>
  </g>''')

    # Footer — watermark only if not premium
    if not premium:
        svg_parts.append(f'''
  <!-- Watermark -->
  <text x="{w - 10}" y="{h - 14}" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="9" fill="{t["dim"]}" text-anchor="end" opacity="0.7">stats-card · ♥ Support → {SPONSOR_LINK.split("/")[-1]}</text>''')
    else:
        svg_parts.append(f'''
  <text x="{w - 10}" y="{h - 14}" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="9" fill="{t["dim"]}" text-anchor="end">stats-card · ♥ Pro</text>''')

    svg_parts.append('\n</svg>')
    return ''.join(svg_parts)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/card')
def card():
    username = request.args.get('user', '')
    if not username:
        return jsonify({"error": "Missing 'user' parameter", "usage": "/card?user=username", "example": "/card?user=torvalds"}), 400

    data = fetch_json(f"{GITHUB_API}/users/{username}")
    if not data or data.get("message"):
        return jsonify({"error": f"User '{username}' not found"}), 404

    theme = request.args.get('theme', 'dark')
    license_key = request.args.get('key', '')
    premium = is_premium(license_key) if license_key else False

    svg = generate_svg(username, data, theme, premium)
    return Response(svg, mimetype='image/svg+xml', headers={
        "Cache-Control": "public, max-age=3600",
        "Access-Control-Allow-Origin": "*"
    })


@app.route('/api/preview')
def preview():
    username = request.args.get('user', '')
    if not username:
        return jsonify({"error": "Missing user"}), 400
    data = fetch_json(f"{GITHUB_API}/users/{username}")
    if not data:
        return jsonify({"error": "Not found"}), 404
    star_count = fetch_stars(username)
    lang = top_language(username)
    return jsonify({
        "user": username,
        "name": data.get("name"),
        "public_repos": data.get("public_repos"),
        "followers": data.get("followers"),
        "following": data.get("following"),
        "total_stars": star_count,
        "top_language": lang,
        "themes": list(THEMES.keys()),
        "premium_themes": [k for k in THEMES if k not in ("dark", "light")],
        "embed_url": f"https://167.233.135.161:8083/card?user={username}"
    })


@app.route('/api/activate', methods=['POST'])
def activate():
    """Validate a Gumroad license key and register it."""
    import hmac
    data = request.get_json() or {}
    key = data.get("license_key", "").strip()
    if not key:
        return jsonify({"valid": False, "error": "No license key provided"}), 400

    # Verify against Gumroad API
    product_id = "Yy0-R0fZjEp086GA-eJlBw=="
    try:
        payload = json.dumps({
            "product_id": product_id,
            "license_key": key,
            "increment_uses_count": True
        }).encode()
        req = urllib.request.Request(
            "https://api.gumroad.com/v2/licenses/verify",
            data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "stats-card/2.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            if result.get("success") and result.get("uses", 0) <= 3:
                # Register key
                h = hashlib.sha256(key.encode()).hexdigest()[:16]
                VALID_KEYS.add(h)
                # Persist to keyfile
                keyfile = os.path.join(os.path.dirname(__file__), "valid_keys.txt")
                with open(keyfile, "a") as f:
                    f.write(f"{h}\n")
                return jsonify({"valid": True, "message": "License activated! Premium features unlocked."})
            elif result.get("uses", 0) > 3:
                return jsonify({"valid": False, "error": "License key usage limit exceeded"}), 403
            else:
                return jsonify({"valid": False, "error": "Invalid license key"}), 403
    except urllib.error.HTTPError as e:
        return jsonify({"valid": False, "error": f"Verification failed: {e.code}"}), 403
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)}), 500


@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "stats-card", "version": "2.0", "premium_keys": len(VALID_KEYS)})


def escape(s):
    if not isinstance(s, str):
        s = str(s)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")


if __name__ == '__main__':
    load_license_keys()
    app.run(host='0.0.0.0', port=int(sys.argv[1]) if len(sys.argv) > 1 else 8083, debug=False)