# Basic Python Program - lean.py
# This program demonstrates some basic Python features

# Variables and data types
name = "Python Learner"
age = 25
height = 5.9
is_student = True

print("Hello, " + name + "!")
print(f"You are {age} years old and {height} feet tall.")
print(f"Are you a student? {is_student}")

# Lists
fruits = ["apple", "banana", "orange", "grape"]
print("\nMy favorite fruits:")
for fruit in fruits:
    print("- " + fruit)

# Functions
def greet(person):
    return f"Hello, {person}! Welcome to Python programming."

print("\n" + greet("World"))

# Conditional statements
if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")

# Loops
print("\nCounting to 5:")
for i in range(1, 6):
    print(i)

# Dictionary
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

print("\nPerson details:")
for key, value in person.items():
    print(f"{key}: {value}")

print("\nPython is powerful and easy to learn!")