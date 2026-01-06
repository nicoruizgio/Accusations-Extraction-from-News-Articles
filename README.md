# Accusation Extraction Playground

This is a standalone playground for extracting accusations from text using LangChain and OpenAI.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd playground
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Configuration:**
    *   Copy `.env.template` to a new file named `.env`:
        ```bash
        cp .env.template .env
        ```
    *   Open `.env` and add your OpenAI API key:
        ```
        OPENAI_API_KEY=sk-...
        ```

## Usage

1.  Open `playground.py` and paste your article text or passage into the `ARTICLE_TEXT` variable. 
2.  Run the script:
    ```bash
    python playground.py
    ```
3.  The script will output the extracted relationships to the console.
