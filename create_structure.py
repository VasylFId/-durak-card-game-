import os

# Define the structure of directories and files
structure = {
    "app": [
        "__init__.py",
        "models.py",
        "routes.py",
        "forms.py",
        {
            "templates": [
                "base.html",
                "register.html"
            ]
        },
        {
            "static": [
                {
                    "css": [
                        "styles.css"
                    ]
                },
                {
                    "js": []
                },
                {
                    "img": []
                }
            ]
        }
    ],
    "tests": [
        "__init__.py",
        "test_registration.py"
    ],
    ".github": [
        {
            "workflows": [
                "ci.yml"
            ]
        }
    ],
    ".gitignore": None,
    "README.md": None,
    "requirements.txt": None,
    "Dockerfile": None,
    "docker-compose.yml": None,
    "config.py": None,
    "run.py": None
}

def create_structure(base_path, structure):
    for key, value in structure.items():
        path = os.path.join(base_path, key)
        if isinstance(value, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, value)
        elif isinstance(value, list):
            os.makedirs(path, exist_ok=True)
            for item in value:
                if isinstance(item, dict):
                    create_structure(path, item)
                else:
                    open(os.path.join(path, item), 'w').close()
        else:
            open(path, 'w').close()

# Create the project structure
create_structure('.', structure)

print("Project structure created successfully.")
