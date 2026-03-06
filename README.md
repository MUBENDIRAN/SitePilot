# SitePilot 🚀

SitePilot is an AI-powered static website generator and deployment engine that allows you to update your website directly from your phone via Telegram. It uses local LLMs to process natural language requests and automatically deploys changes to GitHub Pages.

## 🛠 Tech Stack

| Technology | Role | Why? |
| :--- | :--- | :--- |
| **Python 3.12+** | Core Logic | The industry standard for AI orchestration and automation scripts. |
| **Ollama (Llama 3.1:8b)** | AI Engine | Provides powerful, local LLM capabilities without the need for expensive API subscriptions or privacy concerns. |
| **Telegram Bot API** | User Interface | Offers a cross-platform, ready-made mobile/desktop UI, eliminating the need to build and host a custom frontend. |
| **Git / GitHub Pages** | CI/CD & Hosting | Industry-standard version control paired with free, reliable static site hosting. |
| **python-dotenv** | Config Management | Securely handles sensitive credentials like Telegram tokens outside of the codebase. |

## ❓ Why this stack?

1.  **Privacy & Cost:** By using **Ollama**, all AI processing happens locally on your machine. There are no recurring API costs (like OpenAI) and your data never leaves your infrastructure.
2.  **Zero-Friction UI:** Building a custom web dashboard takes time. **Telegram** provides instant notifications, command handling, and a familiar interface accessible from any device.
3.  **Autonomous Deployment:** The integration with **Git subprocesses** means the transition from "AI thought" to "Live website" is fully automated. If the AI generates it, it's live in seconds.

## 💡 The Problem It Solves

Traditional web development—even for small changes—requires a laptop, a code editor, Git commands, and a deployment step. **SitePilot** bridges the gap between **intent** and **production**:

-   **Mobile-First Development:** Change your website's header or add a new blog post while walking down the street using a simple Telegram message.
-   **Rapid Prototyping:** Skip the boilerplate. Describe your idea in plain English and let the LLM handle the HTML/CSS structure.
-   **Automated CI/CD:** No need to manually run `git add`, `commit`, and `push`. The system handles the entire lifecycle from generation to deployment.

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- [Ollama](https://ollama.com/) installed and running `llama3.1:8b`.
- A Telegram Bot Token (from [@BotFather](https://t.me/botfather)).

### Installation
1.  Clone the repo:
    ```bash
    git clone https://github.com/yourusername/MCP.git
    cd MCP
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
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
2.  Open Telegram and send Eg:`/update Add a dark mode toggle to the homepage`.

## 📁 Project Structure
- `telegram_bot.py`: The entry point for user interaction.
- `mcp_server.py`: The core engine that talks to Ollama, parses file updates, and handles Git deployment.
- `site/`: Contains the actual website source code (HTML/CSS/JS).
