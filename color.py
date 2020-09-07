print("Background | Foreground colors")
for i in range(40, 48):
    print("".center(69, "-"))
    for run in range(2):
        st = f' ESC[{i}m   | \033[;{i}m'
        for j in range(30, 38):
            if run == 0:
                st += f'\033[{j}m[{j}m'.ljust(12)
            else:
                st += f'\033[1;{j}m[1;{j}m'.ljust(14)
        st += "\033[0m"
        print(st)
print("".center(69, "-"), end='\n')