import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="线上课程用户行为洞察，个性化学习新策略！",
    # page_icon="👋",
    layout='wide',
)

col = st.columns(4)
col_names = ['首页', '行为分析', '智能推荐']
col[0].write(col_names[0])
py_names = ['1_User Behavior Analysis.py', '2_Intelligent Recommendation.py']
for i in range(1, 3):
    with col[i]:
        st.page_link(f"pages/{py_names[i-1]}", label=col_names[i])

st.write("# 欢迎来到洞察环节！ 👋")
st.write(
    '''
线上课程智能推荐策略，旨在通过多维数据分析，为每位用户精准推送个性化课程，优化学习体验，提升学习效率，实现资源高效利用。🎯

📚 在数据收集方面，策略会记录用户的学习历史、课程点击量、完成率等信息，形成用户画像和课程画像。

💡 在算法模型方面，策略会运用机器学习等技术，对用户和课程进行深度匹配，实现个性化推荐。

🔄 在反馈机制方面，策略会根据用户的反馈和行为变化，不断优化推荐结果，确保推荐的准确性。

通过这种智能推荐策略，线上课程平台能够为用户提供更加贴心、高效的学习体验，让学习变得更加轻松有趣！😊
'''
)

#%% 多媒体组件
img = plt.imread('image.jpg')
st.image(img)
