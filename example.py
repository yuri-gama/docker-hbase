import happybase
import random
import string

# Define the number of students to insert
num_students = 2000

# Define the column families and their options
column_families = {
    'personal_info': dict(max_versions=10),
    'contact_info': dict(max_versions=1, block_cache_enabled=False),
    'academic_info': dict(),
    'financial_info': dict()
}

# Create a connection to HBase
connection = happybase.Connection('hbase', port=9090)

# Create the table with the column families and options
connection.create_table(
    'students',
    column_families
)

# Open the table
table = connection.table('students')

# Define a function to generate a random string of letters and digits
def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Insert the student information into the table
for i in range(num_students):
    row_key = f'student{i}'
    values = {
        'personal_info:first_name': random_string(8),
        'personal_info:last_name': random_string(8),
        'personal_info:age': str(random.randint(18, 25)),
        'personal_info:gender': random.choice(['Male', 'Female']),
        'contact_info:email': f'student{i}@example.com',
        'contact_info:phone': f'{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
        'contact_info:address': f'{random.randint(1, 999)} {random_string(5)} St, {random_string(8)}, {random_string(5)} {random.randint(10000, 99999)}',
        'academic_info:major': random.choice(['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology']),
        'academic_info:gpa': '{:.2f}'.format(random.uniform(2.5, 4.0)),
        'academic_info:enrollment_date': f'{random.randint(2000, 2022)}-{random.randint(1, 12)}-{random.randint(1, 28)}',
        'academic_info:graduation_date': f'{random.randint(2023, 2027)}-{random.randint(1, 12)}-{random.randint(1, 28)}',
        'financial_info:tuition_balance': str(random.randint(0, 10000)),
        'financial_info:financial_aid': random.choice(['Yes', 'No']),
        'financial_info:scholarship': random.choice(['Yes', 'No'])
    }
    table.put(row_key, values)


rows = table.rows([b'student15', b'student954'])
# Print the rows that match the filter
for key, data in rows:
    print(key, data)

# Close the connection
connection.close()
