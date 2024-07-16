import pandas as pd
import random

# Extensive list of sample names to represent diverse backgrounds
names = [
    "John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank",
    "Grace", "Hank", "Ivy", "Jack", "Kara", "Liam", "Mona", "Noah",
    "Olivia", "Paul", "Quinn", "Rose", "Sam", "Tina", "Uma", "Vince",
    "Wendy", "Xander", "Yara", "Zane", "Brian", "Nina", "Oscar",
    "Pete", "Rachel", "Steve", "Tracy", "Victor", "Zoe", "Ben", "Anna",
    "Leo", "Mia", "Nate", "Sara", "Tom", "Holly", "Kim", "Luke", "Emma",
    "Gabe", "Iris", "Matt", "Jill", "Erin", "Adam", "Chloe", "David",
    "Carlos", "Maria", "Sophia", "James", "Julia", "Elena", "Luis",
    "Jose", "Elisa", "Pablo", "Marta", "Miguel", "Angela", "Juan",
    "Carmen", "Jorge", "Lucia", "Diego", "Isabella", "Martin", "Paula",
    "Roberto", "Esther", "Raul", "Ana", "Pedro", "Natalie", "Sebastian",
    "Laura", "Antonio", "Camila", "Gabriel", "Hector", "Valeria",
    "Fernando", "Clara", "Andres", "Angela", "Ricardo", "Patricia",
    "Emilio", "Julieta", "Eduardo", "Beatriz", "Arturo", "Marina",
    "Javier", "Manuel", "Luis", "Rosa", "Enrique", "Victoria",
    "Samuel", "Daniela", "Alberto", "Monica", "Felix", "Gloria",
    "Mario", "Tomas", "Cecilia", "Elias", "Cristina", "Santiago",
    "Esteban", "Renata", "Rodrigo", "Alicia", "Gustavo", "Andrea",
    "Rafael", "Adriana", "Marco", "Vanessa", "Hugo", "Dario", "Paola",
    "Ignacio", "Sofia", "Francisco", "Silvia", "Humberto", "Lorena",
    "Joaquin", "Belen", "Alfredo", "Carolina", "Ramiro", "Dolores",
    "Matias", "Eva", "Pilar", "Isabel", "Julio", "Natalia"
]

# Generate a list of zipcodes in the range from 46145 to 46180
zipcodes = [str(zipcode) for zipcode in range(46145, 46181)]

# Load the existing CSV
df = pd.read_csv('Student_performance_data _.csv')

# Ensure there are at least 2400 entries
if len(df) < 2392:
    # If not, repeat the dataframe to reach at least 2400 entries
    df = pd.concat([df] * (2392 // len(df) + 1), ignore_index=True)
    df = df.iloc[:2392]

# Add the `name` column with random names
df['name'] = [random.choice(names) for _ in range(len(df))]

# Add the `zipcode` column with random zipcodes
df['zipcode'] = [random.choice(zipcodes) for _ in range(len(df))]

# Save the modified dataframe back to a CSV file
df.to_csv('modified_data.csv', index=False)

print("CSV file has been updated and saved as 'modified_data.csv'")
