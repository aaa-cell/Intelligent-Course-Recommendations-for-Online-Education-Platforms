import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px
from chinese_calendar import is_workday
plt.rcParams['font.sans-serif'] = 'SimHei'

st.set_page_config(
    page_title="线上课程",
    # page_icon="👋",
    layout='wide',
)

st.write("## 不同省份的登录情况")

user = pd.read_csv('./temp/user.csv',parse_dates=['recently_logged','register_time'])
logg = pd.read_csv('./temp/logg.csv',parse_dates=['login_time'])
study = pd.read_csv('./temp/study.csv')

# 绘制地图
st.components.v1.html(open('./temp/map.html', 'r').read(), width=800, height=600)


st.write("## 用户活跃分析")

logg['is_workday'] = logg['login_time'].apply(is_workday)
logg['hour'] = logg['login_time'].dt.hour
# 统计每个时间段、每个工作日非工作日的登录人数
workday_count = logg.groupby(by=['is_workday','hour']).agg({'user_id':'count'}).reset_index()
# 使用plotly express绘制非堆叠的柱状图
fig = px.bar(workday_count, x='hour', y='user_id', color='is_workday', barmode='group')
# 显示图表
st.plotly_chart(fig)

st.write("## 用户流失分析")
col1, col2 = st.columns(2)
with col1:
    # 判断用户是否流失
    user['leave'] = (pd.to_datetime('2020-6-19') - user['recently_logged']).dt.days>90
    # 用户流失与课程数量的关系
    num_clasess = user[user['leave']==True].groupby(by='number_of_classes_join')['leave'].sum().reset_index()
    # 使用plotly express绘制非堆叠的柱状图
    fig = px.bar(num_clasess, x='number_of_classes_join', y='leave',title='流失用户的课程总数')
    # 显示图表
    st.plotly_chart(fig)

# 非流失用户与课程数量的关系
with col2:
    num_clasess2 = user[user['leave']==False].groupby(by='number_of_classes_join')['leave'].count().reset_index()
    fig = px.bar(num_clasess2, x='number_of_classes_join', y='leave',title='未流失用户的课程总数')
    # 显示图表
    st.plotly_chart(fig)

st.write("## 课程受欢迎情况分析")
study['course_id'] = study['course_id'].str.replace('课程','') # 处理课程
study['learn_process'] = study['learn_process'].str.replace('width: ','').str.replace('%;','') # 处理进度
course_num = study['course_id'].value_counts() # 计算课程被参与的次数
# 计算选择每门课后的累计占比
p = course_num.cumsum()/course_num.sum()
# 找到80%的位置的课程
key = p[p>0.8].index[0]
# 找到该课程所在的位置
keu_num = p.index.tolist().index(key)
# 绘制帕累托图
# 绘制帕累托图
fig, ax = plt.subplots(figsize=(14, 6))
course_num[:50].plot(kind='bar', ax=ax) # 绘制柱形图
p.plot(style='--', secondary_y=True, color='b', ax=ax)
ax.axvline(keu_num, color='r', linestyle='--')
ax.text(keu_num, p[key] - 0.05, f'{round(p[key]*100, 2)}%, 数量{keu_num}', color='red',
        fontsize=15,verticalalignment='bottom')
# 设置图表标题和标签
plt.title('课程受欢迎情况分析')
plt.xlabel('课程')
plt.ylabel('次数')
plt.show()
# 在Streamlit中显示图表
st.pyplot(fig)

st.write("## 收费差异与学习进度的关系")
study['learn_process'] = study['learn_process'].astype(int)
learn = study.groupby(by='course_id')['learn_process','price'].mean() # 统计每门课程的平均进度和价格
# 在Streamlit中显示图表
fig = sns.pairplot(data=learn, diag_kind='kde')
st.pyplot(fig)
