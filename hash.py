from passlib.context import CryptContext

# Initialize the password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password to hash
password = "569569"  # Replace with the password you want to hash

# Generate the hash
hashed_password = pwd_context.hash(password)

# Print the hashed password
print(hashed_password)
