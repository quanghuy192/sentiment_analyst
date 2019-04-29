import math

n = 745
min_support = 3
min_sup_percent = min_support / n * 100

# print(min_sup_percent)
# print(pow(3, (-10000)))
new_min = 0.4 * math.log10(745) / 10 + 0.4
support = new_min * 745 / 100
# print(new_min)
# print(support)
for i in range(1, 5):
    new_min = 0.4 * math.log10(n) / (10 * i) + 0.4
    support = new_min * n / 100
    print(new_min)
    print(support)
    print('------------------------')
