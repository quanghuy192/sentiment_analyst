# -*- coding: utf-8 -*-
from underthesea import pos_tag

import collections
from Candidate import Candidate
from underthesea import sent_tokenize
import math
import unittest


class FutureSummaryUpdate:
    transaction = []
    sentences = []

    # Just test
    def read_raw_file(self) -> list:
        f = open("test_a1000.txt", "r+")
        noun_list = []
        adj_list = []
        for line in f:
            result = pos_tag(line)
            print(result)
            print('\n')
            record_n = []
            record_adj = []
            self.sentences.extend(sent_tokenize(line))
            for item in result:
                if self.is_noun(item[1]) and self.one_word_prune(item[0]):
                    record_n.append(str(item[0]).lower())
                if item[1] == 'A' or item[1] == 'AP':
                    record_adj.append(str(item[0]).lower())
            noun_list.append(record_n)
            adj_list.append(record_adj)
        self.transaction = noun_list
        return noun_list

    def is_noun(self, type: str) -> bool:
        if type in ['N', 'Np', 'NP', 'Nc', 'Nu']:
            return True
        else:
            return False

    def apriori(self, data: list) -> list:
        ck = self.gen_large_1_item_set(data)
        candidate = Candidate(ck[1])
        for i in self.transaction:
            candidate.subset_for_candidate(i)
        ck_with_minsup = candidate.filter_with_support_min(self.dynamic_support(len(data), 1))
        # ck_with_minsup = candidate.filter_with_support_min(3)
        ck = {1: ck_with_minsup}
        last_ck = ck
        k = 2
        while len(ck[k - 1]) > 0:
            ck = self.apriori_gen(ck[k - 1], k)
            if len(ck[k]) <= 0:
                break
            print(ck)
            candidate = Candidate(ck[k])
            for i in self.transaction:
                candidate.subset_for_candidate(i)
            print('------------ K = ----------------')
            print(k)
            print(self.dynamic_support(len(data), k))
            ck_with_minsup = candidate.filter_with_support_min(self.dynamic_support(len(data), k))
            # ck_with_minsup = candidate.filter_with_support_min(3)
            last_ck = ck
            ck = {k: ck_with_minsup}
            k += 1
        print('------------- Feature --------------')
        feature = []
        for key, value in last_ck[k - 1].items():
            feature.extend(set(str(value).split(',')))
        print(set(feature))
        return []

    # Just test
    def gen_large_1_item_set(self, data: list) -> dict:
        temp_set = []
        for i in data:
            if len(set(i)) > 0:
                temp_set.extend(i)
        data_index = {}
        index = 0
        for i in set(temp_set):
            data_index[index] = i
            index += 1
        return {1: data_index}

    # Just test
    def dynamic_support(self, n: int, i: int):
        new_min = 0.3 * math.log10(n) / (10 * i) + 0.3
        support = new_min * n / 100
        return support

    # Just test
    def apriori_gen(self, large_k_item: dict, k: int) -> dict:

        ck = {}
        s1 = large_k_item
        s2 = large_k_item
        for k1, v1 in s1.items():
            for k2, v2 in s2.items():
                index_list1 = str(k1).split(',')
                value_list1 = str(v1).split(',')
                index_list2 = str(k2).split(',')
                value_list2 = str(v2).split(',')

                for i in range(k - 1):
                    if int(index_list1[i]) == int(index_list2[i]):
                        continue
                    elif int(index_list1[i]) < int(index_list2[i]) and i == k - 2:
                        key = self.gen_item_from_2_sub(index_list1, index_list2)
                        value = self.gen_item_from_2_sub(value_list1, value_list2)
                        ck[key] = value
                    else:
                        break

        return {k: self.apriori_prune(ck, k, large_k_item)}

    # def apriori_prune(self, ck: dict, n: int, last_ck: dict) -> dict:
    #     result = {}
    #     for k, v in ck.items():
    #         value_list = str(v).split(',')
    #
    #         sub_list = self.combination_gen(value_list, n)
    #
    #         is_contain = False
    #         for key, value in last_ck.items():
    #             for i in sub_list:
    #                 list_value_list = str(value).split(',')
    #                 size = len(set(list_value_list) & set(i))
    #                 if size == n - 1:
    #                     is_contain = True
    #                 else:
    #                     continue
    #         if is_contain:
    #             result[k] = v
    #     return result

    def apriori_prune(self, ck: dict, n: int, last_ck: dict) -> dict:
        result = {}
        for k, v in ck.items():
            value_list = str(v).split(',')

            sub_list = self.combination_gen(value_list, n)

            count = 0
            for key, value in last_ck.items():
                for i in sub_list:
                    list_value_list = str(value).split(',')
                    size = len(set(list_value_list) & set(i))
                    if size == n - 1:
                        count += 1
                    else:
                        continue
            if count == len(sub_list):
                result[k] = v
        return result

    # Just test
    def combination_gen(self, data: list, n: int) -> list:
        result = []
        k = n - 1
        max_value = n - 1
        b = []
        for j in range(n - 1):
            b.append(j)

        first_temp = []
        for q in b:
            first_temp.append(data[q])
        result.append(first_temp)

        is_continue = True
        while is_continue:
            i = k
            while b[i - 1] == max_value - k + i:
                i -= 1
            if i == 0:
                is_continue = False
            else:
                b[i - 1] += 1
                for h in range(i, max_value):
                    b[h] = b[i] + h - i
                data_temp = []
                for q in b:
                    data_temp.append(data[q])
                result.append(data_temp)
        return result

    # Just test
    def gen_item_from_2_sub(self, item1: list, item2: list) -> str:
        item1.extend(item2)
        result = ''
        for i in collections.OrderedDict.fromkeys(item1):
            result += i + ','
        return result[:-1]

    # Just test
    def one_word_prune(self, word: str) -> bool:
        if len(word) > 1:
            return True
        else:
            return False


def main():
    summary = FutureSummaryUpdate()
    summary.apriori(summary.read_raw_file())


if __name__ == '__main__':
    main()
