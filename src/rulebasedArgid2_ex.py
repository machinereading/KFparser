
# coding: utf-8

# In[5]:


import rulebasedArgid2
import json


# In[6]:


input_seq = [[['0',
   'Goodwill의',
   'Goodwill/SL+의/JKG',
   'Goodwill의',
   'SL+JKG',
   'SL+JKG',
   '_',
   '_',
   '1',
   '1',
   'NP_MOD',
   'NP_MOD',
   '_',
   '_'],
  ['1',
   '노력이',
   '노력/NNG+이/JKS',
   '노력이',
   'NNG+JKS',
   'NNG+JKS',
   '_',
   '_',
   '4',
   '4',
   'NP_SBJ',
   'NP_SBJ',
   '_',
   '_'],
  ['2',
   '우리',
   '우리/NP',
   '우리',
   'NP',
   'NP',
   '_',
   '_',
   '3',
   '3',
   'NP',
   'NP',
   '_',
   '_'],
  ['3',
   '공동체에',
   '공동체/NNG+에/JKB',
   '공동체에',
   'NNG+JKB',
   'NNG+JKB',
   '_',
   '_',
   '4',
   '4',
   'NP_AJT',
   'NP_AJT',
   '_',
   '_'],
  ['4',
   '끼친',
   '끼치/VV+ㄴ/ETM',
   '끼친',
   'VV+ETM',
   'VV+ETM',
   '_',
   '_',
   '5',
   '5',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['5',
   '영향력과',
   '영향력/NNG+과/JKB',
   '영향력과',
   'NNG+JKB',
   'NNG+JKB',
   '_',
   '_',
   '6',
   '6',
   'NP_AJT',
   'NP_AJT',
   '영향력.n',
   'Objective_influence'],
  ['6',
   '같이.',
   '같이/MAG+./SF',
   '같이.',
   'MAG+SF',
   'MAG+SF',
   '_',
   '_',
   '-1',
   '-1',
   'AP',
   'AP',
   '_',
   '_']],
 [['0',
   '당신의',
   '당신/NP+의/JKG',
   '당신의',
   'NP+JKG',
   'NP+JKG',
   '_',
   '_',
   '1',
   '1',
   'NP_MOD',
   'NP_MOD',
   '_',
   '_'],
  ['1',
   '관대함으로부터',
   '관대하/VV+ㅁ/ETN+으로부터/JKB',
   '관대함으로부터',
   'VV+ETN+JKB',
   'VV+ETN+JKB',
   '_',
   '_',
   '5',
   '5',
   'VP_AJT',
   'VP_AJT',
   '_',
   '_'],
  ['2',
   '가장',
   '가장/MAG',
   '가장',
   'MAG',
   'MAG',
   '_',
   '_',
   '3',
   '3',
   'AP',
   'AP',
   '_',
   '_'],
  ['3',
   '직접적으로',
   '직접적/NNG+으로/JKB',
   '직접적으로',
   'NNG+JKB',
   'NNG+JKB',
   '_',
   '_',
   '5',
   '5',
   'NP_AJT',
   'NP_AJT',
   '_',
   '_'],
  ['4',
   '혜택을',
   '혜택/NNG+을/JKO',
   '혜택을',
   'NNG+JKO',
   'NNG+JKO',
   '_',
   '_',
   '5',
   '5',
   'NP_OBJ',
   'NP_OBJ',
   '_',
   '_'],
  ['5',
   '받을',
   '받/VV+을/ETM',
   '받을',
   'VV+ETM',
   'VV+ETM',
   '_',
   '_',
   '6',
   '6',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['6',
   '수',
   '수/NNB',
   '수',
   'NNB',
   'NNB',
   '_',
   '_',
   '7',
   '7',
   'NP_SBJ',
   'NP_SBJ',
   '_',
   '_'],
  ['7',
   '있는',
   '있/VA+는/ETM',
   '있는',
   'VA+ETM',
   'VA+ETM',
   '_',
   '_',
   '8',
   '8',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['8',
   '사람들은',
   '사람들/NNG+은/JX',
   '사람들은',
   'NNG+JX',
   'NNG+JX',
   '_',
   '_',
   '11',
   '11',
   'NP_SBJ',
   'NP_SBJ',
   '사람.n',
   'People'],
  ['9',
   '낭비할',
   '낭비하/VV+ㄹ/ETM',
   '낭비할',
   'VV+ETM',
   'VV+ETM',
   '_',
   '_',
   '10',
   '10',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['10',
   '시간을',
   '시간/NNG+을/JKO',
   '시간을',
   'NNG+JKO',
   'NNG+JKO',
   '_',
   '_',
   '11',
   '11',
   'NP_OBJ',
   'NP_OBJ',
   '_',
   '_'],
  ['11',
   '갖지',
   '갖/VV+지/EC',
   '갖지',
   'VV+EC',
   'VV+EC',
   '_',
   '_',
   '12',
   '12',
   'VP',
   'VP',
   '_',
   '_'],
  ['12',
   '못한다.',
   '못하/VX+ㄴ다/EF+./SF',
   '못한다.',
   'VX+EF+SF',
   'VX+EF+SF',
   '_',
   '_',
   '-1',
   '-1',
   'VP',
   'VP',
   '_',
   '_']],
 [['0',
   '당신의',
   '당신/NP+의/JKG',
   '당신의',
   'NP+JKG',
   'NP+JKG',
   '_',
   '_',
   '1',
   '1',
   'NP_MOD',
   'NP_MOD',
   '_',
   '_'],
  ['1',
   '관대함으로부터',
   '관대하/VV+ㅁ/ETN+으로부터/JKB',
   '관대함으로부터',
   'VV+ETN+JKB',
   'VV+ETN+JKB',
   '_',
   '_',
   '5',
   '5',
   'VP_AJT',
   'VP_AJT',
   '_',
   '_'],
  ['2',
   '가장',
   '가장/MAG',
   '가장',
   'MAG',
   'MAG',
   '_',
   '_',
   '3',
   '3',
   'AP',
   'AP',
   '_',
   '_'],
  ['3',
   '직접적으로',
   '직접적/NNG+으로/JKB',
   '직접적으로',
   'NNG+JKB',
   'NNG+JKB',
   '_',
   '_',
   '5',
   '5',
   'NP_AJT',
   'NP_AJT',
   '_',
   '_'],
  ['4',
   '혜택을',
   '혜택/NNG+을/JKO',
   '혜택을',
   'NNG+JKO',
   'NNG+JKO',
   '_',
   '_',
   '5',
   '5',
   'NP_OBJ',
   'NP_OBJ',
   '_',
   '_'],
  ['5',
   '받을',
   '받/VV+을/ETM',
   '받을',
   'VV+ETM',
   'VV+ETM',
   '_',
   '_',
   '6',
   '6',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['6',
   '수',
   '수/NNB',
   '수',
   'NNB',
   'NNB',
   '_',
   '_',
   '7',
   '7',
   'NP_SBJ',
   'NP_SBJ',
   '수.n',
   'Possibility'],
  ['7',
   '있는',
   '있/VA+는/ETM',
   '있는',
   'VA+ETM',
   'VA+ETM',
   '_',
   '_',
   '8',
   '8',
   'VP_MOD',
   'VP_MOD',
   '수.n',
   'Possibility'],
  ['8',
   '사람들은',
   '사람들/NNG+은/JX',
   '사람들은',
   'NNG+JX',
   'NNG+JX',
   '_',
   '_',
   '11',
   '11',
   'NP_SBJ',
   'NP_SBJ',
   '_',
   '_'],
  ['9',
   '낭비할',
   '낭비하/VV+ㄹ/ETM',
   '낭비할',
   'VV+ETM',
   'VV+ETM',
   '_',
   '_',
   '10',
   '10',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['10',
   '시간을',
   '시간/NNG+을/JKO',
   '시간을',
   'NNG+JKO',
   'NNG+JKO',
   '_',
   '_',
   '11',
   '11',
   'NP_OBJ',
   'NP_OBJ',
   '_',
   '_'],
  ['11',
   '갖지',
   '갖/VV+지/EC',
   '갖지',
   'VV+EC',
   'VV+EC',
   '_',
   '_',
   '12',
   '12',
   'VP',
   'VP',
   '_',
   '_'],
  ['12',
   '못한다.',
   '못하/VX+ㄴ다/EF+./SF',
   '못한다.',
   'VX+EF+SF',
   'VX+EF+SF',
   '_',
   '_',
   '-1',
   '-1',
   'VP',
   'VP',
   '_',
   '_']],
 [['0',
   '당신의',
   '당신/NP+의/JKG',
   '당신의',
   'NP+JKG',
   'NP+JKG',
   '_',
   '_',
   '1',
   '1',
   'NP_MOD',
   'NP_MOD',
   '_',
   '_'],
  ['1',
   '관대함으로부터',
   '관대하/VV+ㅁ/ETN+으로부터/JKB',
   '관대함으로부터',
   'VV+ETN+JKB',
   'VV+ETN+JKB',
   '_',
   '_',
   '5',
   '5',
   'VP_AJT',
   'VP_AJT',
   '_',
   '_'],
  ['2',
   '가장',
   '가장/MAG',
   '가장',
   'MAG',
   'MAG',
   '_',
   '_',
   '3',
   '3',
   'AP',
   'AP',
   '_',
   '_'],
  ['3',
   '직접적으로',
   '직접적/NNG+으로/JKB',
   '직접적으로',
   'NNG+JKB',
   'NNG+JKB',
   '_',
   '_',
   '5',
   '5',
   'NP_AJT',
   'NP_AJT',
   '_',
   '_'],
  ['4',
   '혜택을',
   '혜택/NNG+을/JKO',
   '혜택을',
   'NNG+JKO',
   'NNG+JKO',
   '_',
   '_',
   '5',
   '5',
   'NP_OBJ',
   'NP_OBJ',
   '_',
   '_'],
  ['5',
   '받을',
   '받/VV+을/ETM',
   '받을',
   'VV+ETM',
   'VV+ETM',
   '_',
   '_',
   '6',
   '6',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['6',
   '수',
   '수/NNB',
   '수',
   'NNB',
   'NNB',
   '_',
   '_',
   '7',
   '7',
   'NP_SBJ',
   'NP_SBJ',
   '_',
   '_'],
  ['7',
   '있는',
   '있/VA+는/ETM',
   '있는',
   'VA+ETM',
   'VA+ETM',
   '_',
   '_',
   '8',
   '8',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['8',
   '사람들은',
   '사람들/NNG+은/JX',
   '사람들은',
   'NNG+JX',
   'NNG+JX',
   '_',
   '_',
   '11',
   '11',
   'NP_SBJ',
   'NP_SBJ',
   '_',
   '_'],
  ['9',
   '낭비할',
   '낭비하/VV+ㄹ/ETM',
   '낭비할',
   'VV+ETM',
   'VV+ETM',
   '_',
   '_',
   '10',
   '10',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['10',
   '시간을',
   '시간/NNG+을/JKO',
   '시간을',
   'NNG+JKO',
   'NNG+JKO',
   '_',
   '_',
   '11',
   '11',
   'NP_OBJ',
   'NP_OBJ',
   '_',
   '_'],
  ['11',
   '갖지',
   '갖/VV+지/EC',
   '갖지',
   'VV+EC',
   'VV+EC',
   '_',
   '_',
   '12',
   '12',
   'VP',
   'VP',
   '갖다.v',
   'Possession'],
  ['12',
   '못한다.',
   '못하/VX+ㄴ다/EF+./SF',
   '못한다.',
   'VX+EF+SF',
   'VX+EF+SF',
   '_',
   '_',
   '-1',
   '-1',
   'VP',
   'VP',
   '_',
   '_']],
 [['0',
   '당신의',
   '당신/NP+의/JKG',
   '당신의',
   'NP+JKG',
   'NP+JKG',
   '_',
   '_',
   '1',
   '1',
   'NP_MOD',
   'NP_MOD',
   '_',
   '_'],
  ['1',
   '관대함으로부터',
   '관대하/VV+ㅁ/ETN+으로부터/JKB',
   '관대함으로부터',
   'VV+ETN+JKB',
   'VV+ETN+JKB',
   '_',
   '_',
   '5',
   '5',
   'VP_AJT',
   'VP_AJT',
   '_',
   '_'],
  ['2',
   '가장',
   '가장/MAG',
   '가장',
   'MAG',
   'MAG',
   '_',
   '_',
   '3',
   '3',
   'AP',
   'AP',
   '_',
   '_'],
  ['3',
   '직접적으로',
   '직접적/NNG+으로/JKB',
   '직접적으로',
   'NNG+JKB',
   'NNG+JKB',
   '_',
   '_',
   '5',
   '5',
   'NP_AJT',
   'NP_AJT',
   '_',
   '_'],
  ['4',
   '혜택을',
   '혜택/NNG+을/JKO',
   '혜택을',
   'NNG+JKO',
   'NNG+JKO',
   '_',
   '_',
   '5',
   '5',
   'NP_OBJ',
   'NP_OBJ',
   '_',
   '_'],
  ['5',
   '받을',
   '받/VV+을/ETM',
   '받을',
   'VV+ETM',
   'VV+ETM',
   '_',
   '_',
   '6',
   '6',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['6',
   '수',
   '수/NNB',
   '수',
   'NNB',
   'NNB',
   '_',
   '_',
   '7',
   '7',
   'NP_SBJ',
   'NP_SBJ',
   '_',
   '_'],
  ['7',
   '있는',
   '있/VA+는/ETM',
   '있는',
   'VA+ETM',
   'VA+ETM',
   '_',
   '_',
   '8',
   '8',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['8',
   '사람들은',
   '사람들/NNG+은/JX',
   '사람들은',
   'NNG+JX',
   'NNG+JX',
   '_',
   '_',
   '11',
   '11',
   'NP_SBJ',
   'NP_SBJ',
   '_',
   '_'],
  ['9',
   '낭비할',
   '낭비하/VV+ㄹ/ETM',
   '낭비할',
   'VV+ETM',
   'VV+ETM',
   '_',
   '_',
   '10',
   '10',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['10',
   '시간을',
   '시간/NNG+을/JKO',
   '시간을',
   'NNG+JKO',
   'NNG+JKO',
   '_',
   '_',
   '11',
   '11',
   'NP_OBJ',
   'NP_OBJ',
   '_',
   '_'],
  ['11',
   '갖지',
   '갖/VV+지/EC',
   '갖지',
   'VV+EC',
   'VV+EC',
   '_',
   '_',
   '12',
   '12',
   'VP',
   'VP',
   '_',
   '_'],
  ['12',
   '못한다.',
   '못하/VX+ㄴ다/EF+./SF',
   '못한다.',
   'VX+EF+SF',
   'VX+EF+SF',
   '_',
   '_',
   '-1',
   '-1',
   'VP',
   'VP',
   '못하다.a',
   'Quantity']],
 [['0',
   '당신의',
   '당신/NP+의/JKG',
   '당신의',
   'NP+JKG',
   'NP+JKG',
   '_',
   '_',
   '1',
   '1',
   'NP_MOD',
   'NP_MOD',
   '_',
   '_'],
  ['1',
   '지원은',
   '지원/NNG+은/JX',
   '지원은',
   'NNG+JX',
   'NNG+JX',
   '_',
   '_',
   '4',
   '4',
   'NP_SBJ',
   'NP_SBJ',
   '_',
   '_'],
  ['2',
   '실질적인',
   '실질적/NNG+이/VCP+ㄴ/ETM',
   '실질적인',
   'NNG+VCP+ETM',
   'NNG+VCP+ETM',
   '_',
   '_',
   '3',
   '3',
   'VNP_MOD',
   'VNP_MOD',
   '_',
   '_'],
  ['3',
   '해결책을',
   '해결책/NNG+을/JKO',
   '해결책을',
   'NNG+JKO',
   'NNG+JKO',
   '_',
   '_',
   '4',
   '4',
   'NP_OBJ',
   'NP_OBJ',
   '_',
   '_'],
  ['4',
   '제공하도록',
   '제공하/VV+도록/EC',
   '제공하도록',
   'VV+EC',
   'VV+EC',
   '_',
   '_',
   '5',
   '5',
   'VP',
   'VP',
   '_',
   '_'],
  ['5',
   '돕는다.',
   '돕/VV+는다/EF+./SF',
   '돕는다.',
   'VV+EF+SF',
   'VV+EF+SF',
   '_',
   '_',
   '-1',
   '-1',
   'VP',
   'VP',
   '돕다.v',
   'Assistance']],
 [['0',
   '당신의',
   '당신/NP+의/JKG',
   '당신의',
   'NP+JKG',
   'NP+JKG',
   '_',
   '_',
   '1',
   '1',
   'NP_MOD',
   'NP_MOD',
   '_',
   '_'],
  ['1',
   '지원은',
   '지원/NNG+은/JX',
   '지원은',
   'NNG+JX',
   'NNG+JX',
   '_',
   '_',
   '4',
   '4',
   'NP_SBJ',
   'NP_SBJ',
   '지원.n',
   'Supporting'],
  ['2',
   '실질적인',
   '실질적/NNG+이/VCP+ㄴ/ETM',
   '실질적인',
   'NNG+VCP+ETM',
   'NNG+VCP+ETM',
   '_',
   '_',
   '3',
   '3',
   'VNP_MOD',
   'VNP_MOD',
   '_',
   '_'],
  ['3',
   '해결책을',
   '해결책/NNG+을/JKO',
   '해결책을',
   'NNG+JKO',
   'NNG+JKO',
   '_',
   '_',
   '4',
   '4',
   'NP_OBJ',
   'NP_OBJ',
   '_',
   '_'],
  ['4',
   '제공하도록',
   '제공하/VV+도록/EC',
   '제공하도록',
   'VV+EC',
   'VV+EC',
   '_',
   '_',
   '5',
   '5',
   'VP',
   'VP',
   '_',
   '_'],
  ['5',
   '돕는다.',
   '돕/VV+는다/EF+./SF',
   '돕는다.',
   'VV+EF+SF',
   'VV+EF+SF',
   '_',
   '_',
   '-1',
   '-1',
   'VP',
   'VP',
   '_',
   '_']],
 [['0',
   '우리는',
   '우리/NP+는/JX',
   '우리는',
   'NP+JX',
   'NP+JX',
   '_',
   '_',
   '9',
   '9',
   'NP_SBJ',
   'NP_SBJ',
   '_',
   '_'],
  ['1',
   '장애를',
   '장애/NNG+를/JKO',
   '장애를',
   'NNG+JKO',
   'NNG+JKO',
   '_',
   '_',
   '2',
   '2',
   'NP_OBJ',
   'NP_OBJ',
   '_',
   '_'],
  ['2',
   '가진',
   '가지/VV+ㄴ/ETM',
   '가진',
   'VV+ETM',
   'VV+ETM',
   '_',
   '_',
   '3',
   '3',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['3',
   '사람들이',
   '사람들/NNG+이/JKS',
   '사람들이',
   'NNG+JKS',
   'NNG+JKS',
   '_',
   '_',
   '6',
   '6',
   'NP_SBJ',
   'NP_SBJ',
   '사람.n',
   'People'],
  ['4',
   '노동',
   '노동/NNG',
   '노동',
   'NNG',
   'NNG',
   '_',
   '_',
   '5',
   '5',
   'NP',
   'NP',
   '_',
   '_'],
  ['5',
   '인구에',
   '인구/NNG+에/JKB',
   '인구에',
   'NNG+JKB',
   'NNG+JKB',
   '_',
   '_',
   '6',
   '6',
   'NP_AJT',
   'NP_AJT',
   '_',
   '_'],
  ['6',
   '포함되도록',
   '포함되/VV+도록/EC',
   '포함되도록',
   'VV+EC',
   'VV+EC',
   '_',
   '_',
   '7',
   '7',
   'VP',
   'VP',
   '_',
   '_'],
  ['7',
   '하는',
   '하/VX+는/ETM',
   '하는',
   'VX+ETM',
   'VX+ETM',
   '_',
   '_',
   '8',
   '8',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['8',
   '방안들을',
   '방안들/NNG+을/JKO',
   '방안들을',
   'NNG+JKO',
   'NNG+JKO',
   '_',
   '_',
   '9',
   '9',
   'NP_OBJ',
   'NP_OBJ',
   '_',
   '_'],
  ['9',
   '찾았습니다.',
   '찾/VV+었/EP+습니다/EF+./SF',
   '찾았습니다.',
   'VV+EP+EF+SF',
   'VV+EP+EF+SF',
   '_',
   '_',
   '-1',
   '-1',
   'VP',
   'VP',
   '_',
   '_']],
 [['0',
   '우리는',
   '우리/NP+는/JX',
   '우리는',
   'NP+JX',
   'NP+JX',
   '_',
   '_',
   '9',
   '9',
   'NP_SBJ',
   'NP_SBJ',
   '_',
   '_'],
  ['1',
   '장애를',
   '장애/NNG+를/JKO',
   '장애를',
   'NNG+JKO',
   'NNG+JKO',
   '_',
   '_',
   '2',
   '2',
   'NP_OBJ',
   'NP_OBJ',
   '_',
   '_'],
  ['2',
   '가진',
   '가지/VV+ㄴ/ETM',
   '가진',
   'VV+ETM',
   'VV+ETM',
   '_',
   '_',
   '3',
   '3',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['3',
   '사람들이',
   '사람들/NNG+이/JKS',
   '사람들이',
   'NNG+JKS',
   'NNG+JKS',
   '_',
   '_',
   '6',
   '6',
   'NP_SBJ',
   'NP_SBJ',
   '_',
   '_'],
  ['4',
   '노동',
   '노동/NNG',
   '노동',
   'NNG',
   'NNG',
   '_',
   '_',
   '5',
   '5',
   'NP',
   'NP',
   '_',
   '_'],
  ['5',
   '인구에',
   '인구/NNG+에/JKB',
   '인구에',
   'NNG+JKB',
   'NNG+JKB',
   '_',
   '_',
   '6',
   '6',
   'NP_AJT',
   'NP_AJT',
   '_',
   '_'],
  ['6',
   '포함되도록',
   '포함되/VV+도록/EC',
   '포함되도록',
   'VV+EC',
   'VV+EC',
   '_',
   '_',
   '7',
   '7',
   'VP',
   'VP',
   '_',
   '_'],
  ['7',
   '하는',
   '하/VX+는/ETM',
   '하는',
   'VX+ETM',
   'VX+ETM',
   '_',
   '_',
   '8',
   '8',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['8',
   '방안들을',
   '방안들/NNG+을/JKO',
   '방안들을',
   'NNG+JKO',
   'NNG+JKO',
   '_',
   '_',
   '9',
   '9',
   'NP_OBJ',
   'NP_OBJ',
   '_',
   '_'],
  ['9',
   '찾았습니다.',
   '찾/VV+었/EP+습니다/EF+./SF',
   '찾았습니다.',
   'VV+EP+EF+SF',
   'VV+EP+EF+SF',
   '_',
   '_',
   '-1',
   '-1',
   'VP',
   'VP',
   '찾다.v',
   'Intentionally_create']],
 [['0',
   '우리는',
   '우리/NP+는/JX',
   '우리는',
   'NP+JX',
   'NP+JX',
   '_',
   '_',
   '9',
   '9',
   'NP_SBJ',
   'NP_SBJ',
   '_',
   '_'],
  ['1',
   '장애를',
   '장애/NNG+를/JKO',
   '장애를',
   'NNG+JKO',
   'NNG+JKO',
   '_',
   '_',
   '2',
   '2',
   'NP_OBJ',
   'NP_OBJ',
   '_',
   '_'],
  ['2',
   '가진',
   '가지/VV+ㄴ/ETM',
   '가진',
   'VV+ETM',
   'VV+ETM',
   '_',
   '_',
   '3',
   '3',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['3',
   '사람들이',
   '사람들/NNG+이/JKS',
   '사람들이',
   'NNG+JKS',
   'NNG+JKS',
   '_',
   '_',
   '6',
   '6',
   'NP_SBJ',
   'NP_SBJ',
   '_',
   '_'],
  ['4',
   '노동',
   '노동/NNG',
   '노동',
   'NNG',
   'NNG',
   '_',
   '_',
   '5',
   '5',
   'NP',
   'NP',
   '_',
   '_'],
  ['5',
   '인구에',
   '인구/NNG+에/JKB',
   '인구에',
   'NNG+JKB',
   'NNG+JKB',
   '_',
   '_',
   '6',
   '6',
   'NP_AJT',
   'NP_AJT',
   '_',
   '_'],
  ['6',
   '포함되도록',
   '포함되/VV+도록/EC',
   '포함되도록',
   'VV+EC',
   'VV+EC',
   '_',
   '_',
   '7',
   '7',
   'VP',
   'VP',
   '_',
   '_'],
  ['7',
   '하는',
   '하/VX+는/ETM',
   '하는',
   'VX+ETM',
   'VX+ETM',
   '_',
   '_',
   '8',
   '8',
   'VP_MOD',
   'VP_MOD',
   '_',
   '_'],
  ['8',
   '방안들을',
   '방안들/NNG+을/JKO',
   '방안들을',
   'NNG+JKO',
   'NNG+JKO',
   '_',
   '_',
   '9',
   '9',
   'NP_OBJ',
   'NP_OBJ',
   '방안.n',
   'Means'],
  ['9',
   '찾았습니다.',
   '찾/VV+었/EP+습니다/EF+./SF',
   '찾았습니다.',
   'VV+EP+EF+SF',
   'VV+EP+EF+SF',
   '_',
   '_',
   '-1',
   '-1',
   'VP',
   'VP',
   '_',
   '_']]]


# In[7]:


with open("./rulebased2_argid_features.json", "r", encoding = 'utf-8') as make_file:
    feature_list = json.load(make_file)


# In[8]:


print(rulebasedArgid2.arg_id(input_seq, feature_list))

