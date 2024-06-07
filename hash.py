from argon2 import PasswordHasher

# Initialize the password hasher
ph = PasswordHasher()

# Password to hash
password = "569569"  # Replace with the password you want to hash

# Generate the hash
hashed_password = ph.hash(password)

# Print the hashed password
print(hashed_password)
