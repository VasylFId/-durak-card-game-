
# Durak Card Game

## Project Overview

Durak is a popular card game in Russia. This project is a web-based version of the game built using Python Flask. The application includes features like user registration, real-time gameplay using WebSockets, and an AI opponent.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Features

- User Registration and Authentication
- Real-time Gameplay with WebSockets
- AI Opponent using MiniMax and Monte Carlo Tree Search
- Responsive Design with Bootstrap
- Secure Communication with HTTPS

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- Node.js (for frontend development if using React or Vue)

### Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/durak-card-game.git
   cd durak-card-game
   ```

2. **Create a virtual environment and activate it:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   ```sh
   psql -c "CREATE DATABASE durak_db;"
   ```

5. **Configure the environment variables:**
   Create a `.env` file and add the following:
   ```
   SECRET_KEY=your_secret_key
   SQLALCHEMY_DATABASE_URI=postgresql://localhost/durak_db
   ```

6. **Run the application:**
   ```sh
   python run.py
   ```

## Usage

- Open your browser and navigate to `http://127.0.0.1:5000/`
- Register a new account
- Start a new game of Durak

## Project Structure

```
durak/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   ├── templates/
│   │   ├── base.html
│   │   └── register.html
│   └── static/
│       └── css/
│           └── styles.css
│
├── config.py
├── run.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── venv/
├── tests/
│   ├── __init__.py
│   └── test_registration.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── README.md
└── .gitignore
```

## Technologies Used

- **Backend:** Flask, Flask-SQLAlchemy, Flask-WTF, Flask-Bcrypt, Flask-Login, Flask-SocketIO
- **Frontend:** HTML, CSS, JavaScript, Bootstrap (optionally React.js or Vue.js)
- **Database:** PostgreSQL
- **Authentication:** JWT (JSON Web Tokens)
- **AI:** NumPy, SciPy
- **Testing:** pytest, Selenium
- **CI/CD:** GitHub Actions
- **Containerization:** Docker

## Contributing

Contributions are welcome! Please create a pull request with a clear description of your changes.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## License

Distributed under the MIT License. See `LICENSE` for more information.
