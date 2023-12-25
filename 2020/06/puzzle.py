import fileinput
import re

x = "".join([line for line in fileinput.input()]).strip()

sum_anyone = 0
sum_everyone = 0
for group in re.split(r"\n\n", x):
    unique_resp = list(set([v for v in "".join(group.replace("\n", ""))]))
    sum_anyone += len(unique_resp)
    answers = re.split(r"\n", group)
    sum_everyone += sum([all([ur in a for a in answers]) for ur in unique_resp])

print(sum_anyone)
print(sum_everyone)
