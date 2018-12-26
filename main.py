
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
import random
import copy
import xlsxwriter

from functools import reduce


L_value = 10
list_of_deltas = [2, 2.5, 3, 10]


def main(global_children, n, t, pm):
    print('main_started')
    global NFE_COUNTER
    global ten_runs_exited
    children = copy.deepcopy(global_children)
    NFE_COUNTER = 0
    all_average_health = []
    all_best = []
    # best_child = []
    progon_successful = False
    while True:
        children_nfe, best_child_nfe, average_nfe = nfe2(children, L_value)  #NFE CHANGE HERE
        after_tournament = FitnessChoices(children, children_nfe, t)
        after_mutation = mutation(after_tournament, pm)
        break_while = False
        if len(all_average_health) >= 10:
            for health in all_average_health[len(all_average_health) - 10:len(all_average_health)]:
                res = abs(health - average_nfe)
                # print (str(health) + " - " + str(average_nfe) + " = " + str(res))
                if res > 0.0001:
                    break_while = False
                    break
                elif res <= 0.0001:
                    break_while = True
        all_average_health.append(average_nfe)
        all_best.append(best_child_nfe)
        best_child = children[children_nfe.index(best_child_nfe)]
        # print children
        if break_while:
            # print "Exiting for last 10 <= 0.0001"
            progon_successful = True
            ten_runs_exited += 1
            break
        if NFE_COUNTER == 200000:
            # print "Exiting for more than 20000000 nfe counts"
            break
        children = after_mutation
    # print all_average_health
    nfe_counts = len(all_average_health) * n
    average_nfe = reduce(lambda x, y: x + y, all_average_health) / len(all_average_health)
    best_nfe = sorted(all_best)[len(all_best) - 1]
    hemingman_distance = sum(best_child)
    return nfe_counts, average_nfe, best_nfe, hemingman_distance, progon_successful


def cycle(n, l, t, pm_start, d):
    print('cycle_started with values: ', n, l, t, pm_start, d)
    global ten_runs_exited
    global children_dict
    children_dict = {}
    pm = pm_start
    print("###################################################################")
    print("15 by 10 new parent to count PmMAX")
    fifteen_by_ten_data = {}
    for i in range(15):
        fifteen_by_ten_data[i] = {
            "pm": pm,
            "runs": []
        }
        print("---------------------------------------------------------------")
        print("Current Pm = " + str(pm))
        print("Current D = " + str(d))
        print ("Cycle #" + str(i))
        runs = 0
        ten_runs_exited = 0
        while True:
            print("Run #" + str(runs))
            if runs in children_dict:
                pass
            else:
                children_dict[runs] = create_children(n, l)
            nfe_counts, average_nfe, best_nfe, hemingman_distance, progon_successful = main(children_dict[runs], n,
                                                                                            t, pm)
            fifteen_by_ten_data[i]["runs"].append({
                "NFE": nfe_counts,
                "Середнє здоров'я в популяції": average_nfe,
                "Найкраще здоров'я в популяції": best_nfe,
                "Відхилення середнього здоров'я": abs(average_nfe - 1),
                "Відхилення найкращого здоров'я": abs(best_nfe - 1),
                "Геммінгова відстань": hemingman_distance,
                "Успішний": 1 if progon_successful else 0,
            })
            runs += 1
            if runs == 10 and ten_runs_exited == 10:
                pm = pm + d
                break
            elif runs == 10:
                pm = pm - d
                break
        d = d * 0.5
    ten_runs_exited = 0
    runs = 0

    five_by_ten_data = {}
    pms = {
        0: pm,
        1: pm - (0.1 * pm),
        2: pm + (0.1 * pm),
        3: pm - (0.2 * pm),
        4: pm + (0.2 * pm),
    }
    children_dict = {}
    for i in range(5):
        cur_pm = pms[i]
        five_by_ten_data[i] = {
            "pm": cur_pm,
            "runs": []
        }
        print("---------------------------------------------------------------")
        print("Current Pm = " + str(cur_pm))
        print("Cycle #" + str(i))
        runs = 0
        while True:
            print("Run #" + str(runs))
            if runs in children_dict:
                pass
            else:
                children_dict[runs] = create_children(n, l)
            nfe_counts, average_nfe, best_nfe, hemingman_distance, progon_successful = main(children_dict[runs], n,
                                                                                            t, cur_pm)
            runs += 1
            five_by_ten_data[i]["runs"].append({
                "NFE": nfe_counts,
                "Середнє здоров'я в популяції": average_nfe,
                "Найкраще здоров'я в популяції": best_nfe,
                "Відхилення середнього здоров'я": abs(average_nfe - 1),
                "Відхилення найкращого здоров'я": abs(best_nfe - 1),
                "Геммінгова відстань": hemingman_distance,
                "Успішний": 1 if progon_successful else 0,
            })
            if runs == 10:
                break
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(five_by_ten_data)
    return fifteen_by_ten_data, five_by_ten_data

##########################################################################################################################################################
# Функція пристосованності
##########################################################################################################################################################

# the goal ('fitness') function to be maximized
def nfe2(children, l):
    health_of_all = []

    for child in children:
        k = len(child) - sum(child)  # number of zeros in binary string???
        health_of_all.append((l - k) + k * delta)
    best = sorted(health_of_all)[len(health_of_all) - 1]
    average = reduce(lambda x, y: x + y, health_of_all) / len(health_of_all)
    return health_of_all, best, average


############################################################################################################################################################

#
# def ProbabilityList(population_d):
#     fitness = population_d.values()
#     total_fit = sum(fitness)
#     relative_fitness = [f / total_fit for f in fitness]
#     return relative_fitness


def FitnessChoices(population, relative_fitness, number):
    return random.choices(population, weights=relative_fitness, k=number)
# Source:  https://stackoverflow.com/questions/47226362/roulette-wheel-selection-for-non-ordered-fitness-values

def mutation(children, pm):
    local_children = copy.copy(children)
    amount_of_mutations = int(len(local_children) * len(local_children[0]) * pm)
    for i in range(amount_of_mutations):
        index = random.randint(0, len(local_children) * len(local_children[0]) - 1)
        index_of_chrom = math.floor(index / len(local_children[0]))
        index_of_gen = index - ((index_of_chrom) * len(local_children[0]))
        chrom = copy.copy(local_children[index_of_chrom])
        chrom[index_of_gen] = mutate(local_children[index_of_chrom], index_of_gen)
        local_children[index_of_chrom] = chrom

    return local_children


def mutate(children, index):
    return 1 if children[index] == 0 else 0


def create_children(n, l):
    children = []
    for i in range(n):
        child = []
        for k in range(l):
            child.append(random.choice([0, 1]))
        children.append(child)
    return children


def _exiting_population():
    pass

##########################################################################################################################################################
#Тут задається розмір!!!!
##########################################################################################################################################################

for delta in list_of_deltas:
    print('run with delta = ',delta, 'and_L_value', L_value)
    fifteen_by_ten_data, five_by_ten_data = cycle(100, L_value, 2, 0.2, 0.1)
    # count average
    average_and_best_fifteen = {
    }
    for i in fifteen_by_ten_data:
        print('fifteen_by_ten_data started ' + i)
        average_and_best_fifteen[i] = {}
        for progon in fifteen_by_ten_data[i]['runs']:
            for key in progon.keys():
                average_and_best_fifteen[i][key] = {}
                if progon["Успішний"] == 1:
                    try:
                        average_and_best_fifteen[i][key]['data'].append(progon[key])
                    except:
                        average_and_best_fifteen[i][key]['data'] = [progon[key]]
                else:
                    average_and_best_fifteen[i][key]['data'] = []
    for pm in average_and_best_fifteen:
        print('average_and_best_fefteen started ', pm)
        for key in average_and_best_fifteen[pm].keys():
            if average_and_best_fifteen[pm][key]['data']:
                average_and_best_fifteen[pm][key]['average'] = reduce(lambda x, y: x + y,
                                                                      average_and_best_fifteen[pm][key]['data']) / len(
                    average_and_best_fifteen[pm][key]['data'])
                average_and_best_fifteen[pm][key]['best'] = sorted(average_and_best_fifteen[pm][key]['data'])[0]
                if key == "Середнє здоров'я в популяції": average_and_best_fifteen[pm][key]['best'] = \
                sorted(average_and_best_fifteen[pm][key]['data'])[len(average_and_best_fifteen[pm][key]['data']) - 1]
                if key == "Найкраще здоров'я в популяції": average_and_best_fifteen[pm][key]['best'] = \
                sorted(average_and_best_fifteen[pm][key]['data'])[len(average_and_best_fifteen[pm][key]['data']) - 1]
            else:
                average_and_best_fifteen[pm][key]['average'] = 0
                average_and_best_fifteen[pm][key]['best'] = 0
    print("#############")
    print(average_and_best_fifteen)
    print("#############")
    average_and_best_five = {
    }
    for i in five_by_ten_data:
        print('fife_by_ten_data started ', i)
        average_and_best_five[i] = {}
        for progon in five_by_ten_data[i]['runs']:
            for key in progon.keys():
                average_and_best_five[i][key] = {}
                if progon["Успішний"] == 1:
                    try:
                        average_and_best_five[i][key]['data'].append(progon[key])
                    except:
                        average_and_best_five[i][key]['data'] = [progon[key]]
                else:
                    average_and_best_five[i][key]['data'] = []
    for pm in average_and_best_five:
        print('average_and_best_five started ', pm)
        for key in average_and_best_five[pm].keys():
            if average_and_best_five[pm][key]['data']:
                average_and_best_five[pm][key]['average'] = reduce(lambda x, y: x + y,
                                                                   average_and_best_five[pm][key]['data']) / len(
                    average_and_best_five[pm][key]['data'])
                average_and_best_five[pm][key]['best'] = sorted(average_and_best_five[pm][key]['data'])[0]
                if key == "Середнє здоров'я в популяції": average_and_best_five[pm][key]['best'] = \
                sorted(average_and_best_five[pm][key]['data'])[len(average_and_best_five[pm][key]['data']) - 1]
                if key == "Найкраще здоров'я в популяції": average_and_best_five[pm][key]['best'] = \
                sorted(average_and_best_five[pm][key]['data'])[len(average_and_best_five[pm][key]['data']) - 1]
            else:
                average_and_best_five[pm][key]['average'] = 0
                average_and_best_five[pm][key]['best'] = 0

    print("#############")
    print(average_and_best_five)
    print("#############")

##########################################################################################################################################################
# Export to excel
##########################################################################################################################################################

    workbook = xlsxwriter.Workbook('data_with_delta=', delta, '_and_L=', L_value ,'.xlsx')
    worksheet_1 = workbook.add_worksheet()
    worksheet_2 = workbook.add_worksheet()

    row = 0
    col = 0

    worksheet_1.write(row, col, "Конфігурація Pm:")
    for i in range(10):
        worksheet_1.write(row, col + 1, "Прогін {0}".format(i + 1))
        col += 7
    worksheet_1.write(row, col + 1, "Середнє по всім прогонам")
    col += 7
    worksheet_1.write(row, col + 1, "Найкраще по всім прогонам")
    col += 7
    worksheet_1.write(row, col + 1, "Suc Runs")

    row = 1

    for i in five_by_ten_data:
        col = 0
        if row == 1:
            for progon in five_by_ten_data[i]['runs']:
                for k in progon.keys():
                    col += 1
                    worksheet_1.write(row, col, k)
            for key in average_and_best_five[i].keys():
                col += 1
                worksheet_1.write(row, col, key)
            for key in average_and_best_five[i].keys():
                col += 1
                worksheet_1.write(row, col, key)

            col = 0
            row += 1
            worksheet_1.write(row, col, five_by_ten_data[i]['pm'])
            for progon in five_by_ten_data[i]['runs']:
                for key in progon.keys():
                    col += 1
                    worksheet_1.write(row, col, progon[key])
            for key in average_and_best_five[i].keys():
                col += 1
                worksheet_1.write(row, col, average_and_best_five[i][key]['average'])
            for key in average_and_best_five[i].keys():
                col += 1
                worksheet_1.write(row, col, average_and_best_five[i][key]['best'])
            col += 1
            print('##########')
            print(i)
            print(average_and_best_five[i])
            worksheet_1.write(row, col, str((len(average_and_best_five[i]['Успішний']['data']) / 10) * 100) + "%")

        else:
            worksheet_1.write(row, col, five_by_ten_data[i]['pm'])
            for progon in five_by_ten_data[i]['runs']:
                for key in progon.keys():
                    col += 1
                    worksheet_1.write(row, col, progon[key])
            for key in average_and_best_five[i].keys():
                col += 1
                worksheet_1.write(row, col, average_and_best_five[i][key]['average'])
            for key in average_and_best_five[i].keys():
                col += 1
                worksheet_1.write(row, col, average_and_best_five[i][key]['best'])
            col += 1
            print('##########')
            print(i)
            print(average_and_best_five[i])
            worksheet_1.write(row, col, str((len(average_and_best_five[i]['Успішний']['data']) / 10) * 100) + "%")

        row += 1

    """
    ##############################################################################
    """

    row_2 = 0
    col_2 = 0

    worksheet_2.write(row_2, col_2, "Конфігурація Pm:")
    for i in range(10):
        worksheet_2.write(row_2, col_2 + 1, "Прогін {0}".format(i + 1))
        col_2 += 7
    worksheet_2.write(row_2, col_2 + 1, "Середнє по всім прогонам")
    col_2 += 7
    worksheet_2.write(row_2, col_2 + 1, "Найкраще по всім прогонам")
    col_2 += 7
    worksheet_2.write(row_2, col_2 + 1, "Suc Runs")

    row_2 = 1
    for i in fifteen_by_ten_data:
        col_2 = 0
        if row_2 == 1:
            for progon in fifteen_by_ten_data[i]['runs']:
                for k in progon.keys():
                    col_2 += 1
                    worksheet_2.write(row_2, col_2, k)
            for key in average_and_best_fifteen[i].keys():
                col_2 += 1
                worksheet_2.write(row_2, col_2, key)
            for key in average_and_best_fifteen[i].keys():
                col_2 += 1
                worksheet_2.write(row_2, col_2, key)

            col_2 = 0
            row_2 += 1
            worksheet_2.write(row_2, col_2, fifteen_by_ten_data[i]['pm'])
            for progon in fifteen_by_ten_data[i]['runs']:
                for key in progon.keys():
                    col_2 += 1
                    worksheet_2.write(row_2, col_2, progon[key])
            for key in average_and_best_fifteen[i].keys():
                col_2 += 1
                worksheet_2.write(row_2, col_2, average_and_best_fifteen[i][key]['average'])
            for key in average_and_best_fifteen[i].keys():
                col_2 += 1
                worksheet_2.write(row_2, col_2, average_and_best_fifteen[i][key]['best'])
            col_2 += 1
            print('##########')
            print(i)
            print(average_and_best_fifteen[i])
            worksheet_2.write(row_2, col_2, str((len(average_and_best_fifteen[i]['Успішний']['data']) / 10) * 100) + "%")

        else:
            worksheet_2.write(row_2, col_2, fifteen_by_ten_data[i]['pm'])
            for progon in fifteen_by_ten_data[i]['runs']:
                for key in progon.keys():
                    col_2 += 1
                    worksheet_2.write(row_2, col_2, progon[key])
            for key in average_and_best_fifteen[i].keys():
                col_2 += 1
                worksheet_2.write(row_2, col_2, average_and_best_fifteen[i][key]['average'])
            for key in average_and_best_fifteen[i].keys():
                col_2 += 1
                worksheet_2.write(row_2, col_2, average_and_best_fifteen[i][key]['best'])
            col_2 += 1
            print('##########')
            print(i)
            print(average_and_best_fifteen[i])
            worksheet_2.write(row_2, col_2, str((len(average_and_best_fifteen[i]['Успішний']['data']) / 10) * 100) + "%")

        row_2 += 1

    workbook.close()
