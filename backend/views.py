from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import pandas as pd
import json
import ast
from tqdm import tqdm
import numpy as np
from scipy.spatial.distance import euclidean
from collections import Counter
import math


# Create your views here.
def getClusterdata(request):
    # 生成画图的数据
    stuInfo = pd.read_csv('backend/static/learnerProfile_2021.csv')

    val = ['-', 'CR', 'ER', 'TS', 'EQ', 'MQ', 'HQ']
    val_full = ['number', 'Correct', 'Error', 'Total Submissions', 'Easy questions', 'Medium questions', 'Hard questions']

    selectX = request.GET['selectX']
    selectY = request.GET['selectY']

    selected_stuInfo = stuInfo.iloc[:, [0, val.index(selectX), val.index(selectY), 7]]

    # 重新命名所有列
    selected_stuInfo.columns = ['name', 'x', 'y', 'cluster']

    res_t = []

    for index, row in selected_stuInfo.iterrows():
        stu_i = {
            'name': row['name'],
            'x': int(row['x']),
            'y': int(row['y']),
            'cluster': int(row['cluster'])
        }
        res_t.append(stu_i)

    res = {
        'xname': val_full[val.index(selectX)],
        'yname': val_full[val.index(selectY)],
        'clusterInfo': res_t
    }

    return JsonResponse(res)

def getPatteroverviewdata(request):
    df1 = pd.read_csv('backend/static/RNP_2021.csv')
    df2 = pd.read_csv('backend/static/20240505-submitRecord-StageSeq-Cluster-2021.csv')

    df1.insert(0, 'number', df2['number'])

    df1.insert(1, 'cluster', df2['Cluster'])

    # 修改分类，将0、1、2等级统一替换为'Normal'
    df1['cluster'] = df1['cluster'].replace([0, 1, 2, 3], 'Normal')

    df1['cluster'] = df1['cluster'].replace([4], 'Abnormal')

    grouped_df = df1.iloc[:, 2:]

    grouped_df['cluster'] = df1['cluster']

    grouped_sum = grouped_df.groupby('cluster').sum()

    # 分别遍历每个等级的结果
    pat_count = 1
    pat_List = []
    max_pat = 0
    total_normal = 0
    total_abnormal = 0

    for level, data in grouped_sum.iteritems():
        pat_List.append({
            'name': 'Pat_' + str(pat_count),
            'value': [int(data[1]), int(data[0])]
        })
        # 记录总的正常模式数量
        total_normal += data[1]
        # 记录总的异常模式数量
        total_abnormal += data[0]
        # 记录最大值
        max_temp = data[1] + data[0]
        if max_temp > max_pat:
            max_pat = max_temp
        pat_count += 1

    res = {
        'total': int(pat_count)-1,
        'ratio': [{"name": "Normal", "value": total_normal/(total_normal+total_abnormal)}, {"name": "Abnormal", "value": total_abnormal/(total_normal+total_abnormal)}],
        'patternList': pat_List,
        'patternMax': int(max_pat)
    }
    return JsonResponse(res)

def getAbnormaldata(request):
    selectType = request.GET['type']
    selectAttr = request.GET['attr']
    file_1 = ''
    file_2 = ''
    if selectType=="IS":
        file_1 = 'inferenceScore'
    else:
        file_1 = 'rawValue'

    if selectAttr=="1":
        file_2 = 'Result'
    elif selectAttr=="2":
        file_2 = 'Difficulty'
    elif selectAttr=="3":
        file_2 = 'Skill'
    else:
        file_2 = 'Practice'

    with open('./backend/static/'+file_1+'-'+file_2+'.json', 'r') as fp:
        ret_roles = fp.read()
    fp.close()
    return HttpResponse(ret_roles)


def getPatternexploredata(request):
    with open('./backend/static/patternExplore.json', 'r') as fp:
        ret_roles = fp.read()
    fp.close()
    return HttpResponse(ret_roles)

def getPatterncompare(request):
    source = request.GET['source']

    target = request.GET['target']
    df2_pattern = pd.read_csv('./backend/static/pattern-compare.csv')

    source_col_index = int(source.split('_')[1])

    target_col_index = int(target.split('_')[1])

    # 计算涉及的学习者数量
    source_column = df2_pattern.iloc[:, source_col_index]
    source_non_zero_values = source_column[source_column != 0]
    source_sum_non_zero = source_non_zero_values.sum()

    target_column = df2_pattern.iloc[:, target_col_index]
    target_non_zero_values = target_column[target_column != 0]
    target_sum_non_zero = target_non_zero_values.sum()

    # 计算涉及的事件数量
    source_col_name = df2_pattern.columns[source_col_index]
    target_col_name = df2_pattern.columns[target_col_index]

    source_parsed_list = ast.literal_eval(source_col_name)
    target_parsed_list = ast.literal_eval(target_col_name)

    # 计算多样性
    # 统计每个类别的频数
    source_counts = Counter(elem[0] for elem in source_parsed_list)
    source_total_instances = sum(source_counts.values())
    source_probabilities = [count / source_total_instances for count in source_counts.values()]
    source_entropy = abs(-sum(p * math.log2(p) for p in source_probabilities))

    target_counts = Counter(elem[0] for elem in target_parsed_list)
    target_total_instances = sum(target_counts.values())
    target_probabilities = [count / target_total_instances for count in target_counts.values()]
    target_entropy = abs(-sum(p * math.log2(p) for p in target_probabilities))

    title_skill = ['-', '1', '2', '2', '2', '2', '3', '3', '3', '3', '3', '4', '4', '4', '4', '4', '4', '5', '5', '6',
                   '7', '7', '7', '7', '7', '7', '7', '7', '8', '8', '9', '10', '10', '10', '11', '10', '12', '12',
                   '13']

    # 计算涉及知识点数量
    source_skill_count = [title_skill[int(elem[1][0])] for elem in enumerate(source_parsed_list)]
    target_skill_count = [title_skill[int(elem[1][0])] for elem in enumerate(target_parsed_list)]

    # 将 NumPy int64 类型转换为 Python int 类型
    def convert_to_builtin_type(obj):
        if isinstance(obj, np.int64):
            return int(obj)
        raise TypeError("Object of type '{}' is not JSON serializable".format(type(obj)))

    ret_roles = {
        'radarData': [
            {'name': source, 'value': [{'axis': 'Total Event', 'value': len(source_parsed_list)},
                                       {'axis': 'Total Learner', 'value': source_sum_non_zero},
                                       {'axis': 'Event Diversity', 'value': source_entropy},
                                       {'axis': 'Total Knowledge', 'value': len(source_skill_count)}]},
            {'name': target, 'value': [{'axis': 'Total Event', 'value': len(target_parsed_list)},
                                       {'axis': 'Total Learner', 'value': target_sum_non_zero},
                                       {'axis': 'Event Diversity', 'value': target_entropy},
                                       {'axis': 'Total Knowledge', 'value': len(target_skill_count)}]}
        ],
        'hist': [
            df2_pattern[df2_pattern.iloc[:, source_col_index] != 0]['learning performance'].tolist(),
            df2_pattern[df2_pattern.iloc[:, target_col_index] != 0]['learning performance'].tolist()
        ]
    }
    return JsonResponse(ret_roles, safe=False, json_dumps_params={'default': convert_to_builtin_type})