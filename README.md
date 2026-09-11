# FossilAI

FossilAI is an experiment management and machine learning lifecycle platform. It provides a web interface and backend API for running, monitoring, and organizing machine learning experiments, datasets, and models.

## Features
- **Experiments**: Create, track, and run machine learning experiments using custom hyperparameters.
- **Datasets**: View and manage datasets used for training and evaluation.
- **Models**: Manage trained models, and use them to serve predictions.
- **Analytics & Replay**: Analyze model outputs and replay experiments.
- **Ticketing System**: Track issues and tasks directly alongside your experiments.

## Prerequisites
- **Python**: Version 3.8 or higher is recommended.
- **Git**: For version control.

## Setup Instructions

1. **Clone the Repository** (If you are pulling this from Git):
   ```bash
   git clone <repository_url>
   cd FossilAI
   ```

2. **Create a Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   Install all required Python packages via `pip`:
   ```bash
   pip install -r requirements.txt
   ```
   *(This will install Flask, Pandas, NumPy, Scikit-learn, and Joblib)*

## Running the Application

1. **Start the Backend Server**:
   From the root of the project directory, run:
   ```bash
   python -m web.backend.app
   ```

2. **Access the UI**:
   Open your web browser and navigate to:
   [http://localhost:5000](http://localhost:5000)
   The app will automatically redirect you to the main interface at `/ui/experiments.html`.

## Project Structure
- `web/backend/`: Contains the Flask API, blueprints, and server configuration.
- `web/frontend/`: Contains the HTML, CSS, and JS files for the user interface.
- `utils/`: Includes utility scripts for experiments, model inference, and other core functions.
- `datasets/`, `models/`, `experiments/`: Directories used by the app to store data, trained models, and experiment logs. (These are usually ignored in Git).

## Making It Git-Pushable
The project has been initialized with a `.gitignore` to avoid pushing cache files, virtual environments, Fossil version control artifacts, or large data/model directories. To push to a remote repository:
```bash
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your_remote_url>
git push -u origin main
```
