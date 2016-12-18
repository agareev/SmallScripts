#!/usr/bin/env python3
__author__ = 'aydar'

import xlrd
import re
import sys
import csv

element_cell_number = 0
description_cell_number = 1


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    """
    return [atoi(c) for c in re.split('(\d+)', text)]


def load_xls_tables(name):
    try:
        x = xlrd.open_workbook(name)
        sheet = x.sheet_by_index(0)
        cell_quantity = sheet.nrows
        presort_output = []
        for cell in range(cell_quantity):
            presort_output.append([sheet.row_values(cell)[element_cell_number],
                                   sheet.row_values(cell)[description_cell_number], cell])
        return presort_output, cell_quantity
    except XLRDError as e:
        return False

def tilda_counter(problem_string, bad_symbols):
    regex_name = re.search('([A-Z]+)', problem_string)
    name = regex_name.group(0)
    output = []
    # print(name)

    dirty_range = problem_string.split(bad_symbols)
    start = int(re.sub('[A-Z]+', '', dirty_range[0]))
    end = int(re.sub('[A-Z]+', '', dirty_range[1]))
    for i in range(start, end+1):
        # print(name + str(i))
        output.append(name+str(i))
    return output


def custom_split(presort_input, cell_quantity):
    presorted_list = []
    for i in range(cell_quantity):
        if presort_input[i][element_cell_number]:
            for z in presort_input[i][element_cell_number].split(","):
                z = re.sub(r'^\s', '', z)
                global bad_symbols
                bad_symbols = re.search('([~,-])', z)
                if bad_symbols:
                    for counts in tilda_counter(z, bad_symbols.group(0)):
                        presorted_list.append([counts, presort_input[i][description_cell_number]])
                else:
                    presorted_list.append([z, presort_input[i][description_cell_number]])
    return presorted_list


def custom_sort(presort_list):
    sort_list = []
    presort_list.sort(key=lambda tup: (natural_keys(tup[0]), tup[1]))
    for i in presort_list:
        # sort_list.append("{0};{1}".format(i[element_cell_number], i[description_cell_number]))
        sort_list.append([i[element_cell_number], i[description_cell_number]])
    return sort_list


def save_to_csv(sort_list, output_name):
    # if os.path.isfile(output_name):
    #     answer = input('File exist! Overwrite? y/n ')
    #     while answer != "y":
    #         if answer == "n":
    #             sys.exit(0)
    #         else:
    #             print("answer is not yes or no")
    #             sys.exit(1)
    with open(output_name, 'w', newline='') as fp:
        a = csv.writer(fp, delimiter=';')
        a.writerows(sort_list)
        print("Work is done!")





def converter(file_name, output_name):
    unparsed_list, cell_quantity = load_xls_tables(file_name)
    presort_list = custom_split(unparsed_list, cell_quantity)
    sort_list = custom_sort(presort_list)
    print(sort_list)
    mainer(sort_list)



class Item(object):
    def __init__(self, pk, k, v):
        self.pk = pk
        self.k = k
        self.v = int(v)
        self.next_v = self.v

    def same(self, other):
        return self.pk == other.pk

    def distant(self, other):
        return abs(self.v - other.v) != 1

    def extend(self, other):
        self.next_v = other.v

    def __repr__(self):
        r = '{}..{}'.format(self.v, self.next_v) if self.v != self.next_v else str(self.v)
        return '{pk}: {k}{r}'.format(pk=self.pk, k=self.k, r=r)


def finalize(prev_item):
    print(prev_item)

def mainer(aaa):
    # aaa = "".split()
    res = dict()
    r = re.compile(r'([A-Z]+)(\d+)')

    for line in aaa.split("\n"):
        if not line:
            continue
        v, k = line.split(';')
        m = re.match(r, v)
        item = (m.group(1), int(m.group(2)))

        if k in res:
            res[k].append(item)
        else:
            res[k] = [item]


    for k, v in res.items():
        print(v)
        prev_item = None
        for k2, v2 in v:
            item = Item(k, k2, v2)

            if prev_item is None:
                prev_item = item
                continue

            if not prev_item.same(item):
                finalize(prev_item)
                prev_item = item
                continue

            if prev_item.distant(item):
                finalize(prev_item)
                prev_item = item
                continue

            prev_item.extend(item)

        finalize(prev_item)

if __name__ == "__main__":
    converter(sys.argv[1], sys.argv[2])
    print(sys.argv[1])
    print(sys.argv[2])
