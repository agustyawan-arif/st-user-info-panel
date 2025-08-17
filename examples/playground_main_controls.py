# examples/playground_main_controls.py
from __future__ import annotations

from pprint import pformat
from typing import Any, Dict

import streamlit as st
from st_user_info_panel import st_user_info_panel


# ---------- Helpers ----------
DEFAULT_CFG: Dict[str, Any] = {
    # Identity
    "name": "Sarah Johnson",
    "job_title": "Senior Data Scientist",
    "email": "sarah.johnson@techcorp.com",
    "avatar_color": "#FE5556",
    "department": "Data Platform",
    "work_location": "Jakarta",
    # Stats
    "messages_count": 340,
    "monthly_messages_limit": 500,
    "tokens_this_month": 3_200_000,
    "monthly_tokens_limit": 10_000_000,
    "cost_usd": 42.35,
    "monthly_cost_limit": 200.0,
    "show_detailed_stats": True,
    # Layout & behavior
    "attach_mode": "portal",      # "portal" | "inside"
    "side_padding_px": 12,
    "bottom_offset_px": 16,
    "border_radius_px": 12,
    "compact": True,
    "stats_style": "rows",        # "rows" | "cards"
    "show_progress": False,
    # State control (default: uncontrolled)
    "controlled": False,
    "expanded": False,
    "key": "user-panel",  # IMPORTANT: Streamlit component key
}


def ensure_state() -> None:
    """Initialize session state safely."""
    if "panel_cfg" not in st.session_state:
        st.session_state.panel_cfg = DEFAULT_CFG.copy()
    if "user_panel_expanded" not in st.session_state:
        st.session_state.user_panel_expanded = bool(DEFAULT_CFG["expanded"])
    if "history_count" not in st.session_state:
        st.session_state.history_count = 12


def code_for_cfg(cfg: Dict[str, Any]) -> str:
    """Return a minimal, nicely formatted call snippet for the current config."""
    # Only show non-defaults to keep snippet tidy
    # (here we include everything for clarity)
    ordered = {
        "name": cfg["name"],
        "job_title": cfg["job_title"],
        "email": cfg["email"],
        "avatar_color": cfg["avatar_color"],
        "department": cfg.get("department") or "",
        "work_location": cfg.get("work_location") or "",
        "messages_count": cfg["messages_count"],
        "monthly_messages_limit": cfg["monthly_messages_limit"],
        "tokens_this_month": cfg["tokens_this_month"],
        "monthly_tokens_limit": cfg["monthly_tokens_limit"],
        "cost_usd": cfg["cost_usd"],
        "monthly_cost_limit": cfg["monthly_cost_limit"],
        "show_detailed_stats": cfg["show_detailed_stats"],
        "compact": cfg["compact"],
        "stats_style": cfg["stats_style"],
        "show_progress": cfg["show_progress"],
        "side_padding_px": cfg["side_padding_px"],
        "bottom_offset_px": cfg["bottom_offset_px"],
        "attach_mode": cfg["attach_mode"],
        "controlled": cfg["controlled"],
        "expanded": cfg["expanded"],
    }
    # Build a call using kwargs for readability
    body = ",\n        ".join(f"{k}={pformat(v)}" for k, v in ordered.items())
    return (
        "from st_user_info_panel import st_user_info_panel\n\n"
        "result = st_user_info_panel(\n"
        f"        {body},\n"
        ")\n"
        "if result and result.get('event') == 'logout':\n"
        "    st.warning('Logout clicked')\n"
    )


# ---------- App ----------
def main() -> None:
    st.set_page_config(
        page_title="AI Chat Assistant – Panel Playground",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    ensure_state()

    # === MAIN AREA: Controls + live code ===
    st.title("AI Chat Assistant with User Info Panel Demo")
    
    with st.expander("Panel controls", expanded=False):
        with st.form("panel_controls"):
            st.subheader("Panel Controls")

            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown("**Identity**")
                name = st.text_input("Name", st.session_state.panel_cfg["name"])
                title = st.text_input("Job title", st.session_state.panel_cfg["job_title"])
                email = st.text_input("Email", st.session_state.panel_cfg["email"])
                color = st.color_picker("Avatar color", st.session_state.panel_cfg["avatar_color"])
                dept = st.text_input("Department", st.session_state.panel_cfg.get("department", ""))
                loc = st.text_input("Work location", st.session_state.panel_cfg.get("work_location", ""))

                st.markdown("---")
                st.markdown("**Stats**")
                show_stats = st.checkbox(
                    "Show detailed stats",
                    value=st.session_state.panel_cfg["show_detailed_stats"],
                )

                colA, colB = st.columns(2)
                with colA:
                    messages = st.number_input(
                        "Messages this month",
                        0, 1_000_000,
                        st.session_state.panel_cfg["messages_count"],
                        step=10,
                    )
                    tokens = st.number_input(
                        "Tokens this month",
                        0, 10_000_000_000,
                        st.session_state.panel_cfg["tokens_this_month"],
                        step=10_000,
                    )
                    cost = st.number_input(
                        "Cost this month (USD)",
                        0.0, 1_000_000.0,
                        float(st.session_state.panel_cfg["cost_usd"]),
                        step=0.05,
                    )
                with colB:
                    msg_limit = st.number_input(
                        "Monthly messages limit (0=none)",
                        0, 1_000_000,
                        st.session_state.panel_cfg["monthly_messages_limit"],
                        step=50,
                    )
                    tok_limit = st.number_input(
                        "Monthly tokens limit (0=none)",
                        0, 10_000_000_000,
                        st.session_state.panel_cfg["monthly_tokens_limit"],
                        step=100_000,
                    )
                    cost_limit = st.number_input(
                        "Monthly cost limit (0=none)",
                        0.0, 1_000_000.0,
                        float(st.session_state.panel_cfg["monthly_cost_limit"]),
                        step=1.0,
                    )

            with c2:
                st.markdown("**Layout & Behavior**")
                attach_mode = st.selectbox(
                    "Attach mode",
                    ["portal", "inside"],
                    index=0 if st.session_state.panel_cfg["attach_mode"] == "portal" else 1,
                )
                compact = st.checkbox("Compact", value=st.session_state.panel_cfg["compact"])
                stats_style = st.selectbox(
                    "Stats style",
                    ["rows", "cards"],
                    index=0 if st.session_state.panel_cfg["stats_style"] == "rows" else 1,
                )
                show_progress = st.checkbox(
                    "Show progress bars",
                    value=st.session_state.panel_cfg["show_progress"],
                )
                side_padding_px = st.slider(
                    "Side padding (px)",
                    0, 24, int(st.session_state.panel_cfg["side_padding_px"]), 1
                )
                bottom_offset_px = st.slider(
                    "Bottom offset (px)",
                    0, 48, int(st.session_state.panel_cfg["bottom_offset_px"]), 1
                )
                border_radius_px = st.slider(
                    "Border radius (px)",
                    6, 20, int(st.session_state.panel_cfg["border_radius_px"]), 1
                )

                st.markdown("---")
                st.markdown("**State control**")
                controlled = st.checkbox("Controlled by host (advanced)", value=st.session_state.panel_cfg["controlled"])
                if controlled:
                    st.toggle("Expanded (controlled)", key="user_panel_expanded")

                st.markdown("---")
                st.markdown("**Chat history**")
                st.session_state.history_count = st.slider(
                    "Number of recent conversations in sidebar",
                    0, 50, st.session_state.history_count, 1
                )

            applied = st.form_submit_button("✅ Apply changes", use_container_width=True)
            if applied:
                st.session_state.panel_cfg.update(
                    dict(
                        # identity
                        name=name, job_title=title, email=email,
                        avatar_color=color, department=dept, work_location=loc,
                        # stats
                        messages_count=int(messages),
                        monthly_messages_limit=int(msg_limit),
                        tokens_this_month=int(tokens),
                        monthly_tokens_limit=int(tok_limit),
                        cost_usd=float(cost),
                        monthly_cost_limit=float(cost_limit),
                        show_detailed_stats=bool(show_stats),
                        # layout
                        attach_mode=attach_mode,
                        side_padding_px=int(side_padding_px),
                        bottom_offset_px=int(bottom_offset_px),
                        border_radius_px=int(border_radius_px),
                        compact=bool(compact),
                        stats_style=stats_style,
                        show_progress=bool(show_progress),
                        # state control
                        controlled=bool(controlled),
                        expanded=bool(st.session_state.user_panel_expanded),
                        key="user-panel"
                    )
                )
                st.success("Applied. Rerunning …")
                st.rerun()

    with st.expander("Live code", expanded=False):
        # Show live code for current config
        st.markdown("### Current call")
        st.code(code_for_cfg(st.session_state.panel_cfg), language="python")

    # === SIDEBAR: chat history + the panel ===
    with st.sidebar:
        st.title("🤖 AI Assistant")
        st.subheader("Recent Conversations")
        for i in range(st.session_state.history_count):
            st.markdown(f"• Chat {i+1}")

        st.markdown("---")
        st.subheader("Settings")
        st.selectbox("Model", ["GPT-4", "Claude", "Gemini"], index=0)
        st.slider("Temperature", 0.0, 2.0, 0.7, 0.05)

        # Render the user panel (floating at the bottom of the sidebar)
        cfg = st.session_state.panel_cfg.copy()
        # Keep expanded in sync when controlled
        if cfg.get("controlled"):
            cfg["expanded"] = bool(st.session_state.user_panel_expanded)

        result = st_user_info_panel(**cfg)

        # Handle events from component
        if result:
            evt = result.get("event")
            if evt == "toggle":
                st.session_state.user_panel_expanded = result["expanded"]
            elif evt == "logout":
                st.session_state.user_panel_expanded = False
                st.warning("Logout clicked")
            elif evt == "view_profile":
                st.session_state.user_panel_expanded = False
                st.info("Profile clicked")

    # === Main chat area (dummy) ===
    st.subheader("💬 Chat Interface")
    with st.chat_message("user"):
        st.write("Hello! How can you help me today?")
    with st.chat_message("assistant"):
        st.write("Hi! I can help with data analysis, Q&A, and more.")
    if prompt := st.chat_input("Type your message..."):
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            st.write("This is a demo response.")


if __name__ == "__main__":
    main()