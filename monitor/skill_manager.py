import os
import subprocess

SKILLS_DIR = "skills"


class SkillManager:

    def __init__(self):
        os.makedirs(SKILLS_DIR, exist_ok=True)

    def skill_exists(self, failure):

        path = os.path.join(SKILLS_DIR, f"{failure}.sh")
        return os.path.exists(path)

    def write_skill(self, failure):

        path = os.path.join(SKILLS_DIR, f"{failure}.sh")

        script = f"""#!/bin/bash
echo "Executing recovery for {failure}"
sleep 1
echo "Recovery complete"
"""

        with open(path, "w") as f:
            f.write(script)

        os.chmod(path, 0o755)

        print(f"New skill created: {path}")

    def execute_skill(self, failure):

        path = os.path.join(SKILLS_DIR, f"{failure}.sh")

        if os.path.exists(path):

            print(f"Executing skill: {failure}")
            subprocess.call(["bash", path])

        else:

            print("Skill not found:", failure)