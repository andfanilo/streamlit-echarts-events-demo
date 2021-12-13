import streamlit as st
from streamlit_echarts import st_echarts
from vega_datasets import data

def main():
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
        return

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


if __name__ == "__main__":
    st.set_page_config(
        page_title="Streamlit ECharts Events Demo", page_icon=":chart_with_upwards_trend:"
    )
    st.title("ECharts Events Demo")
    main()
    with st.sidebar:
        st.markdown("---")
        st.markdown(
            '<h6><a href="https://github.com/andfanilo/streamlit-echarts-events-demo">Source code</a></h6>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by <a href="https://twitter.com/andfanilo">@andfanilo</a></h6>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="margin-top: 0.75em;"><a href="https://www.buymeacoffee.com/andfanilo" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a></div>',
            unsafe_allow_html=True,
        )
