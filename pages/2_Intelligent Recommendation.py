import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
import plotly.express as px
from mlxtend.frequent_patterns import apriori,association_rules
plt.rcParams['font.sans-serif'] = 'SimHei'

st.set_page_config(
    page_title="智能推荐",
    # page_icon="👋",
    layout='wide',
)


user = pd.read_csv('./temp/user1.csv',parse_dates=['recently_logged','register_time'])
logg = pd.read_csv('./temp/logg1.csv',parse_dates=['login_time'])
study = pd.read_csv('./temp/study1.csv')

## 数据整理
# 删除只注册未使用的学员
user = user[user['number_of_classes_join']>0]
# 删除学习时长为0 的学员
user = user[user['learn_time']>0]

# 删除学习人数少于100的课程
course_num = study['course_id'].value_counts() # 计算课程被参与的次数
course_num = course_num[course_num>100].reset_index()
course_num.columns = ['course_id','numb']
study = pd.merge(study, course_num, how='inner', on='course_id')
study = pd.merge(study, user, how='inner', on='user_id')
# 构造用户-课程矩阵
data = pd.pivot_table(data=study, index='user_id', columns='course_id', 
               values='learn_time',aggfunc='count', fill_value=0)

#  生成频繁项集
frequent = apriori(data,  min_support=0.2, use_colnames=True)

# 生成规则
rules = association_rules(frequent,  metric='lift', min_threshold=1)
def get_items(names, lens):
    '''
    names: 表示购买的物品名
    lens: 表示推荐的前项长度
    '''
    # 将输入的物品名转换为字符串类型
    names = int(names)
    
    # 所有前项
    alltimes = [list(x) for x in rules['antecedents'].values]
    # 找满足条件的规则位置
    indx = [i for i in range(len(alltimes)) if len(alltimes[i]) == lens and alltimes[i][0] == names]
    # 找出对应规则
    item = rules.iloc[indx, :].sort_values(by='lift', ascending=False)
    return item.head()

# 在Streamlit中创建用户界面
st.title("获取推荐商品")
item_name = st.text_input("请输入购买的物品名:")
item_length = st.number_input("请输入推荐的前项长度:", min_value=1, value=2)

# 当用户点击按钮时执行推荐函数并显示结果
if st.button("获取推荐"):
    recommended_items = get_items(item_name, item_length)
    st.write(recommended_items)