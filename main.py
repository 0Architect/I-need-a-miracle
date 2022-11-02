import itertools

from contradiction_class import Struct


def prioritize(dictionary: dict):
    priority = {}
    for key in dictionary.keys():
        struct = dictionary[key]
        score_a = len(struct.possible_values)
        score_b = len(struct.adjacent)
        if score_a in priority.keys():
            lst_copy = priority[score_a].copy()
            for x in priority[score_a]:
                if score_b <= len(dictionary[x].adjacent):
                    continue
                if score_b > len(dictionary[x].adjacent):
                    x_index = priority[score_a].index(x)
                    lst_copy = lst_copy[:x_index] + [key] + lst_copy[x_index:]
                    continue
                lst_copy.append(key)
            priority[score_a] = lst_copy.copy()
        else:
            priority[score_a] = [key]
    priority_list = []
    asd = list(priority.keys())
    asd.sort()
    for kwy in asd:
        for jgh in priority[kwy]:
            priority_list.append(jgh)

    return priority_list


def remove(found: list, hash_map: dict):
    hash_map_copy = hash_map.copy()
    for key in hash_map.keys():
        if key in found:
            hash_map_copy.pop(key)
    return hash_map_copy


def main():
    mat = [[0, 0, 0, 2, 0, 0, 0, 0, 0], [8, 0, 9, 0, 0, 0, 1, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0, 0],
           [6, 0, 3, 0, 0, 9, 0, 0, 0], [0, 7, 0, 6, 0, 0, 0, 5, 0], [0, 0, 0, 0, 4, 0, 9, 0, 3],
           [0, 4, 0, 0, 8, 0, 0, 3, 0], [0, 0, 6, 9, 0, 0, 0, 7, 0], [0, 9, 5, 0, 0, 1, 0, 0, 2]]

    found = []
    for row in range(len(mat)):
        for col in range(len(mat)):
            if mat[row][col] != 0:
                found.append((row, col))

    hash_map = {}
    for i in range(9):
        for j in range(9):
            hash_map[i, j] = set({})

    while found:
        hash_map = remove(found, hash_map)

        for found_item in found:
            curr_row = found_item[0]
            curr_col = found_item[1]
            curr_cell = mat[curr_row][curr_col]

            for unsolved_item in hash_map.keys():

                if curr_row == unsolved_item[0]:
                    hash_map[unsolved_item].add(curr_cell)

                if curr_col == unsolved_item[1]:
                    hash_map[unsolved_item].add(curr_cell)

                if curr_row // 3 == unsolved_item[0] // 3 and curr_col // 3 == unsolved_item[1] // 3:
                    hash_map[unsolved_item].add(curr_cell)

        found.clear()
        for item in hash_map.keys():
            if len(hash_map[item]) == 8:
                found.append(item)

        for item in found:
            universal_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            my_num = (universal_set - hash_map[item]).pop()
            my_row = item[0]
            my_col = item[1]
            mat[my_row][my_col] = my_num

        # determines cells that contradict themselves
        if hash_map:
            rejects = {}
            for key in hash_map.keys():
                rejects[key] = (Struct(({1, 2, 3, 4, 5, 6, 7, 8, 9} - hash_map[key])))
            for item in rejects.keys():
                for links in rejects.keys():
                    if item == links: continue
                    if item[0] == links[0] or item[1] == links[1] or (
                            item[0] // 3 == links[0] // 3 and item[1] // 3 == links[1] // 3):
                        rejects[item].link(rejects[links])
            # some_list = rejects.copy()
            # for x in rejects.keys():
            #     value = rejects[x]
            #     some_list[x] = value.possible_values
            # print(list(itertools.product(*some_list.values())))
            # for num in prioritize(rejects):
            #     struct = rejects[num]
            #     if struct.value > 0:
            #         continue
            #     update_value = random.choice(list(struct.possible_values))
            #     struct.update(update_value)
            #
            #     my_row = num[0]
            #     my_col = num[1]
            #     mat[my_row][my_col] = struct.value

    for row in mat:
        print(row)
    # print(found)
    print("\nKEY\t\t\t\tVALUE\t\t\t\tCONSTRAINTS")
    print(len(prioritize(rejects)))
    for key in prioritize(rejects):
        print(f"{key}\t\t\t\t{({1, 2, 3, 4, 5, 6, 7, 8, 9}) - hash_map[key]}\t\t\t\t{len(rejects[key].adjacent)}")


if __name__ == '__main__':
    main()
