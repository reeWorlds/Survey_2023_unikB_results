# -*- coding: windows-1251 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

g_mp = {'³������':0, '�������':1, '�������':2, '�������':3}

df = pd.read_csv('../data.csv')

df_teh = df[df['�� ���� �� ����� ��������� �� ������� �����? (�����, ������)'] == '���']
df_n_teh = df[df['�� ���� �� ����� ��������� �� ������� �����? (�����, ������)'] == 'ͳ']

def showAgeDistribution(df, path, title_full):
    plt.clf()
    plt.rcParams.update({'font.size': 20})

    age = df['������ ��� ��'].copy()
    age = age[pd.to_numeric(age, errors='coerce').notnull()]
    age = age.astype(float)
    age = age.astype(int)
    age[age >= 25] = '25+'
    age = age.astype(str)

    age_counts = age.value_counts().sort_index()
    percentages = age_counts.values / age_counts.values.sum() * 100

    bars = plt.bar(age_counts.index.astype(str), age_counts.values)
    
    plt.title(title_full)
    plt.xlabel('ʳ������ ����')
    plt.ylabel('ʳ������ ��������')

    plt.savefig(path, dpi=200, bbox_inches='tight')

#showAgeDistribution(df, "plts/��_��.png", "��� ������")
#showAgeDistribution(df_teh, "plts/��_���.png", "���. ��������")
#showAgeDistribution(df_n_teh, "plts/��_�����.png", "�����. ��������")

def newDraw1Main_avg(tdf, num):
    col_name = tdf.columns[num]
    col = tdf[col_name]

    tSum = 0
    tCnt = 0

    for x in col:
        if x in g_mp:
            tSum += g_mp[x]
            tCnt += 1

    return tSum / tCnt

def newDraw1Main():
    num = 28 # 3..7  8..17  19..28

    plt.rcParams.update({'font.size': 14})

    parameters = ['��� ������', '���.', '�����.']
    answers = ['³������', '�������', '�������', '�������', '����� �������']

    color_dict = {'³������':'green', '�������':'blue', '�������':'yellow', \
       '�������':'red', '����� �������':'purple'}

    fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    
    for i, ax in enumerate(axs):
        tdf = df
        if i == 1:
            tdf = df_teh
        elif i == 2:
            tdf = df_n_teh

        col_name = tdf.columns[num]
        data = tdf[col_name].value_counts()

        actual_answers = [ans for ans in answers if ans in data.index]
        data_b = [data[ans] for ans in actual_answers]

        ax.bar(actual_answers, data_b, color=[color_dict[ans] for ans in actual_answers], alpha=0.7)
        ax.set_title(f'{parameters[i]}', rotation=0)

        print(newDraw1Main_avg(tdf, num))

    patches = [mpatches.Patch(color=color, label=label) for label, color in color_dict.items()]
    fig.legend(handles=patches, loc='upper right', bbox_to_anchor=(1.15, 0.85))

    for ax in axs:
        ax.set_xticklabels([])

    plt.tight_layout()
    plt.savefig('plts/new_' + str(num - 2) + '.png', dpi=200, bbox_inches='tight')

#newDraw1Main()

def newDraw2_avg(tdf, rowi, indexType):
    idx = []
    if indexType == 'all':
        print("here")
        idx.extend(range(3, 8))
        idx.extend(range(8, 18))
        idx.extend(range(19, 29))
    else:
        idx.extend(range(8, 18))
        
    score = 0
    score_cnt = 0

    for i in idx:
        val = tdf.iat[rowi, i]
        if val in g_mp:
            score += g_mp[val]
            score_cnt += 1

    return score / score_cnt

def newDraw2(tp1, tp2):
    tdf = df
    if tp1 == 1:
        tdf = df_teh
    elif tp1 == 2:
        tdf = df_n_teh

    name = "��� ������"
    if tp1 == 1:
        name = "���."
    elif tp1 == 2:
        name = "�����."

    plt.rcParams.update({'font.size': 16})

    scores = [newDraw2_avg(tdf, i, tp2) for i in range(len(tdf))]
    tot = 0
    for s in scores:
        tot += s
    tot /= len(scores)
    print(tot)

    plt.cla()
    plt.hist(scores, bins=10, range=(0,3), rwidth=0.8)

    plt.title(name)
    plt.xlabel("������� ������")
    plt.ylabel("ʳ������ ��������")

    plt.savefig('plts/new2_' + str(tp1) + '_' + tp2 + '.png', dpi=200, bbox_inches='tight')

#newDraw2(0, 'all')
#newDraw2(1, 'all')
#newDraw2(2, 'all')
#newDraw2(0, 'psych')
#newDraw2(1, 'psych')
#newDraw2(2, 'psych')

def process1(vals):
    vals.remove(vals[3])
    vals.remove(vals[1])

    return vals

def process2_1(col):
    def replace_values2(val):
        if pd.notnull(val) and val != '���' and val != 'ͳ' and val != '������':
            return '������� ������������� ����������'
        else:
            return val

    col = col.apply(replace_values2)
    return col

def process2_2(vals):
    vals.remove(vals[1])

    return vals

def process3_1(vals):
    vals.remove(vals[2])

    return vals

def process3_2(vals):
    vals = ['���, �� ���� �����\n� ���������� �����\n����� ���������.', \
        '���, �� ���� �������\n������ ����� ���������\n�� ����������.', \
        'ͳ, �� ��� �����,\n�� ���� ������\n�������� �����.']

    return vals

def process4(vals):
    vals = ['������ ������,\n�� �� ������', '������� ������', '������ �� ������,\n�� ������']

    return vals

def process5(vals):
    vals = ['���, ��� �����\n����� ��������', '���, �����\n����� ������', 'ͳ, �����\n����� ����']

    return vals

def process6(vals):
    vals = ['ͳ, �� ���� ��\n���� ����������', '���, ������������\n�������', \
            '���, ��� �����������\n���� ���������']

    return vals

def process7_1(vals):
    return vals[:3]

def process7_2(vals):
    vals = ['ͳ, ��\n�������������', '���, ��������\n�������������',\
       '�������� �, ���\n������������� �\n������������� � �������\n����� �����']

    return vals

def process8(vals):
    return vals[:4]

def process9(vals):
    vals.remove(vals[2])
    vals.remove(vals[2])

    return vals[:4]

def process10_1(vals):
    return vals[:3]

def process10_2(vals):
    vals = ['ͳ, ����\n�������\n��������', '���, ������\n�������\n��������',
            '��������, ������\n������� ��������']

    return vals

def process11_1(vals):
    return vals[:3]

def process11_2(vals):
    vals = ['���������, ��� �����\n�������� ���� ����\n������ ���������', \
        '���, ����������\n��������� �������', 'ͳ, ���������� ��\n���� ����������']

    return vals

def process12(vals):
    return vals[:3]

def newDraw3(name):
    idx = 43 # 30..35 37..43

    col_name = df.columns[idx]
    col = df[col_name]

    #col = process2_1(col) # 31

    vals = col.unique().tolist()
    print(vals)

    #vals = process1(vals) # 30
    #vals = process2_2(vals) # 31
    #vals = process3_1(vals) # 32
    #vals = process7_1(vals) # 37
    #vals = process8(vals) # 38
    #vals = process9(vals) # 39
    #vals = process10_1(vals) # 40
    #vals = process11_1(vals) # 42
    #vals = process12(vals) # 43
    
    frequencies = col.value_counts().loc[vals].fillna(0)

    labels = frequencies.index.tolist()
    #labels = process3_2(labels) # 32
    #labels = process4(labels) # 33
    #labels = process5(labels) # 34
    #labels = process6(labels) # 35
    #labels = process7_2(labels) # 37
    #labels = process10_2(labels) # 40
    #labels = process11_2(labels) # 42

    plt.rcParams.update({'font.size': 16})
    plt.pie(frequencies, labels=labels, autopct='%1.1f%%')
    
    plt.savefig('plts/new3_' + name + '.png', dpi=200, bbox_inches='tight')

#newDraw3('19')

def newDraw4():
    ans = set()

    for i in range(79):
        ans.update(set(df.iat[i, 36].split(';')))

    ans = list(ans)

    cnt = [0 for i in range(len(ans))]

    for i in range(79):
        for j in range(len(ans)):
            if ans[j] in df.iat[i, 36].split(';'):
                cnt[j] += 1
    
    for i, x in enumerate(cnt):
        cnt[i] = x / 79 * 100

    sorted_lists = sorted(zip(cnt, ans), reverse=True)
    cnt, ans = zip(*sorted_lists)

    ans = list(ans)

    ans[0] = '��������-�������\n(�����, �����,\n������ ����)'
    ans[1] = '������ (������,\n���� ����)'
    ans[2] = '���� ���\n������'
    ans[3] = '������ ����������\n(����, ������\n������������ ����)'
    ans[4] = '����� ��������\n(�����, ����������)'

    cnt = cnt[:5]
    ans = ans[:5]
    
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(lambda x, _: f'{x}%')

    plt.barh(ans, cnt, color='blue', alpha=0.7)

    plt.savefig('plts/new4.png', dpi=200, bbox_inches='tight')

#newDraw4()