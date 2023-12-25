import fileinput

x = [line.strip() for line in fileinput.input()]

passports = []
content = ""
x.append("")  # extra newline at the end for easier parsing
for line in x:
    if line == "":
        passport = {}
        for key_value in content.strip().split(" "):
            passport.update({key_value.split(":")[0]: key_value.split(":")[1]})
        passports.append(passport)
        content = ""
    else:
        content += " " + line

req_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

num_valid_part_1 = 0
num_valid_part_2 = 0
for passport in passports:
    req_exist = all([req in passport.keys() for req in req_fields])
    if req_exist:
        num_valid_part_1 += 1

        # part 2
        passport_ok = True
        passport_ok *= (1920 <= int(passport["byr"]) <= 2002)
        passport_ok *= (2010 <= int(passport["iyr"]) <= 2020)
        passport_ok *= (2020 <= int(passport["eyr"]) <= 2030)

        if "cm" in passport["hgt"]:
            passport_ok *= (150 <= int(passport["hgt"].strip("cm")) <= 193)
        elif "in" in passport["hgt"]:
            passport_ok *= (59 <= int(passport["hgt"].strip("in")) <= 76)
        else:
            passport_ok = False

        if (passport["hcl"][0] == "#" and len(passport["hcl"]) == 7):
            try:
                int(passport["hcl"][1:], 16)
            except:
                passport_ok = False
        else:
            passport_ok = False

        passport_ok *= (passport["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
        passport_ok *= (len(passport["pid"]) == 9 and passport["pid"].isdigit())
        if passport_ok:
            num_valid_part_2 += 1

print("total valid", num_valid_part_1)
print("total valid part 2", num_valid_part_2)
