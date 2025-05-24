import os

# === Core Data Structure ===

sparse_matrix = {}

def set_element(matrix, row, col, value):
    key = (row, col)
    if value == 0:
        if key in matrix:
            del matrix[key]
    else:
        matrix[key] = value

def get_element(matrix, row, col):
    return matrix.get((row, col), 0)

# === Matrix Operations ===

def add_sparse_matrix(a, b):
    result = {}
    for key in a:
        result[key] = a[key]
    for key in b:
        if key in result:
            result[key] += b[key]
            if result[key] == 0:
                del result[key]
        else:
            result[key] = b[key]
    return result

def subtract_sparse_matrix(a, b):
    result = {}
    for key in a:
        result[key] = a[key]
    for key in b:
        if key in result:
            result[key] -= b[key]
            if result[key] == 0:
                del result[key]
        else:
            result[key] = -b[key]
    return result

def multiply_sparse_matrix(a, b):
    result = {}
    # Create a mapping from column to its elements in b
    b_by_row = {}
    for (row, col), val in b.items():
        if row not in b_by_row:
            b_by_row[row] = {}
        b_by_row[row][col] = val

    for (i, k1), v1 in a.items():
        if k1 in b_by_row:
            for j, v2 in b_by_row[k1].items():
                key = (i, j)
                result[key] = result.get(key, 0) + v1 * v2
                if result[key] == 0:
                    del result[key]
    return result

# === File Reading ===

def read_file_matrix(path):
    matrix = {}
    num_rows = 0
    num_cols = 0
    try:
        with open(path, "r") as file:
            lines = [line.strip() for line in file if line.strip()]

        if len(lines) < 2:
            raise ValueError("File must have at least 2 lines: rows and cols")

        if lines[0].startswith("rows="):
            num_rows = int(lines[0][5:])
        if lines[1].startswith("cols="):
            num_cols = int(lines[1][5:])

        for line in lines[2:]:
            if line[0] != '(' or line[-1] != ')':
                print("Error: wrong format")
                return 0, 0, {}

            content = line[1:-1]
            parts = content.split(",")
            if len(parts) != 3:
                print("Error: invalid entry")
                return 0, 0, {}

            row = int(parts[0].strip())
            col = int(parts[1].strip())
            val = int(parts[2].strip())

            if val != 0:
                matrix[(row, col)] = val

    except Exception as e:
        print("File not found or error reading file.")
        print("Reason:", str(e))
    return num_rows, num_cols, matrix

# === Main Menu ===

print("Choose operation:")
print("1. Add")
print("2. Subtract")
print("3. Multiply")
choice = input("Enter your choice (1/2/3): ")

# Provide your actual file paths here
path1 = r"C:\Users\HP\Learning DSA\sparse_matrix_work\sample_inputs\easy_sample_02_1.txt"
path2 = r"C:\Users\HP\Learning DSA\sparse_matrix_work\sample_inputs\easy_sample_02_2.txt"

rows1, cols1, m1 = read_file_matrix(path1)
rows2, cols2, m2 = read_file_matrix(path2)

# Validate dimensions before operation
if choice == '1':
    if rows1 == rows2 and cols1 == cols2:
        result = add_sparse_matrix(m1, m2)
    else:
        print("Matrix dimensions don't match for addition.")
        result = {}
elif choice == '2':
    if rows1 == rows2 and cols1 == cols2:
        result = subtract_sparse_matrix(m1, m2)
    else:
        print("Matrix dimensions don't match for subtraction.")
        result = {}
elif choice == '3':
    if cols1 == rows2:
        result = multiply_sparse_matrix(m1, m2)
    else:
        print("Matrix dimensions not compatible for multiplication.")
        result = {}
else:
    print("Invalid choice.")
    result = {}

# === Display Result ===
if result:
    print("\nResult (non-zero elements):")
    for key in sorted(result):
        print(f"{key} => {result[key]}")
else:
    print("\nNo non-zero elements in result or operation failed.")
