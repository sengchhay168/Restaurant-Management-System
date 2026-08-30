import streamlit as st
from Services.auth_service import AuthService
from Services.menu_service import MenuService
from Services.table_service import TableService
from Services.order_service import OrderService
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="Restaurant Management System", layout="wide")

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Restaurant Management System", layout="wide")

# Modern High-End POS Theme & Live Clock Styling
st.markdown("""
    <style>
    /* Global background and card styling */
    .stApp {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    
    /* Sleek container borders */
    div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    /* Glow text effect */
    .glow-text {
        color: #00d2ff;
        text-shadow: 0 0 8px rgba(0, 210, 255, 0.8), 0 0 15px rgba(0, 210, 255, 0.5);
        font-weight: 500;
        text-align: right;
    }

    /* Metric and header adjustments */
    h1, h2, h3 {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Live Ticking Digital Clock in the Sidebar
st.sidebar.markdown("### 🕒 Live System Time")

clock_html = """
<div style="background-color: #21262d; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #30363d; font-family: sans-serif;">
    <div id="live-clock" style="font-size: 1rem; font-weight: bold; color: #00d2ff;">Loading...</div>
</div>
<script>
function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    const dateString = now.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' });
    document.getElementById('live-clock').innerHTML = dateString + '<br>' + timeString;
}
setInterval(updateClock, 1000);
updateClock();
</script>
"""
components.html(clock_html, height=75)
st.sidebar.markdown("---")

# Initialize services in session state to persist states across re-runs
if "auth_service" not in st.session_state:
    st.session_state.auth_service = AuthService()
if "menu_service" not in st.session_state:
    st.session_state.menu_service = MenuService()
if "table_service" not in st.session_state:
    st.session_state.table_service = TableService()
if "order_service" not in st.session_state:
    st.session_state.order_service = OrderService(
        st.session_state.menu_service, 
        st.session_state.table_service
    )

auth = st.session_state.auth_service
menu = st.session_state.menu_service
tables = st.session_state.table_service
orders = st.session_state.order_service

st.sidebar.title("Restaurant System")

# Authentication View
if not auth.current_user:
    # Center the login box using columns
    _, center_col, _ = st.columns([1, 1.2, 1])
    
    with center_col:
        st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>Restaurant Management</h2>", unsafe_allow_html=True)
        
        # Initialize toggle state for switching between login and registration
        if "show_register" not in st.session_state:
            st.session_state.show_register = False

        if not st.session_state.show_register:
            # Login Box Container
            with st.container(border=True):
                st.subheader("Staff Login")
                username = st.text_input("Username", key="login_user")
                password = st.text_input("Password", type="password", key="login_pass")
                
                if st.button("Login", use_container_width=True):
                    if auth.login_user(username, password):
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid Username or Password!")
                
                # Bottom right "or register" link/button with blue glow
                col_spacer, col_btn = st.columns([1.5, 1])
                with col_btn:
                    if st.button("or register", key="switch_to_reg", help="Click to register a new user"):
                        st.session_state.show_register = True
                        st.rerun()
        else:
            # Register Box Container
            with st.container(border=True):
                st.subheader("Register User")
                reg_id = st.text_input("User ID", key="reg_id_input")
                reg_user = st.text_input("New Username", key="reg_user_input")
                reg_pass = st.text_input("New Password", type="password", key="reg_pass_input")
                reg_role = st.selectbox("Role", ["staff", "admin"], key="reg_role_input")
                
                if st.button("Register Account", use_container_width=True):
                    if auth.register_user(reg_id, reg_user, reg_pass, reg_role):
                        st.success("Registered successfully! Please log in.")
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error("Registration failed (ID or username may already exist).")
                
                # Back to login link on the bottom right
                col_spacer, col_btn = st.columns([1.5, 1])
                with col_btn:
                    if st.button("back to login", key="switch_to_login"):
                        st.session_state.show_register = False
                        st.rerun()
else:
    st.sidebar.write(f"Logged in as: **{auth.current_user.username}** ({auth.get_current_role()})")
    if st.sidebar.button("Logout"):
        auth.logout()
        st.rerun()

    # Create top-level navigation tabs instead of sidebar selectbox
    tab_pos, tab_menu, tab_table, tab_orders = st.tabs([
        "Point of Sale (POS)", 
        "Menu Management", 
        "Table Management", 
        "Active Orders & Receipts"
    ])

    with tab_pos:
        st.title("Point of Sale")
        
        avail_tables = tables.tables
        table_options = {t.table_id: f"Table {t.table_id} (Capacity: {t.capacity}, Occupied: {t.is_occupied})" for t in avail_tables}
        
        if table_options:
            selected_table_id = st.selectbox("Select Table", list(table_options.keys()), format_func=lambda x: table_options[x], key="pos_table")
            
            st.subheader("Add Items to Order")
            all_menu_items = menu.get_all_items()
            
            if all_menu_items:
                item_options = {item.item_id: f"{item.name} - ${item.price:.2f} ({item.category})" for item in all_menu_items}
                
                if "cart" not in st.session_state:
                    st.session_state.cart = []
                    
                col1, col2 = st.columns(2)
                with col1:
                    chosen_item_id = st.selectbox("Menu Item", list(item_options.keys()), format_func=lambda x: item_options[x], key="pos_item")
                with col2:
                    qty = st.number_input("Quantity", min_value=1, value=1, step=1, key="pos_qty")
                    
                if st.button("Add to Cart", key="pos_add_cart"):
                    st.session_state.cart.append({"item_id": chosen_item_id, "quantity": qty})
                    st.success("Added item to cart!")
                    
                if st.session_state.cart:
                    st.subheader("Cart Items")
                    for cart_item in st.session_state.cart:
                        m_obj = menu.get_item(cart_item["item_id"])
                        name = m_obj.name if m_obj else cart_item["item_id"]
                        price = m_obj.price if m_obj else 5.00
                        st.write(f"- {name} x {cart_item['quantity']} (${price * cart_item['quantity']:.2f})")
                        
                    order_id_input = st.text_input("Unique Order ID (e.g., ORD001)", key="pos_order_id")
                    if st.button("Submit Order", key="pos_submit"):
                        if order_id_input:
                            success = orders.create_order(order_id_input, selected_table_id, st.session_state.cart)
                            if success:
                                st.success("Order created successfully!")
                                st.session_state.cart = []
                                st.rerun()
                            else:
                                st.error("Order ID already exists or failed.")
                        else:
                            st.error("Please provide a valid Order ID.")
                    
                    if st.button("Clear Cart", key="pos_clear"):
                        st.session_state.cart = []
                        st.rerun()
            else:
                st.warning("No menu items available. Add items in Menu Management first.")
        else:
            st.warning("No tables found. Add tables in Table Management first.")

    with tab_menu:
        st.title("Menu Management")
        
        st.subheader("Existing Menu Items")
        items = menu.get_all_items()
        if items:
            for item in items:
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                col1.write(f"**{item.name}**")
                col2.write(f"${item.price:.2f}")
                col3.write(f"Category: {item.category}")
                if col4.button("Delete", key=f"del_{item.item_id}"):
                    menu.delete_item(item.item_id)
                    st.success(f"Deleted {item.name}")
                    st.rerun()
        else:
            st.info("Menu is empty.")
            
        st.subheader("Add New Menu Item")
        with st.form("add_menu_form"):
            new_id = st.text_input("Item ID (e.g. M01)")
            new_name = st.text_input("Item Name")
            new_cat = st.text_input("Category")
            new_price = st.number_input("Price ($)", min_value=0.0, step=0.50)
            submit_menu = st.form_submit_button("Add Item")
            
            if submit_menu:
                if new_id and new_name and new_cat and new_price > 0:
                    res = menu.add_item(new_id, new_name, new_cat, new_price)
                    if res:
                        st.success(f"Successfully added {new_name}!")
                        st.rerun()
                    else:
                        st.error("Duplicate item ID or failed to add.")
                else:
                    st.error("Please fill out all fields correctly.")

    with tab_table:
        st.title("Table Management")
        
        st.subheader("All Tables")
        for t in tables.tables:
            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
            col1.write(f"**Table {t.table_id}**")
            col2.write(f"Capacity: {t.capacity}")
            col3.write(f"Occupied: {'Yes' if t.is_occupied else 'No'}")
            if t.is_occupied:
                if col4.button("Vacate", key=f"vac_{t.table_id}"):
                    tables.vacate_table(t.table_id)
                    st.rerun()
            else:
                if col4.button("Occupy", key=f"occ_{t.table_id}"):
                    tables.occupy_table(t.table_id, t.capacity)
                    st.rerun()
                    
        st.subheader("Add New Table")
        with st.form("add_table_form"):
            t_id = st.text_input("Table ID (e.g. T1)")
            t_cap = st.number_input("Capacity", min_value=1, step=1, value=4)
            sub_t = st.form_submit_button("Add Table")
            if sub_t:
                if t_id:
                    tables.add_table(t_id, t_cap)
                    st.success(f"Table {t_id} added!")
                    st.rerun()
                else:
                    st.error("Enter a valid table ID.")

    with tab_orders:
        st.title("Active Orders & Receipts")
        
        all_ords = orders.get_all_orders()
        if all_ords:
            for o in all_ords:
                st.write("---")
                st.write(f"**Order ID:** {o.order_id} | **Table ID:** {o.table_id} | **Status:** {getattr(o, 'status', 'Pending')}")
                st.write(f"**Total:** ${o.total_price:.2f}")
                
                new_st = st.selectbox("Update Status", ["Pending", "Preparing", "Completed", "Cancelled"], key=f"status_{o.order_id}")
                if st.button("Save Status", key=f"save_status_{o.order_id}"):
                    orders.update_order_status(o.order_id, new_st)
                    st.success("Status updated!")
                    st.rerun()
                    
            st.subheader("Generate Bill / Receipt")
            receipt_table_id = st.text_input("Enter Table ID for Receipt", key="rcpt_table")
            discount = st.number_input("Discount Percentage (%)", min_value=0.0, max_value=100.0, step=1.0, value=0.0, key="rcpt_disc")

            col_gen, col_pay = st.columns(2)
            
            with col_gen:
                if st.button("Generate Receipt Printout", key="btn_gen_receipt"):
                    if receipt_table_id:
                        table_orders = orders.get_orders_by_table(receipt_table_id)
                        if table_orders:
                            raw_sub = 0.0
                            receipt_rows = []
                            for ord_item in table_orders:
                                for itm in ord_item.items:
                                    q = itm["quantity"]
                                    iid = itm["item_id"]
                                    m_obj = menu.get_item(iid)
                                    name = m_obj.name if m_obj else iid
                                    price = m_obj.price if m_obj else itm.get("price", 5.00)
                                    sub = price * q
                                    raw_sub += sub
                                    
                                    receipt_rows.append({
                                        "Item": name,
                                        "Qty": str(q),
                                        "Price": f"${price:.2f}",
                                        "Subtotal": f"${sub:.2f}"
                                    })
                            
                            disc_amt = raw_sub * (discount / 100.0)
                            taxable = raw_sub - disc_amt
                            tax = taxable * 0.05
                            grand = taxable + tax
                            
                            st.markdown("---")
                            st.markdown(f"### 🧾 RECEIPT: TABLE {receipt_table_id}")
                            st.table(pd.DataFrame(receipt_rows))
                            
                            st.markdown(f"""
                            **Subtotal:** ${raw_sub:.2f}  
                            {f'**Discount ({discount}%):** -${disc_amt:.2f}' if discount > 0 else ''}
                            **Tax (5%):** +${tax:.2f}  
                            ___
                            ### **GRAND TOTAL: ${grand:.2f}**
                            """)
                        else:
                            st.warning(f"No active orders found for Table {receipt_table_id}.")
                            
            with col_pay:
                if st.button("Finished Paying (Clear Orders & Vacate Table)", type="primary", key="btn_finish_pay"):
                    if receipt_table_id:
                        cleared = orders.delete_orders_by_table(receipt_table_id)
                        tables.vacate_table(receipt_table_id)
                        
                        if cleared:
                            st.success(f"Table {receipt_table_id} checked out successfully! Orders cleared and table vacated.")
                            st.rerun()
                        else:
                            st.warning(f"No active orders found to clear for Table {receipt_table_id}.")
                    else:
                        st.error("Please enter a valid Table ID.")

            if st.button("Generate Receipt Printout"):
                if receipt_table_id:
                    table_orders = orders.get_orders_by_table(receipt_table_id)
                    if table_orders:
                        raw_sub = 0.0
                        receipt_rows = []
                        for ord_item in table_orders:
                            for itm in ord_item.items:
                                q = itm["quantity"]
                                iid = itm["item_id"]
                                m_obj = menu.get_item(iid)
                                name = m_obj.name if m_obj else iid
                                price = m_obj.price if m_obj else itm.get("price", 5.00)
                                sub = price * q
                                raw_sub += sub
                                
                                receipt_rows.append({
                                    "Item": name,
                                    "Qty": str(q),
                                    "Price": f"${price:.2f}",
                                    "Subtotal": f"${sub:.2f}"
                                })
                        
                        disc_amt = raw_sub * (discount / 100.0)
                        taxable = raw_sub - disc_amt
                        tax = taxable * 0.05
                        grand = taxable + tax
                        
                        st.markdown("---")
                        st.markdown(f"### 🧾 RECEIPT: TABLE {receipt_table_id}")
                        st.table(pd.DataFrame(receipt_rows))
                        
                        st.markdown(f"""
                        **Subtotal:** ${raw_sub:.2f}  
                        {f'**Discount ({discount}%):** -${disc_amt:.2f}' if discount > 0 else ''}
                        **Tax (5%):** +${tax:.2f}  
                        ___
                        ### **GRAND TOTAL: ${grand:.2f}**
                        """)
                    else:
                        st.warning(f"No active orders found for Table {receipt_table_id}.")
        else:
            st.info("No orders placed yet.")