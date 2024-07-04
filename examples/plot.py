import matplotlib.pyplot as plt

# Original values (x-axis)
displacements = [
    0.02782095968723297, 0.027983250096440315, 0.028131339699029922,
    0.028265109285712242, 0.028384869918227196, 0.02844787947833538,
    0.02856718935072422, 0.02879003994166851, 0.028893930837512016,
    0.029087549075484276, 0.02926366962492466, 0.029588749632239342,
    0.029760390520095825, 0.030063370242714882, 0.030295979231595993,
    0.030632829293608665, 0.03099678084254265, 0.031365711241960526,
    0.03175375983119011, 0.032248418778181076
]

# Corresponding values (y-axis)
fe_mesh_size = [
    0.5, 0.48, 0.46, 0.44, 0.42, 0.4, 0.38, 0.36, 0.34, 0.32,
    0.3, 0.28, 0.26, 0.24, 0.22, 0.2, 0.18, 0.16, 0.14, 0.12
]

# displacements.reverse()
# fe_mesh_size.reverse()

# Plotting
plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
plt.plot(fe_mesh_size, displacements, marker='o', linestyle='-', color='b', label='Values')
plt.title('Corresponding Values')
plt.xlabel('X values')
plt.ylabel('Y values')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Display the plot
plt.show()
