def ask_required(prompt):
    while (v := input(prompt).strip()) == "":
        print("Required field.")
    return v


def ask_int(prompt, default):
    while True:
        v = input(prompt).strip()
        if not v:
            return default
        if v.isdigit():
            return int(v)
        print("Enter a valid number.")


def ask_skills(prompt, default="3"):
    while True:
        v = input(prompt).strip()
        if not v:
            return [default]

        skills = [s.strip() for s in v.split(",") if s.strip()]
        if skills:
            return skills

        print("Enter at least one skill ID.")