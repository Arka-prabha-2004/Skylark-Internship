import streamlit as st
from agent import (
    ask_agent,
    get_kpis,
    get_deals_data,
    get_work_orders_data
)

st.set_page_config(
    page_title="Monday BI Agent",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Monday.com Business Intelligence Agent")

# ------------------------------
# FETCH DATA FROM MONDAY
# ------------------------------

deals = get_deals_data()
work_orders = get_work_orders_data()

# ------------------------------
# KPI DASHBOARD
# ------------------------------

deal_count, work_orders_count, sector_count = get_kpis()

col1, col2, col3 = st.columns(3)

col1.metric("📊 Deals in Pipeline", deal_count)
col2.metric("🛠 Active Work Orders", work_orders_count)
col3.metric("🏭 Sectors Covered", sector_count)

st.markdown(
"""
Ask questions about **pipeline health, sectors, deals, and work orders**.

This AI agent queries **monday.com boards live** and generates insights for leadership.
"""
)

st.markdown("### Example Questions")

st.markdown(
"""
• How many deals are in the pipeline?  
• Which sector has the most deals?  
• Which deals are closing this quarter?  
• How many work orders are completed?  
• Generate a leadership update
"""
)

# ------------------------------
# SIDEBAR
# ------------------------------

with st.sidebar:

    st.header("About")

    st.write(
        """
        This AI agent analyzes business data from monday.com boards.

        Features:
        - Live monday.com API queries
        - Pipeline insights
        - Sector performance analysis
        - Leadership updates
        """
    )

    st.divider()

    st.subheader("Source Boards")

    st.link_button(
        "📊 Open Deals Board",
        "https://arkaprabha05022004s-team.monday.com/boards/5026988160",
        use_container_width=True
    )

    st.link_button(
        "🛠 Open Work Orders Board",
        "https://arkaprabha05022004s-team.monday.com/boards/5026988627",
        use_container_width=True
    )

    st.divider()

    show_debug = st.toggle("🔍 Show Agent Trace", value=True)

    st.divider()
    st.caption("Built for Skylark Drones Internship Assignment")

st.info("🟢 Connected to monday.com API")

# ------------------------------
# QUICK ACTION
# ------------------------------

st.subheader("Quick Actions")

if st.button("📈 Generate Leadership Update", use_container_width=True):

    with st.spinner("Preparing leadership update..."):

        response, steps = ask_agent(
            "Prepare a leadership update",
            deals,
            work_orders,
            st.session_state.get("chat_history", [])
        )

    with st.chat_message("assistant"):

        if show_debug:
            with st.expander("Agent Action Trace"):
                for step in steps:
                    st.write(step)

        st.success(response)


# ------------------------------
# CHAT HISTORY
# ------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask a business question...")

if user_input:

    with st.spinner("🔎 Fetching monday.com data and generating insights..."):

        response, steps = ask_agent(
            user_input,
            deals,
            work_orders,
            st.session_state.chat_history
        )

    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("assistant", response))

    if show_debug:
        with st.expander("Agent Action Trace"):
            for step in steps:
                st.write(step)

# ------------------------------
# DISPLAY CHAT
# ------------------------------

for role, message in st.session_state.chat_history:

    if role == "user":
        st.chat_message("user").write(message)

    else:
        st.chat_message("assistant").write(message)

st.divider()

st.caption(
"""
Built using Streamlit, Gemini, and the monday.com API.
"""
)