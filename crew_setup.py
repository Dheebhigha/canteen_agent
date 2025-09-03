from crewai import Agent, Task, Crew
from tools.face_tools import recognize_face, register_face
from services.db import get_all_registered
from services.sessions import can_serve, mark_served

# Tool wrappers
def run_register(name, image_path):
    """Registers a new face into the database."""
    return register_face(name, image_path)

def run_recognize(image_path):
    """Recognizes a face and decides meal eligibility."""
    identity = recognize_face(image_path)

    if identity is None:
        return "DENY_UNKNOWN"

    # Check session serving rules
    if not can_serve(identity):
        return "DENY_ALREADY_SERVED"

    # Mark as served
    mark_served(identity)
    return f"ALLOW:{identity}"

def run_list_registered():
    """Returns all registered employees."""
    return get_all_registered()

# CrewAI agent setup
canteen_agent = Agent(
    role="Canteen Manager",
    goal="Detect faces of employees and ensure they get food only once per session.",
    backstory="This agent manages food distribution in the canteen using facial recognition.",
    verbose=True,
    tools=[run_register, run_recognize, run_list_registered],
)

# Crew setup
crew = Crew(
    agents=[canteen_agent],
    tasks=[
        Task(description="Register a new employee face", agent=canteen_agent),
        Task(description="Recognize face and serve food", agent=canteen_agent),
        Task(description="List all registered employees", agent=canteen_agent),
    ]
)

# Helper functions for Streamlit or scripts
def register_employee(name, image_path):
    return run_register(name, image_path)

def recognize_employee(image_path):
    return run_recognize(image_path)

def list_employees():
    return run_list_registered()
