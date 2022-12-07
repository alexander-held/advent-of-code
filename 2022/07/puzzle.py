import fileinput
from collections import defaultdict

x = [line.strip() for line in fileinput.input()]

# track total size of all files below each directory
directory_sizes = defaultdict(int)
path = "/"  # current position

for line in x:
    if line[0] == "$":
        if line.split()[1] == "cd":
            target = line.split()[2]
            if target == "/":
                path = "/"
            elif target == "..":
                path = f"{'/'.join(path.split('/')[0:-2])}/"
            else:
                path = f"{path}{target}/"
    else:
        size, name = line.split()
        if size != "dir":
            fname = f"{path}{name}"
            # generate list of all directories containing this file and update sizes
            for dirname in [
                "/".join(fname.split("/")[:-i]) for i in range(len(fname.split("/")))
            ][1:-1] + ["/"]:
                directory_sizes[dirname] += int(size)


print(f"part 1: {sum([ds for ds in directory_sizes.values() if ds < 100_000])}")

need_to_del = 30_000_000 - (70_000_000 - directory_sizes["/"])
print(f"part 2: {min([ds for ds in directory_sizes.values() if ds >= need_to_del])}")
