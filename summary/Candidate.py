class Candidate:

    def __init__(self, candidate: dict):
        self.candidate = candidate
        self.item_list = []
        for key, value in self.candidate.items():
            self.item_list.append(Item(key, value))

    # Just test
    def subset_for_candidate(self, transaction: list):
        for i in self.item_list:
            value_list = i.value.split(',')
            if len(value_list) == len(set(value_list) & set(transaction)):
                i.count += 1

    def filter_with_support_min(self, min_sup: int) -> dict:
        result = {}
        for i in self.item_list:
            if i.count >= min_sup:
                result[i.key] = i.value
        return result


class Item:

    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value
        self.count = 0
