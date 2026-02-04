##  Blogging System with MVC Architecture & PyQt6 GUI

A professional full-stack blogging application demonstrating modern software engineering principles with Model-View-Controller architecture, data persistence, and an intuitive graphical user interface.

##  Project Overview

This project implements a complete blogging system developed as part of a university software engineering course. The application features an architecture with clear separation of concerns and graphical user interfaces.

**Key Highlights:**

- **Dual Interfaces**: Both CLI (prototype) and GUI (production) implementations
- **Data Persistence**: JSON and Pickle-based DAO patterns for reliable data storage
- **Professional GUI**: Modern PyQt6 interface with table views and rich text editing
- **Comprehensive Testing**: Unit tests, integration tests, and controller tests

##  Team Collaboration

**Team Project** - Developed collaboratively by 2 computer science students:
- **Rida** : Blog management module, GUI layout, authentication system, and comprehensive testing suite
- **Yasaman**: Post management module, text editing interface, and data persistence layer
 We employed pair programming and feature-based development, with regular code reviews and integration sessions because ending up with errors is not in our dictionaries.

##  Features

###  User Management
- Secure login/logout system
- Session management
- User authentication workflow

###  Blog Management 
- Create, read, update, search and delete blogs
- QTableView widget for structured data display
- Current blog selection system
- JSON-based persistence with custom encoder/decoder

###  Post Management
- Rich text post creation and editing
- QPlainTextEdit widget for content management
- Post CRUD operations within selected blogs
- Pickle-based serialization for post data


##  Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Language** | Python 3.9+ | Core implementation |
| **GUI Framework** | PyQt6 | Professional desktop interface |
| **Data Persistence** | JSON + Pickle | Reliable data storage |
| **Testing** | unittest Framework | Quality assurance |

##  Project Structure
blogging-system/
├── blogging/
│ ├── main.py # Application entry point
│ ├── controller.py # Business logic layer
│ ├── blog.py # Blog domain model (My focus)
│ ├── post.py # Post domain model
│ ├── gui/ # PyQt6 interface components
│ │ ├── blogging_gui.py # Main application window
│ │ └── [widgets/] # Custom GUI components
│ ├── dao/ # Data Access Objects
│ │ ├── blog_dao_json.py
│ │ └── post_dao_pickle.py
│ ├── exception/ # Custom exception classes
│ └── cli/ # Command-line interface
├── tests/ # Comprehensive test suite
├── data/ # Persistent storage
└── requirements.txt # Dependencies



##  Installation & Usage

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation
# Clone repository
git clone https://github.com/yourusername/blogging-system-mvc-gui.git
cd blogging-system-mvc-gui

# Install dependencies
pip install PyQt6

# Run the GUI application
python3 -m blogging gui

# Or run the CLI prototype
python3 -m blogging cli


# Run unit tests
python -m pytest tests/

# Run specific test modules
python -m pytest tests/blog_test.py
python -m pytest tests/post_test.py
