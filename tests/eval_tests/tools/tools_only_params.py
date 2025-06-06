import datetime
import math
import re
from llama_stack_client.lib.agents.client_tool import client_tool


@client_tool
def add_two_numbers(a: float, b: float) -> float:
    """
    :param a: The first number.
    :param b: The second number.
    """
    return a + b

@client_tool
def subtract_two_numbers(a: float, b: float) -> float:
    """
    :param a: The number to subtract from.
    :param b: The number to subtract.
    """
    return a - b

@client_tool
def multiply_two_numbers(a: float, b: float) -> float:
    """
    :param a: The first number.
    :param b: The second number.
    """
    return a * b

@client_tool
def divide_two_numbers(a: float, b: float) -> float:
    """
    :param a: The dividend.
    :param b: The divisor.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

@client_tool
def get_current_date() -> str:
    """
    """
    return datetime.date.today().strftime("%Y-%m-%d")

@client_tool
def greet_user(name: str) -> str:
    """
    :param name: The name of the user to greet.
    """
    return f"Hello, {name}!"

@client_tool
def string_length(text: str) -> int:
    """
    :param text: The input string.
    """
    return len(text)

@client_tool
def to_uppercase(text: str) -> str:
    """
    :param text: The input string.
    """
    return text.upper()

@client_tool
def to_lowercase(text: str) -> str:
    """
    :param text: The input string.
    """
    return text.lower()

@client_tool
def reverse_string(text: str) -> str:
    """
    :param text: The input string.
    """
    return text[::-1]

@client_tool
def is_even(number: int) -> bool:
    """
    :param number: The integer to check.
    """
    return number % 2 == 0

@client_tool
def is_odd(number: int) -> bool:
    """
    :param number: The integer to check.
    """
    return number % 2 != 0

@client_tool
def get_max_of_two(a: float, b: float) -> float:
    """
    :param a: The first number.
    :param b: The second number.
    """
    return max(a, b)

@client_tool
def get_min_of_two(a: float, b: float) -> float:
    """
    :param a: The first number.
    :param b: The second number.
    """
    return min(a, b)

@client_tool
def concatenate_strings(s1: str, s2: str) -> str:
    """
    :param s1: The first string.
    :param s2: The second string.
    """
    return s1 + s2

@client_tool
def is_palindrome(text: str) -> bool:
    """
    :param text: The input string.
    """
    processed_text = "".join(char.lower() for char in text if char.isalnum())
    return processed_text == processed_text[::-1]

@client_tool
def calculate_square_root(number: float) -> float:
    """
    :param number: The non-negative number.
    """
    if number < 0:
        raise ValueError("Cannot calculate square root of a negative number.")
    return number**0.5

@client_tool
def power(base: float, exponent: float) -> float:
    """
    :param base: The base number.
    :param exponent: The exponent.
    """
    return base ** exponent

@client_tool
def get_day_of_week(date_string: str) -> str:
    """
    :param date_string: The date in YYYY-MM-DD format.
    """
    date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    return date_object.strftime("%A")

@client_tool
def email_validator(email: str) -> bool:
    """
    :param email: The email string to validate.
    """
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None

@client_tool
def count_words(text: str) -> int:
    """
    :param text: The input string.
    """
    words = text.split()
    return len(words)

@client_tool
def average_two_numbers(a: float, b: float) -> float:
    """
    :param a: The first number.
    :param b: The second number.
    """
    return (a + b) / 2

@client_tool
def remove_whitespace(text: str) -> str:
    """
    :param text: The input string.
    """
    return "".join(text.split())

@client_tool
def convert_celsius_to_kelvin(celsius: float) -> float:
    """"
    :param celsius: The temperature in Celsius.
    """
    return celsius + 273.15

@client_tool
def convert_fahrenheit_to_kelvin(fahrenheit: float) -> float:
    """"
    :param fahrenheit: The temperature in Fahrenheit.
    """
    return (fahrenheit - 32) * 5/9 + 273.15

@client_tool
def convert_celsius_to_fahrenheit(celsius: float) -> float:
    """
    :param celsius: The temperature in Celsius.
    """
    return (celsius * 9/5) + 32

@client_tool
def convert_fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    :param fahrenheit: The temperature in Fahrenheit.
    """
    return (fahrenheit - 32) * 5/9

@client_tool
def get_substring(text: str, start_index: int, end_index: int) -> str:
    """
    :param text: The input string.
    :param start_index: The starting index (inclusive).
    :param end_index: The ending index (exclusive).
    """
    return text[start_index:end_index]

@client_tool
def round_number(number: float, decimal_places: int) -> float:
    """
    :param number: The float number to round.
    :param decimal_places: The number of decimal places to round to.
    """
    return round(number, decimal_places)

@client_tool
def is_leap_year(year: int) -> bool:
    """
    :param year: The year to check.
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

@client_tool
def generate_random_integer(min_value: int, max_value: int) -> int:
    """
    :param min_value: The minimum value for the random integer.
    :param max_value: The maximum value for the random integer.
    """
    import random
    return random.randint(min_value, max_value)

@client_tool
def get_file_extension(filename: str) -> str:
    """
    :param filename: The input filename (e.g., "document.pdf").
    """
    return filename.split('.')[-1] if '.' in filename else ""

@client_tool
def replace_substring(text: str, old_substring: str, new_substring: str) -> str:
    """
    :param text: The original string.
    :param old_substring: The substring to be replaced.
    :param new_substring: The substring to replace with.
    """
    return text.replace(old_substring, new_substring)

@client_tool
def is_prime(number: int) -> bool:
    """
    :param number: The integer to check.
    """
    if number < 2:
        return False
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True

@client_tool
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    :param weight_kg: The weight in kilograms.
    :param height_m: The height in meters.
    """
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    return weight_kg / (height_m ** 2)

@client_tool
def convert_kilograms_to_pounds(kg: float) -> float:
    """
    :param kg: The weight in kilograms.
    """
    return kg * 2.20462

@client_tool
def convert_pounds_to_kilograms(lb: float) -> float:
    """
    :param lb: The weight in pounds.
    """
    return lb / 2.20462

@client_tool
def convert_meters_to_feet(meters: float) -> float:
    """
    :param meters: The length in meters.
    """
    return meters * 3.28084

@client_tool
def convert_feet_to_meters(feet: float) -> float:
    """
    :param feet: The length in feet.
    """
    return feet / 3.28084

@client_tool
def is_alphanumeric(text: str) -> bool:
    """
    :param text: The input string.
    """
    return text.isalnum()

@client_tool
def url_encode(text: str) -> str:
    """
    :param text: The string to URL-encode.
    """
    import urllib.parse
    return urllib.parse.quote_plus(text)

@client_tool
def url_decode(text: str) -> str:
    """
    :param text: The string to URL-decode.
    """
    import urllib.parse
    return urllib.parse.unquote_plus(text)
