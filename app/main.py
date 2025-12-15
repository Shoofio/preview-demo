"""
Preview Environment Demo App
A simple Flask app that displays build information to demonstrate
ephemeral preview environments with ArgoCD + GitHub Actions.
"""

import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Build info injected at container build time
BUILD_INFO = {
    "commit_sha": os.environ.get("COMMIT_SHA", "unknown"),
    "commit_sha_short": os.environ.get("COMMIT_SHA", "unknown")[:7],
    "pr_number": os.environ.get("PR_NUMBER", "N/A"),
    "branch": os.environ.get("BRANCH_NAME", "unknown"),
    "build_time": os.environ.get("BUILD_TIME", "unknown"),
    "image_tag": os.environ.get("IMAGE_TAG", "unknown"),
}

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Preview Environment Demo</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-card: #21262d;
            --border: #30363d;
            --text-primary: #f0f6fc;
            --text-secondary: #8b949e;
            --accent-green: #3fb950;
            --accent-blue: #58a6ff;
            --accent-purple: #a371f7;
            --accent-orange: #f0883e;
            --accent-pink: #f778ba;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Outfit', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background-image: 
                radial-gradient(circle at 20% 80%, rgba(63, 185, 80, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(88, 166, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(163, 113, 247, 0.05) 0%, transparent 40%);
        }
        
        .container {
            max-width: 600px;
            width: 90%;
            animation: fadeIn 0.6s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-green), var(--accent-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }
        
        .header .subtitle {
            color: var(--text-secondary);
            font-size: 1.1rem;
        }
        
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: var(--bg-card);
            border: 1px solid var(--accent-green);
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            margin-top: 1rem;
            font-size: 0.9rem;
        }
        
        .status-badge .dot {
            width: 8px;
            height: 8px;
            background: var(--accent-green);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .card {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 1rem;
        }
        
        .card-header {
            background: var(--bg-card);
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border);
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .card-body {
            padding: 1.5rem;
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--border);
        }
        
        .info-row:last-child {
            border-bottom: none;
        }
        
        .info-label {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
        
        .info-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            background: var(--bg-card);
            padding: 0.25rem 0.75rem;
            border-radius: 6px;
        }
        
        .info-value.highlight-green { color: var(--accent-green); }
        .info-value.highlight-blue { color: var(--accent-blue); }
        .info-value.highlight-purple { color: var(--accent-purple); }
        .info-value.highlight-orange { color: var(--accent-orange); }
        .info-value.highlight-pink { color: var(--accent-pink); }
        
        .pr-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink));
            padding: 0.25rem 0.75rem;
            border-radius: 6px;
            font-weight: 600;
        }
        
        .footer {
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.85rem;
            margin-top: 2rem;
        }
        
        .footer a {
            color: var(--accent-blue);
            text-decoration: none;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Preview Environment</h1>
            <p class="subtitle">Ephemeral deployment powered by ArgoCD</p>
            <div class="status-badge">
                <span class="dot"></span>
                <span>Environment Active</span>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">
                📋 Build Information
            </div>
            <div class="card-body">
                <div class="info-row">
                    <span class="info-label">Pull Request</span>
                    {% if pr_number != "N/A" %}
                    <span class="pr-badge">#{{ pr_number }}</span>
                    {% else %}
                    <span class="info-value">N/A</span>
                    {% endif %}
                </div>
                <div class="info-row">
                    <span class="info-label">Branch</span>
                    <span class="info-value highlight-blue">{{ branch }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Commit SHA</span>
                    <span class="info-value highlight-purple">{{ commit_sha_short }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Full SHA</span>
                    <span class="info-value" style="font-size: 0.7rem;">{{ commit_sha }}</span>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">
                🐳 Container Information
            </div>
            <div class="card-body">
                <div class="info-row">
                    <span class="info-label">Image Tag</span>
                    <span class="info-value highlight-green">{{ image_tag }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Build Time</span>
                    <span class="info-value highlight-orange">{{ build_time }}</span>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>This environment will be automatically deleted when the PR is closed.</p>
            <p style="margin-top: 0.5rem;">
                Built with ❤️ using 
                <a href="https://argoproj.github.io/cd/" target="_blank">ArgoCD</a> + 
                <a href="https://github.com/features/actions" target="_blank">GitHub Actions</a>
            </p>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(TEMPLATE, **BUILD_INFO)

@app.route("/health")
def health():
    return {"status": "healthy", "build": BUILD_INFO}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

