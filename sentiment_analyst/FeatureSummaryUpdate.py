# -*- coding: utf-8 -*-
from underthesea import pos_tag
from Apriori import Apriori
import pandas as pd
from collections import OrderedDict
from datetime import date


class FutureSummaryUpdate:

    def print_x(self):
        print("Hello world")

    def read_raw_file(self) -> list:
        f = open("raw.txt", "r+")
        noun_list = []
        adj_list = []
        for line in f:
            result = pos_tag(line)
            record_n = []
            record_adj = []
            for item in result:
                if item[1] == 'N':
                    record_n.append(item)
                if item[1] == 'A' or item[1] == 'AP':
                    record_adj.append(item)
            noun_list.append(record_n)
            adj_list.append(record_adj)
        for r in noun_list:
            print(r)
        for rr in adj_list:
            print(rr)
            return noun_list

    def apriori(self, data: list) -> list:
        x = self.large_1_item_set(data)
        print(x)
        return []

    def large_1_item_set(self, data: list) -> list:

        tempList =  []
        tempSet = {}
        for i in range(list):
            tempSet.add(i)

        print(tempSet)
        return []


def main():
    x = FutureSummaryUpdate()
    # x.read_raw_file()
    x.apriori(x.read_raw_file())

    y = Apriori()


if __name__ == '__main__':
    main()
