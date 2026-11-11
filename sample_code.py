
# GreenCode Analyzer - Clean Code Testing Sample

print("GreenCode Analyzer - Clean Code Test")

# A simple list of numbers
numbers = [10, 20, 30, 40, 50]

# A single for loop
for number in numbers:
    square = number * number

print("Program completed successfully.")

# Example 1: Nested loops
print("Example 1: Nested Loop")

for i in range(10):
    for j in range(5):
        result = i * j


# Example 2: Repeated membership checking
print("Example 2: Membership Checking")

students = [
    "Aman",
    "Riya",
    "Rahul",
    "Geetika"
]

registered_students = [
    "Aman",
    "Geetika",
    "Rahul"
]

for student in students:
    if student in registered_students:
        print(student, "is registered")


# Example 3: Normal loop
print("Example 3: Normal Loop")

numbers = [1, 2, 3, 4, 5]

for number in numbers:
    square = number * number


# Example 4: While loop
print("Example 4: While Loop")

count = 0

while count < 3:
    count += 1


print("Sample program completed.")
