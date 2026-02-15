# OpenClaw Skill Project

This project is a boilerplate for developing OpenClaw skills that require Python scripts and external `.whl` libraries.

## Project Structure

- `SKILL.md`: Skill definition for OpenClaw.
- `scripts/`: Python scripts.
- `libs/`: Directory for `.whl` files and other local dependencies.
- `requirements.txt`: Python dependency list.

## Usage

1.  Place your `.whl` files in the `libs/` directory.
2.  Add them to `requirements.txt` if they need to be installed via pip.
3.  Write your logic in `scripts/main.py`.
4.  Run your scripts as defined in `SKILL.md`.
