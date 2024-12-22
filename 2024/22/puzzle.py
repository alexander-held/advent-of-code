import fileinput
from collections import defaultdict


x = list(map(int, [line.strip() for line in fileinput.input()]))


def update_secret(secret):
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret // 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216
    return secret


sum_secrets = 0
bananas_for_pattern = defaultdict(int)
for buyer_secret in x:
    changes = []
    patterns_seen = set()  # only perform one sale per pattern
    for _ in range(2000):
        if tuple(changes[-4:]) not in patterns_seen and len(changes) >= 4:
            bananas_for_pattern[tuple(changes[-4:])] += buyer_secret % 10
            patterns_seen.add(tuple(changes[-4:]))
        next_secret = update_secret(buyer_secret)
        changes.append((next_secret % 10) - (buyer_secret % 10))
        buyer_secret = next_secret
    sum_secrets += buyer_secret


print(f"part 1: {sum_secrets}")
print(f"part 2: {max(bananas_for_pattern.values())}")
