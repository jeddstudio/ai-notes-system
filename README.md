# ai-notes-system
AI-powered note-taking system built with FastAPI, MongoDB, and Streamlit. Features smart note structuring, Feynman summaries, and bilingual support (EN/CN). Demonstrates full-stack development skills and AI integration for Python engineering portfolio.



## Setup
---
1. Create a Repo on GitHub
2. Clone the repo to local machine
3. Create a virtual environment
4. Install dependencies
5. Setup gitignore
6. Create directories
```sh
# Create directories
mkdir src
cd src
mkdir database components utils
touch database/__init__.py database/mongodb.py
touch components/__init__.py components/note_processor.py components/ui_components.py
touch utils/__init__.py utils/helpers.py
touch main.py
cd ..
mkdir tests
touch tests/__init__.py
```
7. Create a .env file Setup
```sh
echo "MONGODB_URL=your_mongodb_url
OPENAI_API_KEY=your_openai_key" > .env
```

---

## Features
- Create and save notes with title and content
- Automatic timestamp for each note
- View all notes in an expandable list
- Copy notes in markdown format to clipboard
- Delete unwanted notes
- MongoDB integration for persistent storage
- Bilingual support (EN/CN)
- Streamlit-based user interface

## Implementation
---
1. Basic MongoDB setup
    - `src/database/mongodb.py`
2. Note Processor
    - `src/components/note_processor.py`
3. Basic UI with features:
    - `src/main.py`
    - Note creation and storage
    - Note viewing and management
    - Markdown format copying
    - Note deletion
4. Basic Test File 
    - `tests/testing.py`
    - I am still practicing how to use pytest
    - Create a pytest.ini file
        ```sh
        echo "[pytest]
        pythonpath = src" > pytest.ini
        ```

> [!NOTE] 
> I am still practising how to use pytest
---



## Installation Instructions
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/ai-notes-system.git
   cd ai-notes-system
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   - Create a `.env` file in the root directory
   - Add your MongoDB URL and OpenAI API key:
     ```
     MONGODB_URL=your_mongodb_url
     OPENAI_API_KEY=your_openai_key
     ```

## Usage Guide
1. Start the application:
   ```sh
   cd src
   python main.py
   ```

2. Access the web interface:
   - Open your web browser
   - Navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Using the Note-Taking System:
   - Create new notes using the input form
   - Notes will be automatically processed and structured
   - Use the search functionality to find specific notes
   - Toggle between English and Chinese language support as needed

4. Running Tests:
   ```sh
   pytest tests/
   ```

---

## Project Structure
```
ai-notes-system/
├── venv/
├── src/
│   ├── main.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── mongodb.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── note_processor.py
│   │   └── ui_components.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   └── __init__.py
├── requirements.txt
└── README.md
```


Error Handling Section

```markdown
## Troubleshooting

### MongoDB Connection
If you encounter MongoDB connection issues:

1. Ensure MongoDB is installed and running:
```bash
# Check MongoDB status (macOS)
brew services list

# Start MongoDB if not running
brew services start mongodb-community
```

1. Verify your connection string in .env:

```
MONGODB_URL=mongodb://localhost:27017
```

1. Test MongoDB connection:

```bash
mongosh
```



#### Development Section
```markdown
## Development

### Version Control
- We use Semantic Versioning (MAJOR.MINOR.PATCH)
- Current version: 0.2.0
- Commit messages follow conventional commits format

### Feature Demonstration
![AI Notes System Demo](docs/images/demo.gif)