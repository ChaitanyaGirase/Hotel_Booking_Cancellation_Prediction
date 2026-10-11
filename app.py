import streamlit as st
import joblib
import pandas as pd
from pathlib import Path

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="StayWise | Cancellation Predictor",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 2. CUSTOM DESIGN
# =========================================================

st.markdown("""
<style>
    .stApp {
        background: #f3f6fb;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(120deg, #102a43, #176b70);
        padding: 34px;
        border-radius: 20px;
        color: white;
        margin-bottom: 24px;
    }

    .hero h1 {
        color: white;
        font-size: 36px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #e0f2f1;
        font-size: 16px;
        margin-bottom: 4px;
    }

    .section-heading {
        color: #17324d;
        font-size: 21px;
        font-weight: 700;
        margin-bottom: 16px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: white;
        border: 1px solid #e1e8ef;
        border-radius: 16px;
    }

    div.stButton > button {
        width: 100%;
        min-height: 50px;
        background: #137c78;
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background: #105f5c;
        color: white;
        border: none;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e1e8ef;
        border-radius: 12px;
        padding: 16px;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. LOAD TRAINED MODEL
# =========================================================

MODEL_PATH = Path(__file__).parent / "model" / "hotel_cancellation_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except Exception as error:
    st.error(f"Could not load the trained model: {error}")
    st.stop()

# =========================================================
# 4. HEADER
# =========================================================

st.markdown("""
<div class="hero">
    <h1>🏨 Hotel Booking Cancellation Prediction</h1>
    <p>
        Estimate whether a hotel booking may be cancelled
        using your trained machine-learning model.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "Complete the booking details below and select "
    "**Predict Cancellation** to view the result."
)

# =========================================================
# 5. BOOKING DETAILS
# =========================================================

with st.container(border=True):
    st.markdown(
        '<div class="section-heading">📅 Booking Details</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        hotel = st.selectbox(
            "Hotel Type",
            ["City Hotel", "Resort Hotel"]
        )

        lead_time = st.number_input(
            "Lead Time (days)",
            min_value=0,
            max_value=1000,
            value=30
        )

        arrival_date_year = st.selectbox(
            "Arrival Year",
            [2015, 2016, 2017]
        )

        arrival_date_month = st.selectbox(
            "Arrival Month",
            [
                "January", "February", "March", "April",
                "May", "June", "July", "August",
                "September", "October", "November", "December"
            ]
        )

    with col2:
        arrival_date_week_number = st.number_input(
            "Arrival Week Number",
            min_value=1,
            max_value=53,
            value=25
        )

        arrival_date_day_of_month = st.number_input(
            "Arrival Day of Month",
            min_value=1,
            max_value=31,
            value=15
        )

        stays_in_weekend_nights = st.number_input(
            "Weekend Nights",
            min_value=0,
            max_value=20,
            value=2
        )

        stays_in_week_nights = st.number_input(
            "Week Nights",
            min_value=0,
            max_value=50,
            value=3
        )

    with col3:
        meal = st.selectbox(
            "Meal Plan",
            ["BB", "HB", "FB", "SC", "Undefined"]
        )

        market_segment = st.selectbox(
            "Market Segment",
            [
                "Online TA", "Offline TA/TO", "Groups",
                "Direct", "Corporate", "Complementary",
                "Aviation", "Undefined"
            ]
        )

        distribution_channel = st.selectbox(
            "Distribution Channel",
            ["TA/TO", "Direct", "Corporate", "GDS", "Undefined"]
        )

# =========================================================
# 6. GUEST INFORMATION
# =========================================================

with st.container(border=True):
    st.markdown(
        '<div class="section-heading">👥 Guest Information</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        adults = st.number_input(
            "Number of Adults",
            min_value=0,
            max_value=20,
            value=2
        )

        children = st.number_input(
            "Number of Children",
            min_value=0,
            max_value=10,
            value=0
        )

    with col2:
        babies = st.number_input(
            "Number of Babies",
            min_value=0,
            max_value=10,
            value=0
        )

        is_repeated_guest = st.selectbox(
            "Is Repeated Guest?",
            ["No", "Yes"]
        )

    with col3:
        customer_type = st.selectbox(
            "Customer Type",
            ["Transient", "Transient-Party", "Contract", "Group"]
        )

        country = st.text_input(
            "Country Code",
            value="PRT",
            help="Enter a three-letter country code, such as PRT or GBR."
        ).strip().upper()

# Convert Yes/No to numeric, as required by the numeric pipeline.
is_repeated_guest_value = (
    1 if is_repeated_guest == "Yes" else 0
)

# =========================================================
# 7. BOOKING HISTORY AND PREFERENCES
# =========================================================

with st.container(border=True):
    st.markdown(
        '<div class="section-heading">🧾 Booking History & Preferences</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        deposit_type = st.selectbox(
            "Deposit Type",
            ["No Deposit", "Non Refund", "Refundable"]
        )

        reserved_room_type = st.selectbox(
            "Reserved Room Type",
            ["A", "B", "C", "D", "E", "F", "G", "H", "L"]
        )

        agent = st.number_input(
            "Agent ID (0 if none)",
            min_value=0,
            value=0
        )

    with col2:
        previous_cancellations = st.number_input(
            "Previous Cancellations",
            min_value=0,
            value=0
        )

        previous_bookings_not_canceled = st.number_input(
            "Previous Bookings Not Cancelled",
            min_value=0,
            value=0
        )

        booking_changes = st.number_input(
            "Booking Changes",
            min_value=0,
            value=0
        )

    with col3:
        days_in_waiting_list = st.number_input(
            "Days in Waiting List",
            min_value=0,
            value=0
        )

        adr = st.number_input(
            "Average Daily Rate",
            min_value=0.0,
            value=100.0,
            step=10.0
        )

        required_car_parking_spaces = st.number_input(
            "Required Car Parking Spaces",
            min_value=0,
            max_value=10,
            value=0
        )

        total_of_special_requests = st.number_input(
            "Total Special Requests",
            min_value=0,
            max_value=10,
            value=0
        )

# =========================================================
# 8. ENGINEERED FEATURES
# =========================================================

total_nights = (
    int(stays_in_weekend_nights)
    + int(stays_in_week_nights)
)

total_guests = (
    int(adults)
    + int(children)
    + int(babies)
)

total_previous_bookings = (
    int(previous_cancellations)
    + int(previous_bookings_not_canceled)
)

has_special_request = int(total_of_special_requests > 0)

st.markdown("### 📌 Booking Summary")

m1, m2, m3 = st.columns(3)

m1.metric("Total Nights", total_nights)
m2.metric("Total Guests", total_guests)
m3.metric("Special Requests", int(total_of_special_requests))

# =========================================================
# 9. PREDICTION
# =========================================================

st.markdown("---")

if st.button("🔍 Predict Cancellation", use_container_width=True):

    if not country:
        st.error("Please enter a country code.")
        st.stop()

    # IMPORTANT:
    # Keep all feature names aligned with model training.
    # agent is converted to a string because the trained
    # categorical encoder expects string categories.

    input_data = pd.DataFrame([{
        "hotel": hotel,
        "lead_time": lead_time,
        "arrival_date_year": arrival_date_year,
        "arrival_date_month": arrival_date_month,
        "arrival_date_week_number": arrival_date_week_number,
        "arrival_date_day_of_month": arrival_date_day_of_month,
        "stays_in_weekend_nights": stays_in_weekend_nights,
        "stays_in_week_nights": stays_in_week_nights,
        "adults": adults,
        "children": children,
        "babies": babies,
        "meal": meal,
        "country": country,
        "market_segment": market_segment,
        "distribution_channel": distribution_channel,
        "is_repeated_guest": is_repeated_guest_value,
        "previous_cancellations": previous_cancellations,
        "previous_bookings_not_canceled": previous_bookings_not_canceled,
        "reserved_room_type": reserved_room_type,
        "booking_changes": booking_changes,
        "deposit_type": deposit_type,
        "agent": str(int(agent)),
        "days_in_waiting_list": days_in_waiting_list,
        "customer_type": customer_type,
        "adr": adr,
        "required_car_parking_spaces": required_car_parking_spaces,
        "total_of_special_requests": total_of_special_requests,
        "total_nights": total_nights,
        "total_guests": total_guests,
        "total_previous_bookings": total_previous_bookings,
        "has_special_request": has_special_request
    }])

    try:
        prediction = model.predict(input_data)[0]

        st.markdown("## Prediction Result")

        if prediction == 1:
            st.error(
                "### ⚠️ Cancellation Predicted\n\n"
                "Based on the provided booking details, "
                "the model predicts that this booking may be cancelled."
            )
        else:
            st.success(
                "### ✅ Booking Likely to Be Retained\n\n"
                "Based on the provided booking details, "
                "the model predicts that this booking may not be cancelled."
            )

        st.caption(
            "This is a machine-learning prediction, not a guarantee. "
            "The model's output depends on the information entered."
        )

        with st.expander("View submitted booking details"):
            st.dataframe(
                input_data.T.rename(columns={0: "Value"}),
                use_container_width=True
            )

    except Exception as error:
        st.error(
            "Prediction could not be completed. "
            "Please check the input values and try again."
        )
        st.exception(error)

# =========================================================
# 10. FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#718096; padding:10px;">
        Hotel Booking Cancellation Prediction<br>
        Built with Streamlit and Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)