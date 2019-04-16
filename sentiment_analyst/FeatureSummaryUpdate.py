# -*- coding: utf-8 -*-
from underthesea import pos_tag
from Apriori import Apriori
import collections
import pandas as pd
from collections import OrderedDict
from datetime import date


class FutureSummaryUpdate:

    def read_raw_file(self) -> list:
        f = open("raw.txt", "r+")
        noun_list = []
        adj_list = []
        for line in f:
            result = pos_tag(line)
            record_n = []
            record_adj = []
            for item in result:
                if item[1] == 'N' and self.one_word_prune(item[0]):
                    record_n.append(item[0])
                if item[1] == 'A' or item[1] == 'AP':
                    record_adj.append(item[0])
            noun_list.append(record_n)
            adj_list.append(record_adj)
            # for r in noun_list:
            #     print(r)
            # for rr in adj_list:
            #     print(rr)
        return noun_list

    def apriori(self, data: list) -> list:
        ck = self.gen_large_1_item_set(data[2:3])
        # large_1_item_df = pd.DataFrame(large_1_item_set[1].items(), columns=['key', 'value'])
        # print(ck)
        k = 2
        while len(ck[k - 1]) > 0:
            ck = self.apriori_gen(ck[k - 1], k)
            # print(ck)
            k += 1

        return []

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

        print('====================\n')
        self.apriori_prune(ck, k, large_k_item)
        return {k: ck}

    def apriori_prune(self, ck: dict, n: int, last_ck: dict) -> dict:
        result = {}
        print(ck)
        print(last_ck)
        for k, v in ck.items():
            index_list = str(k).split(',')
            value_list = str(v).split(',')

            sub_list = self.combination_gen(value_list, n)

            is_contain = True
            for key, value in last_ck.items():
                for i in sub_list:
                    list_value_list = str(value).split(',')
                    size = len(set(list_value_list) & set(i))
                    # print(set(list_value_list) & set(i))
                    if size == n - 1:
                        continue
                    else:
                        is_contain = False
            if is_contain:
                result[k] = v
        # print(result)
        return result

    def combination_gen(self, data: list, n: int) -> list:
        result = []
        k = n - 1
        max_value = n - 1
        b = []
        for j in range(n - 1):
            b.append(j)

        first_temp = []
        for q in b:
            first_temp.append(data[q - 1])
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
                    data_temp.append(data[q - 1])
                result.append(data_temp)
        print(result)
        return result

    def gen_item_from_2_sub(self, item1: list, item2: list) -> str:
        item1.extend(item2)
        result = ''
        for i in collections.OrderedDict.fromkeys(item1):
            result += i + ','
        return result[:-1]

    def one_word_prune(self, word: str) -> bool:
        if len(word) > 1:
            return True
        else:
            return False


def main():
    x = FutureSummaryUpdate()
    # x.read_raw_file()
    x.apriori(x.read_raw_file())

    y = Apriori()


if __name__ == '__main__':
    main()
