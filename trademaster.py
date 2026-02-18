import streamlit as st



# Page Configuration for Mobile Responsiveness
st.set_page_config(page_title="TradeMaster Pro", layout="centered")

# Custom CSS for Large Fonts and High Contrast
st.markdown("""
    <style>
    .result-box {
        background-color: white;
        border: 2px solid #333;
        border-radius: 10px;
        padding: 30px;
        text-align: center;
        margin-top: 20px;
    }
    .main-header { font-size: 24px !important; font-weight: bold; color: #333; }
    .investment-text { font-size: 14px; color: #666; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 TradeMaster Pro")
# tab1, tab2 = st.tabs(["Stock Averaging", "Options Calculator"])
tab1, tab2, tab3 = st.tabs(["Stock Averaging", "Options Calculator", "Live Option Chain"])


# --- TAB 1: STOCK AVERAGING ---
with tab1:
    st.markdown("<p class='main-header'>Equity 3-Tier Averaging</p>", unsafe_allow_html=True)

    stk_total_val = 0
    stk_total_qty = 0

    col1, col2 = st.columns(2)
    for i in range(3):
        with col1:
            price = st.number_input(f"Buy {i + 1} Price (₹)", min_value=0.0, step=0.1, key=f"stk_p{i}")
        with col2:
            qty = st.number_input(f"Buy {i + 1} Quantity", min_value=0, step=1, key=f"stk_q{i}")

        slot_cost = price * qty
        stk_total_val += slot_cost
        stk_total_qty += qty
        st.markdown(f"<p class='investment-text'>Slot {i + 1} Investment: ₹{slot_cost:,.2f}</p>",
                    unsafe_allow_html=True)

    if st.button("Calculate Stock Average"):
        if stk_total_qty > 0:
            avg_price = stk_total_val / stk_total_qty
            st.markdown(f"""
                <div class="result-box">
                    <h2 style="color:#003366;">NEW AVERAGE PRICE</h2>
                    <h1 style="font-size:40px; color:#003366;">₹{avg_price:,.2f}</h1>
                    <p style="font-size:18px;">Total Qty: {stk_total_qty} | Total Invested: ₹{stk_total_val:,.2f}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Please enter quantity to calculate.")

# --- TAB 2: OPTIONS CALCULATOR ---
with tab2:
    st.markdown("<p class='main-header'>Options 3-Tier & Brokerage</p>", unsafe_allow_html=True)

    opt_total_buy_val = 0
    opt_total_qty = 0
    orders_count = 0

    # Global Parameters in Sidebar or Top
    c1, c2, c3 = st.columns(3)
    with c1:
        lot_size = st.number_input("Lot Size", value=65, step=1)
    with c2:
        br_per_order = st.number_input("Brokerage/Order (₹)", value=20.0)
    with c3:
        exit_price = st.number_input("Exit Price (₹)", min_value=0.0)

    st.divider()

    col_a, col_b = st.columns(2)
    for i in range(3):
        with col_a:
            p = st.number_input(f"Buy {i + 1} Price (₹)", min_value=0.0, key=f"opt_p{i}")
        with col_b:
            lots = st.number_input(f"Buy {i + 1} Lots", min_value=0, key=f"opt_l{i}")

        if lots > 0:
            qty = lots * lot_size
            cost = p * qty
            opt_total_buy_val += cost
            opt_total_qty += qty
            orders_count += 1
            st.markdown(f"<p class='investment-text'>Slot {i + 1} Investment: ₹{cost:,.2f}</p>", unsafe_allow_html=True)

    if st.button("Calculate Options P&L"):
        if opt_total_qty > 0:
            total_sell_val = exit_price * opt_total_qty
            total_brokerage = (orders_count + 1) * br_per_order
            taxes = (opt_total_buy_val + total_sell_val) * 0.0006
            total_costs = total_brokerage + taxes

            net_pnl = (total_sell_val - opt_total_buy_val) - total_costs
            avg_buy = opt_total_buy_val / opt_total_qty

            pnl_color = "#006400" if net_pnl >= 0 else "#cc0000"

            st.markdown(f"""
                <div class="result-box">
                    <p style="font-size:18px; color:#666;">Avg Buy: ₹{avg_buy:,.2f} | Charges: ₹{total_costs:,.2f}</p>
                    <h2 style="color:{pnl_color};">NET PROFIT/LOSS</h2>
                    <h1 style="font-size:45px; color:{pnl_color};">₹{net_pnl:,.2f}</h1>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Please enter lot quantity and exit price.")
