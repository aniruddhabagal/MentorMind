# MentorMind - AI-Powered Tutoring System

**MentorMind** is an AI-powered tutoring system designed to provide personalized learning experiences using advanced language models. Built with modular components, it adapts to students' learning needs through interactive lessons, assessments, and feedback. The system leverages a graph-based structure to manage learning flows, integrates **Google Gemini** for AI capabilities, and includes specialized tools for subjects like math, science, and language arts.

---

## Key Features

- **Adaptive Learning**: Tailors lessons based on student progress and understanding.
- **Graph-Based Tutoring**: Uses a structured flow for seamless learning experiences.
- **Multi-Subject Support**: Includes dedicated tools for math, science, and language.
- **Assessment & Feedback**: Provides real-time evaluations to guide student improvement.
- **Scalable AI Integration**: Powered by **Google Gemini** for intelligent tutoring.

---

## Project Structure

```
ai_tutor/
│
├── backend/                     # FastAPI backend
│   ├── requirements.txt         # Backend dependencies
│   ├── .env                     # Environment variables (Google Gemini API key)
│   ├── main.py                  # FastAPI application entry point
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration settings
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py        # API endpoints
│   │   │   └── dependencies.py  # API dependencies
│   │   │
│   │   ├── tools/               # Educational tools for various subjects
│   │   │   ├── __init__.py
│   │   │   ├── math_tools.py
│   │   │   ├── science_tools.py
│   │   │   ├── language_tools.py
│   │   │   ├── assessment_tools.py
│   │   │   └── common_tools.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── student_model.py  # Student profile and learning state
│   │   │   └── llm_setup.py      # Google Gemini AI configuration
│   │   │
│   │   ├── graph/               # Graph structure for activity flow
│   │   │   ├── __init__.py
│   │   │   ├── nodes.py
│   │   │   ├── assistant.py
│   │   │   └── builder.py
│   │   │
│   │   ├── activities/          # Learning activities for different stages
│   │   │   ├── __init__.py
│   │   │   ├── introduction.py
│   │   │   ├── practice.py
│   │   │   ├── assessment.py
│   │   │   └── review.py
│   │   │
│   │   └── prompts/             # Predefined prompts for tutor interaction
│   │       ├── __init__.py
│   │       └── tutor_prompts.py
│
├── frontend/                    # React frontend
│   ├── package.json             # Frontend dependencies
│   ├── tailwind.config.js       # Tailwind CSS configuration
│   ├── public/                  # Static assets (e.g., images, icons)
│   │
│   └── src/
│       ├── App.jsx              # Main application component
│       ├── index.jsx            # Application entry point
│       ├── assets/              # Images, fonts, and other static assets
│       ├── components/          # Reusable UI components
│       │   ├── Chat/            # Chat interface components
│       │   ├── Dashboard/       # Dashboard UI components
│       │   ├── Layout/          # Layout components (header, footer)
│       │   ├── StudentProfile/  # Profile components (student info, progress)
│       │   └── common/          # Common UI elements (buttons, inputs)
│       │
│       ├── hooks/               # Custom React hooks
│       ├── contexts/            # React context providers for global state
│       ├── services/            # API client services (for backend interaction)
│       ├── pages/               # Application pages and routes
│       ├── utils/               # Utility functions and helpers
│       └── styles/              # Global styles and Tailwind imports
│
└── README.md                    # Project documentation
```

## Backend (FastAPI)

The backend is powered by **FastAPI**, providing a fast and efficient API layer for communication with the frontend and integration with **Google Gemini** for intelligent AI-powered tutoring.

### Key Components

- **`main.py`**: The entry point of the FastAPI application, where the server is initialized and API routes are defined.
- **`app/config.py`**: Contains configuration settings for the backend, including AWS API keys and other critical parameters.
- **`app/api/routes.py`**: Defines the API endpoints for handling user interactions and AI communication.
- **`app/tools/`**: Contains various tools for handling subject-specific operations like math, science, and language tutoring.
- **`app/models/`**: Contains models like `student_model.py`, which tracks student progress and learning state.
- **`app/activities/`**: Contains different activity types such as practice, assessment, review, and introduction, which the tutor will guide the student through.
- **`app/prompts/`**: Houses predefined prompts that are used to interact with the AI tutor.

### Installation

1. Clone the repository.
2. Navigate to the `backend/` directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your Google Gemini API key:
   ```env
   Gemini_API_KEY=your_api_key_here
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

## Frontend (React)

The frontend is built with **React** and styled using **Tailwind CSS**. It provides an interactive interface for students to interact with the AI tutor, manage their profile, and access learning activities.

### Key Components

- **`App.jsx`**: The root component that holds the main structure of the application.
- **`src/components/`**: Contains reusable UI components like the chat interface, dashboard, student profile, and layout elements.
- **`src/hooks/`**: Contains custom hooks to manage state and logic across components.
- **`src/services/`**: Includes functions for making API calls to the backend.
- **`src/styles/`**: Contains global styles and Tailwind CSS configurations.
- **`src/pages/`**: Houses different pages, including the dashboard and profile pages.

### Installation

1. Navigate to the `frontend/` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm start
   ```

## Contributing

We welcome contributions to this project! If you have suggestions, improvements, or fixes, feel free to fork the repository and submit a pull request.
