import streamlit as st
from Services.auth_service import AuthService
from Services.menu_service import MenuService
from Services.table_service import TableService
from Services.order_service import OrderService
import pandas as pd
import streamlit.components.v1 as components

# MUST be the very first Streamlit command
st.set_page_config(page_title="Restaurant Management System", layout="wide")

TAX_RATE = 0.05


def build_receipt(table_orders, menu_service, discount_percent):
    """
    Builds the itemized rows and totals for a receipt. Pulled out into one
    shared function so the POS/Orders tab has exactly one place that
    calculates a bill, instead of the same math being duplicated (and
    liable to drift out of sync) in multiple button handlers.
    """
    raw_subtotal = 0.0
    receipt_rows = []

    for order_item in table_orders:
        for line in order_item.items:
            quantity = line["quantity"]
            item_id = line["item_id"]
            menu_item = menu_service.get_item(item_id)
            name = menu_item.name if menu_item else item_id
            price = menu_item.price if menu_item else line.get("price", 5.00)
            line_subtotal = price * quantity
            raw_subtotal += line_subtotal

            receipt_rows.append({
                "Item": name,
                "Qty": str(quantity),
                "Price": f"${price:.2f}",
                "Subtotal": f"${line_subtotal:.2f}",
            })

    discount_amount = raw_subtotal * (discount_percent / 100.0)
    taxable_amount = raw_subtotal - discount_amount
    tax = taxable_amount * TAX_RATE
    grand_total = taxable_amount + tax

    return receipt_rows, raw_subtotal, discount_amount, tax, grand_total

# The theme toggle was removed — the light palette consistently looked the
# most polished, so the app now always uses it rather than maintaining a
# second (less refined) dark variant.
C = {
    "bg": "#F6F7FA", "sidebar_bg": "#FFFFFF", "sidebar_card": "#F3F4F6",
    "sidebar_text": "#1B212C", "sidebar_muted": "#6B7280", "sidebar_border": "rgba(27, 33, 44, 0.10)",
    "card": "#FFFFFF", "ink": "#1B212C", "muted": "#6B7280",
    "border": "rgba(27, 33, 44, 0.09)", "input_bg": "#FFFFFF",
    "hover_shadow": "rgba(27, 33, 44, 0.10)",
}

# Fixed accent palette (same in both themes, so status colors stay recognizable)
PRIMARY = "#0F766E"
PRIMARY_DARK = "#0B5C56"
PRIMARY_LIGHT = "#14B8A6"
AMBER = "#D97706"
RED = "#DC2626"
GREEN = "#16A34A"
BLUE = "#2563EB"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    .stApp {{
        background-color: {C['bg']} !important;
        color: {C['ink']} !important;
    }}
    header[data-testid="stHeader"] {{
        background-color: {C['bg']} !important;
    }}
    div[data-testid="stDecoration"] {{
        background-color: {C['bg']} !important;
        background-image: none !important;
    }}
    section[data-testid="stSidebar"] {{
        background-color: {C['sidebar_bg']} !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: {C['sidebar_text']} !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: {C['ink']} !important;
        font-weight: 700 !important;
    }}
    p, span, label, .stMarkdown, .stCaption {{
        color: {C['ink']};
    }}

    /* ---------- Cards ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {C['card']} !important;
        border: 1px solid {C['border']} !important;
        border-radius: 14px !important;
        padding: 6px;
        transition: box-shadow 0.18s ease, transform 0.18s ease;
    }}
    div[data-testid="stForm"] {{
        background-color: {C['card']} !important;
        border: 1px solid {C['border']} !important;
        border-radius: 14px !important;
    }}
    .app-card {{
        background-color: {C['card']};
        border: 1px solid {C['border']};
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 14px;
        transition: box-shadow 0.18s ease, transform 0.18s ease;
    }}
    .app-card:hover {{
        transform: translateY(-1px);
        box-shadow: 0 8px 20px {C['hover_shadow']};
    }}

    /* ---------- Buttons ---------- */
    div.stButton > button, div[data-testid="stFormSubmitButton"] > button {{
        background-color: {PRIMARY};
        color: #FFFFFF !important;
        border: none;
        border-radius: 9px;
        font-weight: 600;
        padding: 0.5rem 1.1rem;
        transition: background-color 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
    }}
    div.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {{
        background-color: {PRIMARY_DARK};
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(15, 118, 110, 0.35);
    }}
    div.stButton > button p, div[data-testid="stFormSubmitButton"] > button p {{
        color: #FFFFFF !important;
    }}

    /* ---------- Tabs (pill style) ---------- */
    [data-testid="stTabs"] [role="tablist"], [data-baseweb="tab-list"] {{
        gap: 4px !important;
        background-color: {C['border']} !important;
        border-bottom: none !important;
        border-radius: 999px !important;
        padding: 5px !important;
        display: inline-flex !important;
    }}
    [data-testid="stTabs"] [role="tab"], [data-baseweb="tab"] {{
        font-weight: 600 !important;
        color: {C['muted']} !important;
        background-color: transparent !important;
        border-radius: 999px !important;
        padding: 8px 18px !important;
        transition: background-color 0.18s ease, color 0.18s ease !important;
    }}
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
        color: #FFFFFF !important;
        background-color: {PRIMARY} !important;
    }}
    [data-testid="stTabs"] [role="tab"] p {{ color: inherit !important; }}
    [data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {{
        display: none !important;
    }}

    /* ---------- Inputs ---------- */
    input, textarea, .stNumberInput input {{
        background-color: {C['input_bg']} !important;
        color: {C['ink']} !important;
        border-color: {C['border']} !important;
        border-radius: 8px !important;
    }}
    div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {{
        background-color: {C['input_bg']} !important;
        color: {C['ink']} !important;
        border-radius: 8px !important;
    }}
    div[data-baseweb="select"]:focus-within > div, input:focus {{
        border-color: {PRIMARY} !important;
        box-shadow: 0 0 0 1px {PRIMARY} !important;
    }}

    /* ---------- Status badges ---------- */
    .status-badge {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 12.5px;
        font-weight: 700;
        letter-spacing: 0.2px;
    }}
    .cat-badge {{
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        background-color: {C['border']};
        color: {C['muted']};
    }}
    .table-dot {{
        display: inline-block;
        width: 9px; height: 9px;
        border-radius: 50%;
        margin-right: 7px;
    }}
    </style>
""", unsafe_allow_html=True)


def status_badge(status):
    """Returns a colored pill badge (as HTML) for an order status."""
    colors = {
        "Pending": (AMBER, "#FFF7ED"),
        "Preparing": (BLUE, "#EFF6FF"),
        "Ready": (PRIMARY, "#F0FDFA"),
        "Completed": (GREEN, "#F0FDF4"),
        "Cancelled": (RED, "#FEF2F2"),
    }
    fg, bg = colors.get(status, (PRIMARY, "#F0FDFA"))
    return f'<span class="status-badge" style="color:{fg}; background-color:{bg};">{status}</span>'


def category_badge(category):
    return f'<span class="cat-badge">{category}</span>'


# Live Ticking Digital Clock in the Sidebar
st.sidebar.markdown("### 🕒 Live System Time")

clock_html = f"""
<div style="background-color: {C['sidebar_card']}; padding: 12px; border-radius: 10px; text-align: center; border: 1px solid {C['sidebar_border']}; border-top: 2px solid {PRIMARY_LIGHT}; font-family: 'Plus Jakarta Sans', sans-serif;">
    <div id="live-clock" style="font-size: 0.95rem; font-weight: 700; color: {C['sidebar_text']};">Loading...</div>
</div>
<script>
function updateClock() {{
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    const dateString = now.toLocaleDateString(undefined, {{ weekday: 'short', month: 'short', day: 'numeric' }});
    document.getElementById('live-clock').innerHTML = dateString + '<br>' + timeString;
}}
setInterval(updateClock, 1000);
updateClock();
</script>
"""
# NOTE: components.html() must be called *inside* a `with st.sidebar:` block
# to actually render in the sidebar — calling it directly (as the original
# code did) silently renders it at the top of the main page instead, which
# is why the clock used to show up floating above the login card.
with st.sidebar:
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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

# Authentication View
if not auth.current_user:
    # Center the login box using columns
    _, center_col, _ = st.columns([1, 1.2, 1])
    
    with center_col:
        st.markdown(f"""
            <div style="text-align:center; margin: 32px 0 24px 0;">
                <div style="
                    width: 56px; height: 56px; margin: 0 auto 14px auto;
                    background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_LIGHT});
                    border-radius: 16px; display: flex; align-items: center; justify-content: center;
                    font-size: 26px; box-shadow: 0 8px 20px rgba(15,118,110,0.3);">
                    🍽️
                </div>
                <h2 style="margin:0; font-weight:800;">Restaurant Management</h2>
                <p style="color:{C['muted']}; margin-top:4px;">Sign in to manage orders, tables, and the menu</p>
            </div>
        """, unsafe_allow_html=True)
        
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
                        # Set native session state variables
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.role = auth.get_current_role()
                        
                        if hasattr(auth, 'update_user_status'):
                            auth.update_user_status(username, "Online")
                            
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
                st.caption("New accounts are created as Staff. An existing admin can promote a user to Admin later.")

                if st.button("Register Account", use_container_width=True):
                    # SECURITY: role is intentionally NOT selectable here — public
                    # self-registration must never be able to grant admin access.
                    # New accounts always start as "staff".
                    if auth.register_user(reg_id, reg_user, reg_pass, role="staff"):
                        st.success("Registered successfully! Please log in.")
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error("Registration failed. Check that the ID/username are unique and the password is at least 4 characters.")
                
                # Back to login link on the bottom right
                col_spacer, col_btn = st.columns([1.5, 1])
                with col_btn:
                    if st.button("back to login", key="switch_to_login"):
                        st.session_state.show_register = False
                        st.rerun()
else:
    role_color = PRIMARY_LIGHT if st.session_state.role == "admin" else BLUE
    st.sidebar.markdown(f"""
        <div style="background-color:{C['sidebar_card']}; border:1px solid {C['sidebar_border']};
                    border-radius:10px; padding:12px 14px; margin-bottom:12px;">
            <div style="font-size:13px; color:{C['sidebar_muted']};">Signed in as</div>
            <div style="font-weight:700; font-size:15px; color:{C['sidebar_text']};">{st.session_state.username}</div>
            <span class="status-badge" style="color:{role_color}; background-color:rgba(20,184,166,0.12); margin-top:4px;">{st.session_state.role.upper()}</span>
        </div>
    """, unsafe_allow_html=True)
    if st.sidebar.button("Logout", use_container_width=True):
        if hasattr(auth, 'update_user_status'):
            auth.update_user_status(st.session_state.username, "Offline")
        auth.logout()
        
        # Clear session state on logout
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()

    # Admin User Status Monitor Dashboard
    if st.session_state.role == "admin" and hasattr(auth, 'get_all_users'):
        st.sidebar.markdown("---")
        st.sidebar.subheader("👥 User Status Monitor")
        all_users = auth.get_all_users()
        for u in all_users:
            uname = u.get("username")
            urole = u.get("role")
            ustatus = u.get("status", "Offline")
            dot_color = GREEN if ustatus == "Online" else "#9CA3AF"
            weight = "700" if ustatus == "Online" else "400"
            opacity = "1" if ustatus == "Online" else "0.65"
            st.sidebar.markdown(
                f'<div style="padding:4px 0; opacity:{opacity};">'
                f'<span class="table-dot" style="background-color:{dot_color};"></span>'
                f'<span style="font-weight:{weight}; color:{C["sidebar_text"]};">{uname}</span> '
                f'<span style="color:{C["sidebar_muted"]}; font-size:12px;">({urole})</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            # Promote/demote — not offered for your own account, since
            # changing your own role mid-session is more confusing than useful.
            if uname != st.session_state.username:
                if urole == "staff":
                    if st.sidebar.button(f"⬆️ Promote to Admin", key=f"promote_{uname}", use_container_width=True):
                        ok, msg = auth.set_user_role(uname, "admin")
                        (st.sidebar.success if ok else st.sidebar.error)(msg)
                        if ok:
                            st.rerun()
                elif urole == "admin":
                    if st.sidebar.button(f"⬇️ Demote to Staff", key=f"demote_{uname}", use_container_width=True):
                        ok, msg = auth.set_user_role(uname, "staff")
                        (st.sidebar.success if ok else st.sidebar.error)(msg)
                        if ok:
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

        st.markdown(f"""
        <div style="background: linear-gradient(120deg, {PRIMARY}, {PRIMARY_LIGHT}); padding: 22px 26px; border-radius: 14px; color: white; margin-bottom: 22px; box-shadow: 0 8px 24px rgba(15,118,110,0.25);">
            <div style="font-size:12px; font-weight:700; letter-spacing:0.5px; opacity:0.85; margin-bottom:4px;">TODAY'S PROMOTION</div>
            <h2 style="margin:0 0 6px 0; color:white;">50% OFF All Burgers & Combo Sets</h2>
            <p style="margin:0; opacity:0.92;">This weekend only — free delivery on orders over $20.</p>
        </div>
        """, unsafe_allow_html=True)

        if "selected_cat" not in st.session_state:
            st.session_state.selected_cat = "All"
            
        st.subheader("What's on Your Mind?")
        
        categories = {
            "All": "🌐 All",
            "Drinks": "🍹 Drinks",
            "Food": "🍔 Food",
            "Dessert": "🍰 Dessert",
            "Noodles": "🍜 Noodles"
        }
        
        cat_cols = st.columns(len(categories))

        for i, (cat_key, cat_label) in enumerate(categories.items()):
            with cat_cols[i]:
                if st.button(cat_label, use_container_width=True, key=f"pos_filter_cat_{cat_key}"):
                    st.session_state.selected_cat = cat_key
                    st.rerun()
                    
        st.markdown(
            f'<div style="margin-bottom:14px;">Filtering by: {category_badge(st.session_state.selected_cat)}</div>',
            unsafe_allow_html=True,
        )
        
        avail_tables = tables.tables
        table_options = {t.table_id: f"Table {t.table_id} (Capacity: {t.capacity}, Occupied: {t.is_occupied})" for t in avail_tables}
        
        if table_options:
            selected_table_id = st.selectbox("Select Table", list(table_options.keys()), format_func=lambda x: table_options[x], key="pos_table")
            
            st.subheader("Add Items to Order")
            
            # 1. Search text input bar
            search_query = st.text_input("🔍 Search Menu Items", "", key="pos_search_query")
            
            all_menu_items = menu.get_all_items()
            current_cat = st.session_state.get("selected_cat", "All")
            
            # 2. Filter by category buttons
            if current_cat == "All":
                items = all_menu_items
            else:
                # Category names are now stored consistently (see Data/menu.json),
                # so a direct case-insensitive match is enough — no more fragile
                # substring/pluralization guessing needed here.
                items = [
                    item for item in all_menu_items
                    if getattr(item, 'category', '').strip().lower() == current_cat.lower()
                ]

            # 3. Filter further if a search term is typed
            if search_query:
                items = [item for item in items if search_query.lower() in item.name.lower()]

            if not items:
                st.warning("No menu items found matching your search or filter.")
            else:
                item_options = {item.item_id: f"{item.name} - ${item.price:.2f} ({item.category})" for item in items}
                
                if "cart" not in st.session_state:
                    st.session_state.cart = []
                    
                col1, col2 = st.columns(2)
                with col1:
                    chosen_item_id = st.selectbox("Menu Item", list(item_options.keys()), format_func=lambda x: item_options[x], key=f"pos_item_{current_cat}_{search_query}")
                with col2:
                    qty = st.number_input("Quantity", min_value=1, value=1, step=1, key=f"pos_qty_{current_cat}_{search_query}")
                
                if st.button("Add to Cart", key="pos_add_cart"):
                    st.session_state.cart.append({"item_id": chosen_item_id, "quantity": qty})
                    st.success("Added item to cart!")
                    st.rerun()
                    
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
            st.warning("No tables found. Add tables in Table Management first.")

    with tab_menu:
        st.title("Menu Management")

        is_admin = st.session_state.get("role") == "admin"

        # Display the menu items for everyone to view
        st.subheader("Current Menu Items")
        items = menu.get_all_items()  # Assuming 'menu' is your MenuService instance

        if items:
            for item in items:
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                col1.write(f"**{item.name}**")
                col2.write(f"${item.price:.2f}")
                col3.markdown(category_badge(item.category), unsafe_allow_html=True)
                
                # Only render the delete button if the user is an admin
                if is_admin:
                    if col4.button("Delete", key=f"del_{item.item_id}"):
                        menu.delete_item(item.item_id)
                        st.success(f"Deleted {item.name}")
                        st.rerun()
        else:
            st.info("Menu is empty.")

        # Admin-only section for adding new items
        if is_admin:
            st.markdown("---")
            st.subheader("🛠️ Add New Menu Item")
            with st.form("add_menu_form"):
                new_id = st.text_input("Item ID (e.g. M01)")
                new_name = st.text_input("Item Name")
                # A fixed dropdown (matching the filter categories above) instead
                # of free text — free text let inconsistent category names like
                # "Drink" vs "Drinks" or trailing spaces creep into the data,
                # which silently broke category filtering for those items.
                new_cat = st.selectbox("Category", ["Food", "Drinks", "Dessert", "Noodles"])
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
        else:
            st.markdown("---")
            st.info("🔒 Note: Adding and deleting menu items is restricted to administrators. You are viewing the menu in read-only mode.")

    with tab_table:
        st.title("Table Management")
        
        st.subheader("All Tables")
        for t in tables.tables:
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
            col1.write(f"**Table {t.table_id}**")
            col2.write(f"Capacity: {t.capacity}")
            dot_color = RED if t.is_occupied else GREEN
            status_label = "Occupied" if t.is_occupied else "Vacant"
            col3.markdown(
                f'<span class="table-dot" style="background-color:{dot_color};"></span>{status_label}',
                unsafe_allow_html=True,
            )
            if t.is_occupied:
                col4.write("")
                if col5.button("Vacate", key=f"vac_{t.table_id}"):
                    tables.vacate_table(t.table_id)
                    st.rerun()
            else:
                # Ask for the actual party size instead of assuming the table
                # is always filled to full capacity — this is also what lets
                # TableService's over-capacity check actually do anything.
                party_size = col4.number_input(
                    "Party size", min_value=1, max_value=t.capacity, value=min(2, t.capacity),
                    step=1, key=f"party_{t.table_id}", label_visibility="collapsed"
                )
                if col5.button("Occupy", key=f"occ_{t.table_id}"):
                    tables.occupy_table(t.table_id, party_size)
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
        
        st.subheader("Live Order Tracking")
        all_orders = orders.get_all_orders()
        
        # Filter for active orders that aren't completed or cancelled
        active_orders = [o for o in all_orders if getattr(o, 'status', 'Pending') not in ["Completed", "Cancelled"]]

        if not active_orders:
            st.info("No active orders right now.")
        else:
            for o in active_orders:
                status = getattr(o, 'status', 'Pending')
                with st.expander(f"Order #{o.order_id} — Table {o.table_id}"):
                    st.markdown(status_badge(status), unsafe_allow_html=True)
                    steps = ["Pending", "Preparing", "Ready", "Completed"]
                    current_index = steps.index(status) if status in steps else 0
                    
                    st.progress((current_index + 1) / len(steps))
                    
                    if st.button("Advance Status", key=f"adv_{o.order_id}"):
                        next_status = steps[current_index + 1] if current_index < len(steps) - 1 else "Completed"
                        orders.update_order_status(o.order_id, next_status)
                        st.rerun()

        st.markdown("---")
        st.subheader("All Order History & Status Updates")
        
        if all_orders:
            for o in all_orders:
                st.markdown("---")
                st.markdown(
                    f"**Order ID:** {o.order_id} &nbsp;|&nbsp; **Table:** {o.table_id} &nbsp;|&nbsp; "
                    f"{status_badge(getattr(o, 'status', 'Pending'))}",
                    unsafe_allow_html=True,
                )
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
                            receipt_rows, raw_sub, disc_amt, tax, grand = build_receipt(table_orders, menu, discount)

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
        else:
            st.info("No orders placed yet.")