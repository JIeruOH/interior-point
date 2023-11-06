import interior, simplex

# example
c = [1, 2, 0]
A = [
    [1, 1, 1],
]
b = [8]
eps = 1e-3



print('Simplex method:')
# try except to ignore exit()
try:
    simplex.run(c, A, b)
except:
    pass

print(f"\n{'=' * 100}\n")

print('Interior point algorithm(alpha = 0.5):')
# try except to ignore exit()
try:
    interior.run(c, A, b, eps, 0.5)
except:
    pass

print(f"\n{'=' * 100}\n")

print('Interior point algorithm(alpha = 0.9):')
# try except to ignore exit()
try:
    interior.run(c, A, b, eps, 0.9)
except:
    pass