import datetime
import math
import re
from llama_stack_client.lib.agents.client_tool import client_tool


@client_tool
def add_two_numbers(a: float, b: float) -> float:
    """
    :description: Adds two numbers.
    :use_case: Use when the user wants to find the sum, total, or combined value of two numbers.
    :param a: The first number.
    :param b: The second number.
    :returns: The sum of `a` and `b`.
    """
    return a + b

@client_tool
def subtract_two_numbers(a: float, b: float) -> float:
    """
    :description: Subtracts the second number from the first.
    :use_case: Use when the user wants to find the difference, subtract one number from another, or determine how much is left after removal.
    :param a: The number to subtract from.
    :param b: The number to subtract.
    :returns: The difference between `a` and `b`.
    """
    return a - b

@client_tool
def multiply_two_numbers(a: float, b: float) -> float:
    """
    :description: Multiplies two numbers.
    :use_case: Use when the user wants to find the product, multiply values, or scale a quantity.
    :param a: The first number.
    :param b: The second number.
    :returns: The product of `a` and `b`.
    """
    return a * b

@client_tool
def divide_two_numbers(a: float, b: float) -> float:
    """
    :description: Divides the first number by the second.
    :use_case: Use when the user wants to find the quotient, ratio, or split a quantity. Handles division by zero.
    :param a: The dividend.
    :param b: The divisor.
    :returns: The quotient of `a` divided by `b`.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

@client_tool
def get_current_date() -> str:
    """
    :description: Retrieves the current date.
    :use_case: Use when the user asks for "today's date", "current date", or similar date inquiries.
    :returns: The current date in YYYY-MM-DD format.
    """
    return datetime.date.today().strftime("%Y-%m-%d")

@client_tool
def greet_user(name: str) -> str:
    """
    :description: Generates a personalized greeting message.
    :use_case: Use when the user provides a name and a greeting is implied or explicitly requested.
    :param name: The name of the user to greet.
    :returns: A personalized greeting message.
    """
    return f"Hello, {name}!"

@client_tool
def string_length(text: str) -> int:
    """
    :description: Calculates the length of a given string.
    :use_case: Use when the user asks for the "length of", "character count", or "how many characters" in a text.
    :param text: The input string.
    :returns: The number of characters in the string.
    """
    return len(text)

@client_tool
def to_uppercase(text: str) -> str:
    """
    :description: Converts a string to uppercase.
    :use_case: Use when the user requests "all caps", "uppercase", or to "capitalize everything".
    :param text: The input string.
    :returns: The string converted to uppercase.
    """
    return text.upper()

@client_tool
def to_lowercase(text: str) -> str:
    """
    :description: Converts a string to lowercase.
    :use_case: Use when the user requests "all small letters", "lowercase", or to "un-capitalize everything".
    :param text: The input string.
    :returns: The string converted to lowercase.
    """
    return text.lower()

@client_tool
def reverse_string(text: str) -> str:
    """
    :description: Reverses a given string.
    :use_case: Use when the user asks to "reverse a string", "spell backwards", or "flip text".
    :param text: The input string.
    :returns: The reversed string.
    """
    return text[::-1]

@client_tool
def is_even(number: int) -> bool:
    """
    :description: Checks if a number is even.
    :use_case: Use when the user asks "is this number even?" or to "check for evenness".
    :param number: The integer to check.
    :returns: True if the number is even, False otherwise.
    """
    return number % 2 == 0

@client_tool
def is_odd(number: int) -> bool:
    """
    :description: Checks if a number is odd.
    :use_case: Use when the user asks "is this number odd?" or to "check for oddness".
    :param number: The integer to check.
    :returns: True if the number is odd, False otherwise.
    """
    return number % 2 != 0

@client_tool
def get_max_of_two(a: float, b: float) -> float:
    """
    :description: Finds the maximum of two numerical inputs.
    :use_case: Use when the user asks for the "maximum", "larger", or "greater" of two values.
    :param a: The first number.
    :param b: The second number.
    :returns: The larger of the two numbers.
    """
    return max(a, b)

@client_tool
def get_min_of_two(a: float, b: float) -> float:
    """
    :description: Finds the minimum of two numerical inputs.
    :use_case: Use when the user asks for the "minimum", "smaller", or "lesser" of two values.
    :param a: The first number.
    :param b: The second number.
    :returns: The smaller of the two numbers.
    """
    return min(a, b)

@client_tool
def concatenate_strings(s1: str, s2: str) -> str:
    """
    :description: Concatenates two strings.
    :use_case: Use when the user asks to "combine strings", "join text", or "put together words".
    :param s1: The first string.
    :param s2: The second string.
    :returns: The combined string.
    """
    return s1 + s2

@client_tool
def is_palindrome(text: str) -> bool:
    """
    :description: Checks if a string is a palindrome.
    :use_case: Use when the user asks "is it a palindrome?" or to "check for palindrome". Ignores case and non-alphanumeric characters.
    :param text: The input string.
    :returns: True if the string is a palindrome, False otherwise.
    """
    processed_text = "".join(char.lower() for char in text if char.isalnum())
    return processed_text == processed_text[::-1]

@client_tool
def calculate_square_root(number: float) -> float:
    """
    :description: Calculates the square root of a non-negative number.
    :use_case: Use when the user asks for the "square root of", "sqrt", or "what number multiplied by itself equals X".
    :param number: The non-negative number.
    :returns: The square root of the number.
    """
    if number < 0:
        raise ValueError("Cannot calculate square root of a negative number.")
    return number**0.5

@client_tool
def power(base: float, exponent: float) -> float:
    """
    :description: Calculates the power of a base number to an exponent.
    :use_case: Use when the user asks for "X to the power of Y", "X raised to Y", or "exponentiation".
    :param base: The base number.
    :param exponent: The exponent.
    :returns: The result of `base` raised to the power of `exponent`.
    """
    return base ** exponent

@client_tool
def get_day_of_week(date_string: str) -> str:
    """
    :description: Determines the day of the week for a given date.
    :use_case: Use when the user asks "what day of the week is X date?" or wants to know the weekday of a specific
    past or future date.
    :param date_string: The date in YYYY-MM-DD format.
    :returns: The day of the week (e.g., "Monday", "Tuesday").
    """
    date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    return date_object.strftime("%A")

@client_tool
def email_validator(email: str) -> bool:
    """
    :description: Checks if a given string is a valid email address format.
    :use_case: Use when the user asks "is this a valid email?" or needs to verify an email's structure.
    :param email: The email string to validate.
    :returns: True if the email format is valid, False otherwise.
    """
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None

@client_tool
def count_words(text: str) -> int:
    """
    :description: Counts the number of words in a given string.
    :use_case: Use when the user asks "how many words are in this text?" or needs a word count.
    :param text: The input string.
    :returns: The number of words in the string.
    """
    words = text.split()
    return len(words)

@client_tool
def average_two_numbers(a: float, b: float) -> float:
    """
    :description: Calculates the average of two numbers.
    :use_case: Use when the user wants to find the "average" or "mean" of two numerical values.
    :param a: The first number.
    :param b: The second number.
    :returns: The average of `a` and `b`.
    """
    return (a + b) / 2

@client_tool
def remove_whitespace(text: str) -> str:
    """
    :description: Removes all whitespace characters from a string.
    :use_case: Use when the user asks to "remove spaces" or "strip whitespace" from text.
    :param text: The input string.
    :returns: The string with all whitespace removed.
    """
    return "".join(text.split())

@client_tool
def convert_celsius_to_kelvin(celsius: float) -> float:
    """"
    :description: Converts temperature from Celsius to Kelvin.
    :use_case: Use this tool when the user explicitly asks to convert a temperature FROM Celsius TO Kelvin.
    Look for keywords like 'Celsius to Kelvin', 'C to K', or 'convert NUM C to K'.
    :param celsius: The temperature in Celsius.
    :returns: The temperature converted to Kelvin.
    """
    return celsius + 273.15

@client_tool
def convert_fahrenheit_to_kelvin(fahrenheit: float) -> float:
    """"
    :description: Converts temperature from Fahrenheit to Kelvin.
    :use_case: Use this tool when the user explicitly asks to convert a temperature FROM Fahrenheit TO Kelvin.
    Look for keywords like 'Fahrenheit to Kelvin', 'F to K', or 'convert NUM F to K'.
    :param fahrenheit: The temperature in Fahrenheit.
    :returns: The temperature converted to Kelvin.
    """
    return (fahrenheit - 32) * 5/9 + 273.15

@client_tool
def convert_celsius_to_fahrenheit(celsius: float) -> float:
    """
    :description: Converts temperature from Celsius to Fahrenheit.
    :use_case: Use this tool when the user explicitly asks to convert a temperature FROM Celsius TO Fahrenheit. Look
    for keywords like 'Celsius in Fahrenheit', 'C to F', or 'convert NUM C to F'.
    :param celsius: The temperature in Celsius.
    :returns: The temperature converted to Fahrenheit.
    """
    return (celsius * 9/5) + 32

@client_tool
def convert_fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    :description: Converts temperature from Fahrenheit to Celsius.
    :use_case: Use this tool when the user explicitly asks to convert a temperature FROM Fahrenheit TO Celsius. Look
    for keywords like 'Fahrenheit to Celsius', 'F to C', or 'convert NUM F to C'.
    :param fahrenheit: The temperature in Fahrenheit.
    :returns: The temperature converted to Celsius.
    """
    return (fahrenheit - 32) * 5/9

@client_tool
def get_substring(text: str, start_index: int, end_index: int) -> str:
    """
    :description: Extracts a substring from a given string based on start and end indices.
    :use_case: Use when the user asks to "get part of a string" or "extract text from index X to Y".
    :param text: The input string.
    :param start_index: The starting index (inclusive).
    :param end_index: The ending index (exclusive).
    :returns: The extracted substring.
    """
    return text[start_index:end_index]

@client_tool
def round_number(number: float, decimal_places: int) -> float:
    """
    :description: Rounds a given float to a specified number of decimal places.
    :use_case: Use when the user asks to "round a number" or "truncate to X decimal places".
    :param number: The float number to round.
    :param decimal_places: The number of decimal places to round to.
    :returns: The rounded number.
    """
    return round(number, decimal_places)

@client_tool
def is_leap_year(year: int) -> bool:
    """
    :description: Checks if a given year is a leap year.
    :use_case: Use when the user asks "is X year a leap year?" or needs to determine leap year status.
    :param year: The year to check.
    :returns: True if the year is a leap year, False otherwise.
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

@client_tool
def generate_random_integer(min_value: int, max_value: int) -> int:
    """
    :description: Generates a random integer within a specified range (inclusive).
    :use_case: Use when the user asks for a "random number between X and Y".
    :param min_value: The minimum value for the random integer.
    :param max_value: The maximum value for the random integer.
    :returns: A random integer within the specified range.
    """
    import random
    return random.randint(min_value, max_value)

@client_tool
def get_file_extension(filename: str) -> str:
    """
    :description: Extracts the file extension from a given filename.
    :use_case: Use when the user asks "what's the file extension of X?" or needs to parse a filename.
    :param filename: The input filename (e.g., "document.pdf").
    :returns: The file extension (e.g., "pdf"), or an empty string if no extension is found.
    """
    return filename.split('.')[-1] if '.' in filename else ""

@client_tool
def replace_substring(text: str, old_substring: str, new_substring: str) -> str:
    """
    :description: Replaces all occurrences of a specified substring with another substring within a given text.
    :use_case: Use when the user asks to "replace text", "find and replace", or "change X to Y in a string".
    :param text: The original string.
    :param old_substring: The substring to be replaced.
    :param new_substring: The substring to replace with.
    :returns: The string with all occurrences replaced.
    """
    return text.replace(old_substring, new_substring)

@client_tool
def is_prime(number: int) -> bool:
    """
    :description: Checks if a given integer is a prime number.
    :use_case: Use when the user asks "is X a prime number?" or needs to check for primality.
    :param number: The integer to check.
    :returns: True if the number is prime, False otherwise.
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
    :description: Calculates the Body Mass Index (BMI) given weight in kilograms and height in meters.
    :use_case: Use when the user asks to "calculate BMI".
    :param weight_kg: The weight in kilograms.
    :param height_m: The height in meters.
    :returns: The calculated BMI.
    """
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    return weight_kg / (height_m ** 2)

@client_tool
def convert_kilograms_to_pounds(kg: float) -> float:
    """
    :description: Converts weight from kilograms to pounds.
    :use_case: Use when the user asks for "kilograms to pounds conversion" or needs to convert weight units.
    :param kg: The weight in kilograms.
    :returns: The weight converted to pounds.
    """
    return kg * 2.20462

@client_tool
def convert_pounds_to_kilograms(lb: float) -> float:
    """
    :description: Converts weight from pounds to kilograms.
    :use_case: Use when the user asks for "pounds to kilograms conversion" or needs to convert weight units.
    :param lb: The weight in pounds.
    :returns: The weight converted to kilograms.
    """
    return lb / 2.20462

@client_tool
def convert_meters_to_feet(meters: float) -> float:
    """
    :description: Converts a length from meters to feet.
    :use_case: Use when the user asks for "meters to feet conversion" or needs to convert length units.
    :param meters: The length in meters.
    :returns: The length converted to feet.
    """
    return meters * 3.28084

@client_tool
def convert_feet_to_meters(feet: float) -> float:
    """
    :description: Converts a length from feet to meters.
    :use_case: Use when the user asks for "feet to meters conversion" or needs to convert length units.
    :param feet: The length in feet.
    :returns: The length converted to meters.
    """
    return feet / 3.28084

@client_tool
def is_alphanumeric(text: str) -> bool:
    """
    :description: Checks if all characters in a string are alphanumeric (letters or numbers).
    :use_case: Use when the user asks "is this string alphanumeric?" or needs to validate input containing only letters and numbers.
    :param text: The input string.
    :returns: True if all characters are alphanumeric, False otherwise.
    """
    return text.isalnum()

@client_tool
def url_encode(text: str) -> str:
    """
    :description: URL-encodes a given string.
    :use_case: Use when the user needs to "URL encode" text for web parameters or links.
    :param text: The string to URL-encode.
    :returns: The URL-encoded string.
    """
    import urllib.parse
    return urllib.parse.quote_plus(text)

@client_tool
def url_decode(text: str) -> str:
    """
    :description: URL-decodes a given string.
    :use_case: Use when the user needs to "URL decode" text from web parameters or links.
    :param text: The string to URL-decode.
    :returns: The URL-decoded string.
    """
    import urllib.parse
    return urllib.parse.unquote_plus(text)
