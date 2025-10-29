"""
Utilities: logging setup and grade validation.
"""
import logging
import os

def setup_logging(log_path: str = None) -> None:
    """
    Configure logging to write logs/app.log (INFO + ERROR).
    """
    log_path = log_path or os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "app.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def parse_grade(text: str) -> float:
    """
    Parse and validate a grade string (0–100).
    Raises ValueError if invalid.
    """
    try:
        g = float(text)
    except Exception:
        raise ValueError("Grade must be a number.")
    if not (0 <= g <= 100):
        raise ValueError("Grade must be between 0 and 100.")
    return g
