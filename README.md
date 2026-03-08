# SitePilot 🚀

SitePilot is an AI-powered static website generator and deployment engine that allows you to update your website directly from your phone via Telegram. It uses local LLMs to process natural language requests and automatically deploys changes to GitHub Pages.

## 🛠 Tech Stack

| Technology | Role | Why? |
| :--- | :--- | :--- |
| **Python 3.12+** | Core Logic | The industry standard for AI orchestration and automation scripts. |
| **Ollama (Qwen2.5-Coder:7b)** | AI Engine | Optimized for coding tasks, providing powerful local LLM capabilities without API costs. |
| **Telegram Bot API** | User Interface | Offers a cross-platform, ready-made mobile/desktop UI for instant interaction. |
| **Git / GitHub Pages** | CI/CD & Hosting | Industry-standard version control paired with free, reliable static site hosting. |
| **python-dotenv** | Config Management | Securely handles sensitive credentials like Telegram tokens. |

## ❓ Why this stack?

1.  **Privacy & Cost:** By using **Ollama**, all AI processing happens locally. No recurring API costs and your data stays private.
2.  **Zero-Friction UI:** No custom frontend needed. **Telegram** provides instant notifications, command handling, and a familiar interface on any device.
3.  **Autonomous Deployment:** Integrated **Git automation** handles the transition from "AI generation" to "Live production" in seconds.

## 💡 The Problem It Solves

Traditional web development—even for small changes—requires a laptop, a code editor, Git commands, and a deployment step. **SitePilot** bridges the gap:

-   **Mobile-First Development:** Update your website's header or add a new section while on the go using a simple Telegram message.
-   **Rapid Prototyping:** Describe your idea in plain English and let the LLM handle the HTML/CSS structure.
-   **Automated CI/CD:** The system handles the entire lifecycle: reading files, generating code, committing, and pushing to production.

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- [Ollama](https://ollama.com/) installed and running `qwen2.5-coder:7b`.
- A Telegram Bot Token (from [@BotFather](https://t.me/botfather)).

### Installation
1.  Clone the repo:
    ```bash
    git clone https://github.com/yourusername/MCP.git
    cd MCP
    ```
2.  Install dependencies:
    ```bash
    pip install python-telegram-bot requests ollama python-dotenv
    ```
    
    
3.  Configure environment:
    Create a `.env` file:
    ```env
    TELEGRAM_TOKEN=your_bot_token_here
    TELEGRAM_NOTIFY_IDS=your_chat_id_1,your_chat_id_2
    ```

### Running
1.  Start the Telegram bot:
    ```bash
    python telegram_bot.py
    ```
2.  Open Telegram and send a command:
    Example: `/pilot Add a dark mode toggle to the homepage`.

## 📁 Project Structure
- `telegram_bot.py`: The entry point for Telegram interaction.
- `mcp_server.py`: The core engine that interacts with Ollama, parses file updates, and handles Git deployment.
- `site/`: Contains the actual website source code (HTML/CSS/JS).
- `.github/workflows/`: Contains the GitHub Actions for automated deployment to GitHub Pages.
