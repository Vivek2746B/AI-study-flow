# 🎓 AI Study Concierge: Your Personalized Learning Agent

**A Capstone Project for the Google 5-Day AI Agents Intensive Course.**

## 📖 Project Overview

The **AI Study Concierge** is an intelligent CLI agent designed to transform passive reading into active learning. Instead of just summarizing text, this agent acts as a personalized tutor. It digests complex topics from Wikipedia, direct questions, or PDF notes and automatically generates a structured study package tailored to your specific knowledge level.

Unlike basic chatbots, this agent employs an **agentic workflow** to route tasks, enforce structured JSON outputs, and provide "smart explanations" for quiz answers, simulating a real tutoring experience.

## ✨ Key Features

* **🤖 Agentic Workflow (Router):** Intelligently selects the correct data source tool—fetching live info from Wikipedia, processing local PDFs, or answering direct questions via the LLM.
* **🧠 Context Engineering:** Dynamic difficulty adjustment. The agent modifies its output style (vocabulary, depth, complexity) based on the user's selected level:
    * *Beginner:* Simple, analogy-heavy explanations.
    * *Intermediate:* Balanced structure.
    * *Advanced:* Technical, concise, and dense.
* **⚡ Smart Quiz Feedback:** It doesn't just say "Correct" or "Wrong." It provides a **reasoned explanation** for every answer, reinforcing learning immediately.
* **🎨 Professional CLI UI:** Built with the `Rich` library for a beautiful, terminal-based user experience featuring panels, colors, and markdown rendering.
* **💾 Observability & Structured Data:** All AI outputs are forced into a strict JSON schema and saved locally (`last_topic_output.json`), proving the agent's ability to handle structured data pipelines.

## 🛠️ Tech Stack

* **Core Logic:** Python
* **AI Model:** Google Gemini 2.5 Flash (via `google-generativeai`)
* **Knowledge Retrieval:** `wikipedia` API, `pypdf`
* **User Interface:** `rich` (for terminal formatting)
* **Environment Management:** `python-dotenv`

## 🚀 Installation & Setup

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/Vivek2746B/AI-study-flow.git
    cd ai-study-concierge
    ```

2.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Key**

    * Get your free API Key from [Google AI Studio](https://aistudio.google.com/).
    * Create a file named `.env` in the root folder.
    * Add your key:
        ```text
        GEMINI_API_KEY=your_api_key_here
        ```

## 🎮 How to Use

1.  **Run the Agent:**

    ```bash
    python main.py
    ```

2.  **Select Your Source:**

    * Option 1: Search for a broad topic (e.g., "Machine Learning").
    * Option 2: Ask a specific question (e.g., "Explain Quantum Entanglement").
    * Option 3: Upload a PDF (provide the file path to your notes).

3.  **Choose Difficulty:**

    * Type `beginner`, `intermediate`, or `advanced`.

4.  **Start Studying:**

    * **Read Summary:** Get a tailored overview of the topic.
    * **Flashcards:** Flip through key terms in the terminal.
    * **Take Quiz:** Test your knowledge and get instant AI feedback.

## 📂 Project Structure

```text
ai-study-concierge/
├── main.py                 # The User Interface (CLI & Menu Logic)
├── tools.py                # The "Brain" (API calls, PDF reading, Prompts)
├── requirements.txt        # List of python libraries
├── .env                    # API Key storage (not shared)
└── last_topic_output.json  # Auto-generated study data (Logs)
