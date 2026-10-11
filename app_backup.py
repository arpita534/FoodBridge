import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# ============================================================
# FOODBRIDGE - COMPLETE STREAMLIT MVP
# "From Surplus to Need, Before It's Too Late."
# ============================================================

st.set_page_config(
    page_title="FoodBridge | Surplus to Need",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# GLOBAL CSS
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f7fff8 0%, #eefbf2 45%, #f7fbff 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #073b2a 0%, #0b5d43 100%);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero {
        padding: 28px 32px;
        border-radius: 24px;
        background: linear-gradient(135deg, #073b2a, #11945f);
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.10);
    }

    .hero h1 {
        font-size: 42px;
        margin: 0;
        font-weight: 800;
    }

    .hero p {
        font-size: 17px;
        margin-top: 8px;
        opacity: 0.95;
    }

    .card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #dcefe3;
        box-shadow: 0 5px 18px rgba(0,0,0,0.06);
        margin-bottom: 15px;
    }

    .feature {
        background: white;
        padding: 22px;
        border-radius: 18px;
        border-top: 5px solid #18a66a;
        box-shadow: 0 5px 18px rgba(0,0,0,0.06);
        height: 100%;
    }

    .feature h3 {
        margin-top: 5px;
        color: #073b2a;
    }

    .stat {
        background: white;
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        border: 1px solid #dcefe3;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }

    .stat-number {
        font-size: 30px;
        font-weight: 800;
        color: #0b8f58;
    }

    .stat-label {
        color: #5d6b65;
        font-size: 14px;
    }

    .badge {
        display: inline-block;
        padding: 5px 11px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        margin: 3px;
    }

    .verified {
        background: #dff8ea;
        color: #08753f;
    }

    .pending {
        background: #fff3cd;
        color: #8a6500;
    }

    .danger {
        background: #ffe3e3;
        color: #a51f1f;
    }

    .info {
        background: #e3f2ff;
        color: #145a92;
    }

    .flow-box {
        background: white;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        border: 1px solid #dcefe3;
        min-height: 120px;
    }

    .flow-arrow {
        text-align: center;
        font-size: 30px;
        padding-top: 35px;
        color: #0b8f58;
    }

    .small-muted {
        color: #68756f;
        font-size: 13px;
    }

    div[data-testid="stMetric"] {
        background: white;
        padding: 12px;
        border-radius: 16px;
        border: 1px solid #dcefe3;
    }

    .footer {
        text-align: center;
        padding: 25px;
        color: #66736d;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

def initialize_state():
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "role" not in st.session_state:
        st.session_state.role = ""

    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

    if "notifications" not in st.session_state:
        st.session_state.notifications = []

    if "donations" not in st.session_state:
        st.session_state.donations = [
            {
                "id": "FB001",
                "donor": "Royal Celebration Hall",
                "food_type": "Cooked Meals",
                "category": "Meals",
                "quantity": 120,
                "prep_time": "Today, 6:00 PM",
                "pickup": "Sector 62, Noida",
                "deadline": "Today, 10:00 PM",
                "storage": "Covered containers",
                "status": "Available",
                "verified": True,
                "claimed_by": "",
                "claim_status": "",
                "created": datetime.now()
            },
            {
                "id": "FB002",
                "donor": "Green Leaf Restaurant",
                "food_type": "Rice & Dal",
                "category": "Meals",
                "quantity": 80,
                "prep_time": "Today, 4:30 PM",
                "pickup": "Greater Noida West",
                "deadline": "Today, 9:00 PM",
                "storage": "Refrigerated",
                "status": "Available",
                "verified": True,
                "claimed_by": "",
                "claim_status": "",
                "created": datetime.now()
            },
            {
                "id": "FB003",
                "donor": "Apex Corporate Event",
                "food_type": "Vegetable Biryani",
                "category": "Rice",
                "quantity": 65,
                "prep_time": "Today, 5:00 PM",
                "pickup": "Knowledge Park III",
                "deadline": "Today, 11:00 PM",
                "storage": "Insulated containers",
                "status": "Available",
                "verified": True,
                "claimed_by": "",
                "claim_status": "",
                "created": datetime.now()
            },
            {
                "id": "FB004",
                "donor": "Sunrise Banquet",
                "food_type": "Roti & Paneer",
                "category": "Meals",
                "quantity": 100,
                "prep_time": "Tomorrow, 1:00 PM",
                "pickup": "Indirapuram",
                "deadline": "Tomorrow, 5:00 PM",
                "storage": "Covered containers",
                "status": "Available",
                "verified": False,
                "claimed_by": "",
                "claim_status": "",
                "created": datetime.now()
            }
        ]

    if "users" not in st.session_state:
        st.session_state.users = [
            {
                "name": "Demo Donor",
                "email": "donor@foodbridge.demo",
                "password": "1234",
                "role": "Donor"
            },
            {
                "name": "Demo NGO",
                "email": "ngo@foodbridge.demo",
                "password": "1234",
                "role": "NGO"
            },
            {
                "name": "Admin",
                "email": "admin@foodbridge.demo",
                "password": "admin123",
                "role": "Admin"
            }
        ]

    if "activity" not in st.session_state:
        st.session_state.activity = [
            {
                "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                "message": "FoodBridge demo platform initialized",
                "type": "system"
            }
        ]


initialize_state()


# ============================================================
# HELPERS
# ============================================================

def add_activity(message, activity_type="info"):
    st.session_state.activity.insert(
        0,
        {
            "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
            "message": message,
            "type": activity_type
        }
    )


def add_notification(message):
    st.session_state.notifications.insert(0, message)


def logout():
    st.session_state.logged_in = False
    st.session_state.role = ""
    st.session_state.user_name = ""
    st.session_state.page = "Home"


def get_available_donations():
    return [
        d for d in st.session_state.donations
        if d["status"] == "Available" and d["verified"]
    ]


def get_claimed_donations_for_user():
    name = st.session_state.user_name
    return [
        d for d in st.session_state.donations
        if d.get("claimed_by") == name
    ]


def estimated_meals():
    completed = [
        d for d in st.session_state.donations
        if d["status"] == "Completed"
    ]
    return sum(d["quantity"] for d in completed)


def rescued_quantity():
    return sum(
        d["quantity"]
        for d in st.session_state.donations
        if d["status"] in ["Accepted", "Picked Up", "Completed"]
    )


def page_title(title, subtitle=""):
    st.markdown(f"""
    <div style="margin-bottom:20px;">
        <h1 style="color:#073b2a; margin-bottom:3px;">{title}</h1>
        <p class="small-muted">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 🍲 FoodBridge")
    st.caption("From Surplus to Need, Before It's Too Late.")

    st.divider()

    if not st.session_state.logged_in:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "Home"

        if st.button("🔐 Login", use_container_width=True):
            st.session_state.page = "Login"

        if st.button("📝 Sign Up", use_container_width=True):
            st.session_state.page = "Signup"

    else:
        st.success(f"Logged in as\n{st.session_state.user_name}")
        st.caption(st.session_state.role)

        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.page = "Dashboard"

        if st.session_state.role == "Donor":
            if st.button("🍱 Donate Food", use_container_width=True):
                st.session_state.page = "Donate"

            if st.button("📦 My Donations", use_container_width=True):
                st.session_state.page = "My Donations"

        elif st.session_state.role == "NGO":
            if st.button("🔎 Find Food", use_container_width=True):
                st.session_state.page = "Find Food"

            if st.button("📍 My Claims", use_container_width=True):
                st.session_state.page = "My Claims"

        elif st.session_state.role == "Admin":
            if st.button("🛡️ Verification", use_container_width=True):
                st.session_state.page = "Verification"

            if st.button("📊 Admin Dashboard", use_container_width=True):
                st.session_state.page = "Admin Dashboard"

        if st.button("📈 Impact Dashboard", use_container_width=True):
            st.session_state.page = "Impact"

        if st.button("🔔 Alerts", use_container_width=True):
            st.session_state.page = "Alerts"

        st.divider()

        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()


# ============================================================
# HOME
# ============================================================

if st.session_state.page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>🍲 FoodBridge</h1>
        <p>From Surplus to Need, Before It's Too Late.</p>
        <p style="font-size:14px;">
            A digital bridge connecting surplus food from events,
            restaurants and gatherings with verified NGOs and communities.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="feature">
            <div style="font-size:35px;">🍽️</div>
            <h3>Donate Surplus</h3>
            <p>List safe surplus food before it goes to waste.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature">
            <div style="font-size:35px;">🤝</div>
            <h3>Connect NGOs</h3>
            <p>Verified NGOs can discover and request available food.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature">
            <div style="font-size:35px;">📍</div>
            <h3>Track Pickup</h3>
            <p>Track accepted donations from request to completion.</p>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="feature">
            <div style="font-size:35px;">📊</div>
            <h3>Measure Impact</h3>
            <p>See rescued food, completed donations and meals served.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("How FoodBridge Works")

    f1, a1, f2, a2, f3, a3, f4 = st.columns([2, .5, 2, .5, 2, .5, 2])

    with f1:
        st.markdown("""
        <div class="flow-box">
            <h2>1️⃣</h2>
            <b>Donor Lists Food</b><br>
            <span class="small-muted">Quantity + deadline + pickup</span>
        </div>
        """, unsafe_allow_html=True)

    with a1:
        st.markdown("<div class='flow-arrow'>→</div>", unsafe_allow_html=True)

    with f2:
        st.markdown("""
        <div class="flow-box">
            <h2>2️⃣</h2>
            <b>Food Verified</b><br>
            <span class="small-muted">Admin checks listing</span>
        </div>
        """, unsafe_allow_html=True)

    with a2:
        st.markdown("<div class='flow-arrow'>→</div>", unsafe_allow_html=True)

    with f3:
        st.markdown("""
        <div class="flow-box">
            <h2>3️⃣</h2>
            <b>NGO Claims</b><br>
            <span class="small-muted">NGO requests the food</span>
        </div>
        """, unsafe_allow_html=True)

    with a3:
        st.markdown("<div class='flow-arrow'>→</div>", unsafe_allow_html=True)

    with f4:
        st.markdown("""
        <div class="flow-box">
            <h2>4️⃣</h2>
            <b>Pickup & Impact</b><br>
            <span class="small-muted">Track + complete + measure</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Live Demo Statistics")

    total_listed = len(st.session_state.donations)
    available = len(get_available_donations())
    claimed = len([
        d for d in st.session_state.donations
        if d["status"] in ["Accepted", "Picked Up", "Completed"]
    ])
    completed = len([
        d for d in st.session_state.donations
        if d["status"] == "Completed"
    ])

    s1, s2, s3, s4 = st.columns(4)

    for col, number, label in [
        (s1, total_listed, "Food Listings"),
        (s2, available, "Available"),
        (s3, claimed, "In Progress"),
        (s4, completed, "Completed")
    ]:
        with col:
            st.markdown(f"""
            <div class="stat">
                <div class="stat-number">{number}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    b1, b2 = st.columns(2)

    with b1:
        if st.button("🚀 Start as Donor", use_container_width=True, type="primary"):
            st.session_state.page = "Signup"
            st.rerun()

    with b2:
        if st.button("🤝 Start as NGO", use_container_width=True):
            st.session_state.page = "Signup"
            st.rerun()


# ============================================================
# LOGIN
# ============================================================

elif st.session_state.page == "Login":

    page_title("🔐 Login", "Access the FoodBridge platform.")

    left, center, right = st.columns([1, 2, 1])

    with center:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True,
                type="primary"
            )

            if submitted:
                user = next(
                    (
                        u for u in st.session_state.users
                        if u["email"].lower() == email.lower()
                        and u["password"] == password
                    ),
                    None
                )

                if user:
                    st.session_state.logged_in = True
                    st.session_state.role = user["role"]
                    st.session_state.user_name = user["name"]
                    st.session_state.page = "Dashboard"
                    add_notification("Welcome back to FoodBridge!")
                    st.success("Login successful.")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

        st.info("""
        **Demo Accounts**

        Donor: `donor@foodbridge.demo` / `1234`

        NGO: `ngo@foodbridge.demo` / `1234`

        Admin: `admin@foodbridge.demo` / `admin123`
        """)


# ============================================================
# SIGNUP
# ============================================================

elif st.session_state.page == "Signup":

    page_title("📝 Create Account", "Join FoodBridge as a donor or NGO.")

    left, center, right = st.columns([1, 2, 1])

    with center:
        with st.form("signup_form"):

            name = st.text_input("Full Name / Organization Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")

            role = st.selectbox(
                "Account Type",
                ["Donor", "NGO"]
            )

            phone = st.text_input("Phone Number")
            location = st.text_input("Primary Location")

            submitted = st.form_submit_button(
                "Create Account",
                use_container_width=True,
                type="primary"
            )

            if submitted:
                if not name or not email or not password:
                    st.error("Please fill all required fields.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                elif any(u["email"].lower() == email.lower()
                         for u in st.session_state.users):
                    st.error("An account with this email already exists.")
                else:
                    st.session_state.users.append({
                        "name": name,
                        "email": email,
                        "password": password,
                        "role": role,
                        "phone": phone,
                        "location": location
                    })

                    add_activity(
                        f"New {role} account created: {name}",
                        "signup"
                    )

                    st.success("Account created successfully!")
                    st.info("Please go to Login to access your account.")


# ============================================================
# DASHBOARD
# ============================================================

elif st.session_state.page == "Dashboard":

    page_title(
        f"👋 Welcome, {st.session_state.user_name}",
        f"{st.session_state.role} Dashboard"
    )

    if st.session_state.role == "Donor":

        my_donations = [
            d for d in st.session_state.donations
            if d["donor"] == st.session_state.user_name
        ]

        if not my_donations:
            my_donations = [
                d for d in st.session_state.donations
                if d["donor"] == "Demo Donor"
            ]

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Listings", len(my_donations))

        with c2:
            st.metric(
                "Available",
                len([d for d in my_donations if d["status"] == "Available"])
            )

        with c3:
            st.metric(
                "Accepted",
                len([d for d in my_donations if d["status"] == "Accepted"])
            )

        with c4:
            st.metric(
                "Completed",
                len([d for d in my_donations if d["status"] == "Completed"])
            )

        st.markdown("### Recent Donations")

        if my_donations:
            df = pd.DataFrame(my_donations)
            st.dataframe(
                df[
                    [
                        "id",
                        "food_type",
                        "quantity",
                        "pickup",
                        "deadline",
                        "status",
                        "verified"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No donations yet.")

        if st.button("➕ Donate Surplus Food", type="primary"):
            st.session_state.page = "Donate"
            st.rerun()

    elif st.session_state.role == "NGO":

        claims = get_claimed_donations_for_user()
        available = get_available_donations()

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Available Food", len(available))

        with c2:
            st.metric("My Claims", len(claims))

        with c3:
            st.metric(
                "Picked Up",
                len([d for d in claims if d["status"] == "Picked Up"])
            )

        with c4:
            st.metric(
                "Completed",
                len([d for d in claims if d["status"] == "Completed"])
            )

        st.markdown("### Available Nearby Food")

        if available:
            for d in available[:4]:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 2, 1])

                    with col1:
                        st.markdown(f"### 🍱 {d['food_type']}")
                        st.write(
                            f"**{d['quantity']} servings** • {d['pickup']}"
                        )

                    with col2:
                        st.write(f"Deadline: **{d['deadline']}**")
                        st.write(f"Storage: {d['storage']}")

                    with col3:
                        if st.button(
                            "Claim",
                            key=f"dash_claim_{d['id']}"
                        ):
                            d["claimed_by"] = st.session_state.user_name
                            d["claim_status"] = "Pending Donor Approval"
                            d["status"] = "Claim Requested"

                            add_notification(
                                f"Claim request submitted for {d['id']}."
                            )
                            add_activity(
                                f"{st.session_state.user_name} requested {d['id']}",
                                "claim"
                            )

                            st.success("Claim request sent to donor.")
                            st.rerun()

        if st.button("🔎 Find More Food"):
            st.session_state.page = "Find Food"
            st.rerun()

    else:
        st.markdown("### 🛡️ Admin Control Center")

        pending = len([
            d for d in st.session_state.donations
            if not d["verified"]
        ])

        total = len(st.session_state.donations)
        active = len([
            d for d in st.session_state.donations
            if d["status"] not in ["Completed"]
        ])

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Listings", total)
        c2.metric("Pending Verification", pending)
        c3.metric("Active Cases", active)
        c4.metric("Completed", len([
            d for d in st.session_state.donations
            if d["status"] == "Completed"
        ]))

        st.markdown("### Recent System Activity")

        for item in st.session_state.activity[:8]:
            st.write(
                f"**{item['time']}** — {item['message']}"
            )


# ============================================================
# DONATE FOOD
# ============================================================

elif st.session_state.page == "Donate":

    page_title(
        "🍱 Donate Surplus Food",
        "List food from events, restaurants, functions or gatherings."
    )

    with st.form("donation_form"):

        st.markdown("### 1. Food Details")

        c1, c2 = st.columns(2)

        with c1:
            food_type = st.text_input(
                "Food Name *",
                placeholder="e.g. Vegetable Biryani"
            )

            category = st.selectbox(
                "Food Category",
                [
                    "Meals",
                    "Rice",
                    "Bread",
                    "Fruits & Vegetables",
                    "Bakery",
                    "Beverages",
                    "Other"
                ]
            )

            quantity = st.number_input(
                "Quantity / Servings *",
                min_value=1,
                value=20
            )

        with c2:
            prep_time = st.text_input(
                "Preparation Time *",
                placeholder="e.g. Today 6:00 PM"
            )

            deadline = st.text_input(
                "Safe Pickup Deadline *",
                placeholder="e.g. Today 10:00 PM"
            )

            storage = st.selectbox(
                "Storage Condition",
                [
                    "Covered containers",
                    "Refrigerated",
                    "Insulated containers",
                    "Room temperature",
                    "Other"
                ]
            )

        st.markdown("### 2. Pickup Details")

        c3, c4 = st.columns(2)

        with c3:
            pickup = st.text_input(
                "Pickup Location *",
                placeholder="Area / Sector / Landmark"
            )

        with c4:
            contact = st.text_input(
                "Contact Number *",
                placeholder="10-digit mobile number"
            )

        st.markdown("### 3. Food Safety Confirmation")

        safe = st.checkbox(
            "I confirm that the listed food is safe for human consumption."
        )

        prepared_hygienically = st.checkbox(
            "The food was prepared/stored hygienically."
        )

        submit = st.form_submit_button(
            "🚀 Submit Food Listing",
            use_container_width=True,
            type="primary"
        )

        if submit:

            if not food_type or not prep_time or not deadline or not pickup or not contact:
                st.error("Please complete all required fields.")

            elif not safe or not prepared_hygienically:
                st.error(
                    "Please confirm the food safety conditions before submitting."
                )

            else:
                new_id = f"FB{len(st.session_state.donations) + 1:03d}"

                new_donation = {
                    "id": new_id,
                    "donor": st.session_state.user_name,
                    "food_type": food_type,
                    "category": category,
                    "quantity": quantity,
                    "prep_time": prep_time,
                    "pickup": pickup,
                    "deadline": deadline,
                    "storage": storage,
                    "status": "Pending Verification",
                    "verified": False,
                    "claimed_by": "",
                    "claim_status": "",
                    "contact": contact,
                    "created": datetime.now()
                }

                st.session_state.donations.append(new_donation)

                add_activity(
                    f"New food listing {new_id} submitted by {st.session_state.user_name}",
                    "donation"
                )

                add_notification(
                    f"Your food listing {new_id} is waiting for verification."
                )

                st.success(
                    f"Food listing {new_id} submitted successfully!"
                )
                st.info(
                    "Admin verification is required before NGOs can see the listing."
                )


# ============================================================
# MY DONATIONS
# ============================================================

elif st.session_state.page == "My Donations":

    page_title(
        "📦 My Donations",
        "Manage listings and respond to NGO claim requests."
    )

    my_donations = [
        d for d in st.session_state.donations
        if d["donor"] == st.session_state.user_name
    ]

    # Demo fallback
    if not my_donations and st.session_state.user_name == "Demo Donor":
        my_donations = [
            d for d in st.session_state.donations
            if d["donor"] == "Demo Donor"
        ]

    if not my_donations:
        st.info("You have not created any food listing yet.")
    else:
        for d in my_donations:

            with st.container(border=True):

                top1, top2, top3 = st.columns([3, 2, 1])

                with top1:
                    st.markdown(f"### {d['id']} • 🍱 {d['food_type']}")
                    st.write(
                        f"**{d['quantity']} servings** • {d['pickup']}"
                    )

                with top2:
                    if d["verified"]:
                        st.markdown(
                            '<span class="badge verified">✓ Verified</span>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            '<span class="badge pending">⏳ Pending Verification</span>',
                            unsafe_allow_html=True
                        )

                    st.write(f"Status: **{d['status']}**")

                with top3:
                    st.write(f"Deadline:")
                    st.write(f"**{d['deadline']}**")

                if d["status"] == "Claim Requested":

                    st.warning(
                        f"NGO **{d['claimed_by']}** requested this donation."
                    )

                    a, b = st.columns(2)

                    with a:
                        if st.button(
                            "✅ Accept Claim",
                            key=f"accept_{d['id']}",
                            type="primary"
                        ):
                            d["status"] = "Accepted"
                            d["claim_status"] = "Accepted"

                            add_notification(
                                f"Claim accepted for {d['id']}."
                            )

                            add_activity(
                                f"Donor accepted NGO claim for {d['id']}",
                                "accepted"
                            )

                            st.success("Claim accepted.")
                            st.rerun()

                    with b:
                        if st.button(
                            "❌ Reject Claim",
                            key=f"reject_{d['id']}"
                        ):
                            d["status"] = "Available"
                            d["claim_status"] = "Rejected"
                            d["claimed_by"] = ""

                            add_activity(
                                f"Donor rejected claim for {d['id']}",
                                "rejected"
                            )

                            st.warning("Claim rejected.")
                            st.rerun()

                if d["status"] == "Accepted":
                    st.info(
                        f"Pickup arranged with NGO: **{d['claimed_by']}**"
                    )

                    if st.button(
                        "📦 Mark as Picked Up",
                        key=f"pickup_{d['id']}"
                    ):
                        d["status"] = "Picked Up"

                        add_activity(
                            f"{d['id']} marked as picked up",
                            "pickup"
                        )

                        st.success("Donation marked as picked up.")
                        st.rerun()

                if d["status"] == "Picked Up":
                    if st.button(
                        "🏁 Mark Completed",
                        key=f"complete_{d['id']}"
                    ):
                        d["status"] = "Completed"

                        add_activity(
                            f"{d['id']} donation completed",
                            "completed"
                        )

                        add_notification(
                            f"{d['id']} has been completed."
                        )

                        st.success("Donation completed.")
                        st.rerun()


# ============================================================
# FIND FOOD
# ============================================================

elif st.session_state.page == "Find Food":

    page_title(
        "🔎 Find Surplus Food",
        "Browse verified food listings and submit claim requests."
    )

    available = get_available_donations()

    c1, c2, c3 = st.columns(3)

    with c1:
        search = st.text_input(
            "Search food / location",
            placeholder="biryani, Noida..."
        )

    with c2:
        category_filter = st.selectbox(
            "Category",
            ["All"] + sorted(
                list(set(d["category"] for d in available))
            )
        )

    with c3:
        min_qty = st.number_input(
            "Minimum quantity",
            min_value=0,
            value=0
        )

    filtered = []

    for d in available:

        text_match = (
            not search
            or search.lower() in d["food_type"].lower()
            or search.lower() in d["pickup"].lower()
            or search.lower() in d["donor"].lower()
        )

        category_match = (
            category_filter == "All"
            or d["category"] == category_filter
        )

        quantity_match = d["quantity"] >= min_qty

        if text_match and category_match and quantity_match:
            filtered.append(d)

    st.markdown(
        f"### {len(filtered)} verified listing(s) available"
    )

    if not filtered:
        st.warning("No food listing matches your filters.")

    for d in filtered:

        with st.container(border=True):

            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                st.markdown(
                    f"### 🍲 {d['food_type']}"
                )
                st.write(
                    f"**{d['quantity']} servings**"
                )
                st.write(
                    f"📍 {d['pickup']}"
                )
                st.write(
                    f"🏢 Donor: {d['donor']}"
                )

            with col2:
                st.write(
                    f"⏰ **Pickup deadline:** {d['deadline']}"
                )
                st.write(
                    f"🔥 Prepared: {d['prep_time']}"
                )
                st.write(
                    f"📦 Storage: {d['storage']}"
                )

                st.markdown(
                    '<span class="badge verified">✓ Admin Verified</span>',
                    unsafe_allow_html=True
                )

            with col3:

                if st.button(
                    "🤝 Claim Food",
                    key=f"claim_{d['id']}",
                    type="primary"
                ):

                    d["claimed_by"] = st.session_state.user_name
                    d["claim_status"] = "Pending Donor Approval"
                    d["status"] = "Claim Requested"

                    add_notification(
                        f"Claim request sent for {d['food_type']}."
                    )

                    add_activity(
                        f"{st.session_state.user_name} requested donation {d['id']}",
                        "claim"
                    )

                    st.success("Request sent to donor!")
                    st.rerun()


# ============================================================
# MY CLAIMS
# ============================================================

elif st.session_state.page == "My Claims":

    page_title(
        "📍 My Claims",
        "Track food requests from donor approval to completion."
    )

    claims = get_claimed_donations_for_user()

    if not claims:
        st.info(
            "You have no claims yet. Go to 'Find Food' to discover available donations."
        )

    for d in claims:

        with st.container(border=True):

            st.markdown(
                f"### {d['id']} • {d['food_type']}"
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.write(f"Quantity: **{d['quantity']} servings**")
                st.write(f"Pickup: **{d['pickup']}**")

            with c2:
                st.write(f"Donor: **{d['donor']}**")
                st.write(f"Deadline: **{d['deadline']}**")

            with c3:
                status = d["status"]

                if status == "Claim Requested":
                    st.warning("⏳ Waiting for donor approval")

                elif status == "Accepted":
                    st.success("✅ Accepted by donor")

                    if st.button(
                        "🚚 Confirm Pickup",
                        key=f"ngo_pickup_{d['id']}"
                    ):
                        d["status"] = "Picked Up"

                        add_activity(
                            f"NGO confirmed pickup for {d['id']}",
                            "pickup"
                        )

                        st.success("Pickup confirmed.")
                        st.rerun()

                elif status == "Picked Up":
                    st.info("🚚 Food picked up")

                    if st.button(
                        "🏁 Mark Delivery Complete",
                        key=f"ngo_complete_{d['id']}"
                    ):
                        d["status"] = "Completed"

                        add_activity(
                            f"NGO completed delivery for {d['id']}",
                            "completed"
                        )

                        add_notification(
                            f"Delivery for {d['id']} completed successfully."
                        )

                        st.success("Delivery completed!")
                        st.rerun()

                elif status == "Completed":
                    st.success("🎉 Completed")


# ============================================================
# VERIFICATION - ADMIN
# ============================================================

elif st.session_state.page == "Verification":

    page_title(
        "🛡️ Food Verification",
        "Review new listings before they become visible to NGOs."
    )

    pending = [
        d for d in st.session_state.donations
        if not d["verified"]
    ]

    if not pending:
        st.success("All food listings are currently verified.")
    else:

        st.info(
            f"{len(pending)} listing(s) waiting for verification."
        )

        for d in pending:

            with st.container(border=True):

                st.markdown(
                    f"### {d['id']} • {d['food_type']}"
                )

                c1, c2 = st.columns(2)

                with c1:
                    st.write(f"Donor: **{d['donor']}**")
                    st.write(f"Category: **{d['category']}**")
                    st.write(f"Quantity: **{d['quantity']} servings**")
                    st.write(f"Preparation: **{d['prep_time']}**")

                with c2:
                    st.write(f"Pickup: **{d['pickup']}**")
                    st.write(f"Deadline: **{d['deadline']}**")
                    st.write(f"Storage: **{d['storage']}**")

                a, b = st.columns(2)

                with a:
                    if st.button(
                        "✅ Verify Listing",
                        key=f"verify_{d['id']}",
                        type="primary"
                    ):
                        d["verified"] = True
                        d["status"] = "Available"

                        add_activity(
                            f"Admin verified food listing {d['id']}",
                            "verification"
                        )

                        add_notification(
                            f"{d['id']} has been verified and is now visible to NGOs."
                        )

                        st.success("Listing verified.")
                        st.rerun()

                with b:
                    if st.button(
                        "❌ Reject Listing",
                        key=f"admin_reject_{d['id']}"
                    ):
                        d["status"] = "Rejected"

                        add_activity(
                            f"Admin rejected food listing {d['id']}",
                            "rejection"
                        )

                        st.warning("Listing rejected.")
                        st.rerun()


# ============================================================
# ADMIN DASHBOARD
# ============================================================

elif st.session_state.page == "Admin Dashboard":

    page_title(
        "📊 Admin Dashboard",
        "Monitor listings, claims and platform activity."
    )

    total = len(st.session_state.donations)

    available = len([
        d for d in st.session_state.donations
        if d["status"] == "Available"
    ])

    requested = len([
        d for d in st.session_state.donations
        if d["status"] == "Claim Requested"
    ])

    completed = len([
        d for d in st.session_state.donations
        if d["status"] == "Completed"
    ])

    pending = len([
        d for d in st.session_state.donations
        if not d["verified"]
    ])

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Total", total)
    c2.metric("Available", available)
    c3.metric("Claims", requested)
    c4.metric("Completed", completed)
    c5.metric("Verification", pending)

    st.markdown("### Donation Pipeline")

    pipeline = pd.DataFrame({
        "Status": [
            "Pending Verification",
            "Available",
            "Claim Requested",
            "Accepted",
            "Picked Up",
            "Completed",
            "Rejected"
        ],
        "Count": [
            len([d for d in st.session_state.donations if d["status"] == "Pending Verification"]),
            len([d for d in st.session_state.donations if d["status"] == "Available"]),
            len([d for d in st.session_state.donations if d["status"] == "Claim Requested"]),
            len([d for d in st.session_state.donations if d["status"] == "Accepted"]),
            len([d for d in st.session_state.donations if d["status"] == "Picked Up"]),
            len([d for d in st.session_state.donations if d["status"] == "Completed"]),
            len([d for d in st.session_state.donations if d["status"] == "Rejected"])
        ]
    })

    st.bar_chart(
        pipeline.set_index("Status")
    )

    st.markdown("### All Food Listings")

    df = pd.DataFrame(st.session_state.donations)

    if not df.empty:
        st.dataframe(
            df[
                [
                    "id",
                    "donor",
                    "food_type",
                    "quantity",
                    "pickup",
                    "deadline",
                    "status",
                    "verified",
                    "claimed_by"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# IMPACT DASHBOARD
# ============================================================

elif st.session_state.page == "Impact":

    page_title(
        "📈 Impact Dashboard",
        "Measure how FoodBridge converts surplus into community impact."
    )

    completed = [
        d for d in st.session_state.donations
        if d["status"] == "Completed"
    ]

    total_completed = len(completed)
    meals = sum(d["quantity"] for d in completed)
    rescued = sum(d["quantity"] for d in st.session_state.donations
                  if d["status"] in ["Accepted", "Picked Up", "Completed"])

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🍱 Completed Donations", total_completed)
    c2.metric("🍽️ Estimated Meals", meals)
    c3.metric("♻️ Food Rescued", rescued)
    c4.metric("🌱 Waste Diversion", f"{rescued} servings")

    st.markdown("### Impact Breakdown")

    categories = {}

    for d in completed:
        categories[d["category"]] = (
            categories.get(d["category"], 0) + d["quantity"]
        )

    if categories:
        chart_df = pd.DataFrame(
            {
                "Category": list(categories.keys()),
                "Servings": list(categories.values())
            }
        )

        st.bar_chart(
            chart_df.set_index("Category")
        )
    else:
        st.info(
            "Complete a donation to populate the impact chart."
        )

    st.markdown("""
    <div class="card">
        <h3>💡 How the impact is calculated</h3>
        <p>
        For this hackathon MVP, the number of estimated meals is based on
        the quantity/servings entered by the donor. In a production system,
        this calculation could be connected to verified quantity and
        beneficiary records.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# ALERTS
# ============================================================

elif st.session_state.page == "Alerts":

    page_title(
        "🔔 Alerts & Notifications",
        "Important FoodBridge activity and deadline reminders."
    )

    if not st.session_state.notifications:
        st.success("No new notifications.")
    else:
        for i, notification in enumerate(
            st.session_state.notifications
        ):
            st.info(notification)

        if st.button("Clear Notifications"):
            st.session_state.notifications = []
            st.rerun()

    st.markdown("### ⏰ Expiry / Deadline Monitoring")

    now = datetime.now()

    active = [
        d for d in st.session_state.donations
        if d["status"] in ["Available", "Claim Requested", "Accepted"]
    ]

    if active:
        for d in active:
            # Demo alert logic:
            # Real production version should parse actual deadline timestamps.
            st.warning(
                f"⚠️ **{d['id']}** — {d['food_type']} — "
                f"Pickup deadline: **{d['deadline']}**"
            )
    else:
        st.success("No active food listings requiring attention.")


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    <b>FoodBridge</b> • From Surplus to Need, Before It's Too Late.<br>
    Hackathon MVP • Built for demonstration and workflow validation.
</div>
""", unsafe_allow_html=True)
