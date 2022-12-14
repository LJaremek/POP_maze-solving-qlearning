from map import simple_gen_map, print_map

small_easy_map = simple_gen_map("small", "easy")
print("Small easy:")
print_map(small_easy_map)

small_hard_map = simple_gen_map("small", "hard")
print("Small hard:")
print_map(small_hard_map)

big_easy_map = simple_gen_map("big", "easy")
print("Big easy:")
print_map(big_easy_map)

big_hard_map = simple_gen_map("big", "hard")
print("Big hard:")
print_map(big_hard_map)
