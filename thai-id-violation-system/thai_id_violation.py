import cv2
import pytesseract
import re
import argparse
from datetime import datetime
from dateutil import parser


def preprocess_image(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Image not found.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Light noise reduction only
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    return gray

def extract_text(image):
    custom_config = r'-l tha+eng --oem 3 --psm 6'
    return pytesseract.image_to_string(image, config=custom_config)


# -------------------- ID NUMBER --------------------

def extract_id_number(text):
    lines = text.split("\n")

    for line in lines:
        if "Identification Number" in line:
            match = re.search(r'(\d[\d\s]{10,})', line)
            if match:
                return match.group().strip()

    # fallback (old method)
    pattern = r"\d{1}\s?\d{4}\s?\d{5}\s?\d{2}\s?\d{1}"
    match = re.search(pattern, text)
    return match.group() if match else "Not Found"


# -------------------- THAI NAME --------------------

def extract_thai_name(text):
    # Find English title position
    eng_match = re.search(r'(Mr\.|Mrs\.|Miss)', text)

    if not eng_match:
        return "Not Found"

    # Take text BEFORE English name
    before_text = text[:eng_match.start()]

    # Extract all Thai words there
    thai_words = re.findall(r'[ก-๙]+', before_text)

    if len(thai_words) >= 2:
        return " ".join(thai_words[-2:])

    return "Not Found"


# -------------------- ENGLISH NAME --------------------

def extract_english_name(text):
    # Extract first name with title
    first_match = re.search(r'(Mr\.|Mrs\.|Miss)\s+[A-Za-z]+', text)
    if not first_match:
        return "Not Found"

    first_part = first_match.group()

    # Extract last name specifically after "Last Name"
    last_match = re.search(r'Last\s*Name\s*([A-Za-z]+)', text)

    if last_match:
        last_part = last_match.group(1)
        return f"{first_part} {last_part}"

    return first_part


# -------------------- BIRTHDATE --------------------

def extract_birthdate(text):
    match = re.search(r'Date of Birth\s*(\d{1,2}.*?\d{4})', text)

    if match:
        date_text = match.group(1)

        # Clean weird characters
        date_text = re.sub(r'[^A-Za-z0-9\s]', '', date_text)

        return date_text.strip()

    return None


def calculate_age(birthdate_str):
    try:
        birthdate = parser.parse(birthdate_str, dayfirst=True)
        today = datetime.today()

        age = today.year - birthdate.year - (
            (today.month, today.day) < (birthdate.month, birthdate.day)
        )

        return age

    except:
        return "Unknown"


# -------------------- VIOLATION --------------------

def assign_violation():
    violations = {
        "1": "Speeding",
        "2": "Red Light Violation",
        "3": "No Helmet"
    }

    print("\nSelect Traffic Violation:")
    for key, value in violations.items():
        print(f"{key}. {value}")

    choice = input("Enter choice (1-3): ")
    return violations.get(choice, "Unknown Violation")


# -------------------- MAIN --------------------

def main():
    parser_arg = argparse.ArgumentParser(description="Thai ID Card OCR AI")
    parser_arg.add_argument("--image", required=True, help="Path to ID card image")
    args = parser_arg.parse_args()

    processed_image = preprocess_image(args.image)
    text = extract_text(processed_image)

    print("\n--- RAW OCR TEXT ---\n")
    print(text)

    id_number = extract_id_number(text)
    thai_name = extract_thai_name(text)
    english_name = extract_english_name(text)
    birthdate = extract_birthdate(text)
    age = calculate_age(birthdate) if birthdate else "Unknown"

    print("\n--- EXTRACTED INFORMATION ---")
    print(f"ID Number: {id_number}")
    print(f"Thai Name: {thai_name}")
    print(f"English Name: {english_name}")
    print(f"Age: {age}")

    violation = assign_violation()
    print(f"\nAssigned Violation: {violation}")


if __name__ == "__main__":
    main()