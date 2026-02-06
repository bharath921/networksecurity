from pathlib import Path
from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    requirement_lst: list[str] = []
    requirements_path = Path(__file__).parent / "requirements.txt"
    try:
        with requirements_path.open("r", encoding="utf-8") as file:
            #Read lines from the file
            lines =file.readlines()
            for line in lines:
                requirement=line.strip()

                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)
                

    except FileNotFoundError:
        print(f"requirements.txt file not found at: {requirements_path}")
    return requirement_lst
setup(
    name='network_security_project',
    version='0.0.1',
    author='Bharath',
    author_email='bharathakula@gmail.com',
    install_requires=get_requirements()
)

