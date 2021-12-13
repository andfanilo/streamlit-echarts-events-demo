import streamlit as st
from streamlit_echarts import st_echarts
from vega_datasets import data

st.title("ECharts Events Demo")

df = data.us_employment().set_index("month").drop(columns=["nonfarm_change"])
means = df.mean(axis=0).map("{:.2f}".format)

bar_options = {
    "title": {"text": "Mean US employment this past decade"},
    "xAxis": {
        "type": "category",
        "axisTick": {"alignWithLabel": True},
        "data": means.index.values.tolist(),
    },
    "yAxis": {"type": "value"},
    "tooltip": {"trigger": "item"},
    "emphasis": {"itemStyle": {"color": "#a90000"}},
    "series": [{"data": means.tolist(), "type": "bar"}],
}

clicked_label = st_echarts(
    bar_options,
    events={"mouseover": "function(params) {return params.name}"},
    height="500px",
    key="global",
)

if clicked_label is None:
    st.stop()

filtered_df = df[clicked_label].sort_index()
line_options = {
    "title": {"text": f"Breakdown US employment for {clicked_label}"},
    "xAxis": {
        "type": "category",
        "axisTick": {"alignWithLabel": True},
        "data": filtered_df.index.values.tolist(),
    },
    "yAxis": {"type": "value"},
    "tooltip": {"trigger": "axis"},
    "itemStyle": {"color": "#a90000"},
    "lineStyle": {"color": "#a90000"},
    "series": [
        {
            "data": filtered_df.tolist(),
            "type": "line",
            "smooth": True,
        }
    ],
}
clicked_label = st_echarts(line_options, key="detail")
