""" Author: Raleigh Hansen
    Last Update: 11/25/2022 
    Version: Python 3.8.2
    Purpose: 
        Provide examples for using generate_data.py. 
"""

import generate_data

# ## EXAMPLE 1 ##
# # Generates a random uniform distribution of thirty two-dimensional points
# ex_1 = "examples/example1_random_uniform.txt"
# generate_data.generate_rand_uniform(30, ex_1, 2, 0, 30)

# ## EXAMPLE 2 ##
# # Generates a random normal distribution of fifty two-dimensional points
# ex_2 = "examples/example2_random_normal.txt"
# generate_data.generate_normal_cluster(50, ex_2)

# ## EXAMPLE 3 ##
# # Generates a random uniform distribution of thirty ten-dimensional points separated into three clusters
# ex_3 = "examples/example3_random_uniform_clustered.txt"
# generate_data.generate_rand_uniform(30, ex_3, 10, 0, 20, 3, 100)

# ## EXAMPLE 4 ##
# # Augments the example4_original.txt dataset from two dimensions to five dimensions
# ex_4o = "examples/example4_original.txt"
# ex_4a = "examples/example4_augmented.txt"
# generate_data.increase_dimensions(5, ex_4o, ex_4a)

