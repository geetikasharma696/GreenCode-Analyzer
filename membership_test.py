
# GreenCode Analyzer - Membership Testing

# List collection
students = ["Aman", "Riya", "Rahul"]

# Set collection
registered_students = {"Aman", "Rahul"}

# Dictionary collection
student_records = {
    "Aman": True,
    "Rahul": True
}

# Test membership in list, set and dictionary
for student in students:

    # List membership check
    if student in students:
        print(student, "found in students list")

    # Set membership check
    if student in registered_students:
        print(student, "found in registered set")

    # Dictionary membership check
    if student in student_records:
        print(student, "found in student records")

