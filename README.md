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



##  Installation & Usage
pip install PyQt6

## Run the GUI application
py -m blogging gui

## Login credentials: 
username: user
password: 123456

---
## Screenshots available in `/screenshots` folder
