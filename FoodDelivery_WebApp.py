import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib

st.set_page_config(
    page_title="Food Delivery Analytics",
    page_icon="🍽️",
    layout="wide"
)

st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #0E1117;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background-color: #1E1E1E;
    border: 1px solid #31333F;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

/* Metric Label */
[data-testid="metric-container"] label {
    color: #BBBBBB !important;
    font-size: 15px !important;
    font-weight: 600;
}

/* Metric Value */
[data-testid="metric-container"] div {
    color: white !important;
}

/* Headers */
h1, h2, h3 {
    color: white !important;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    font-size: 16px;
    font-weight: 600;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161A23;
}

/* Info Boxes */
.stAlert {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

USER_ID = "admin"
PASSWORD = "admin123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login_page():
    st.title("🍽️ Food Delivery Analytics Web App")
    st.subheader("Login")

    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if user_id == USER_ID and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid User ID or Password")


if not st.session_state.logged_in:
    login_page()
    st.stop()


@st.cache_data
def load_data():
    users_df = pd.read_csv("USERS_CLEAN.csv",low_memory=False)
    restaurant_df = pd.read_csv("RESTAURANT_CLEAN.csv",low_memory=False)
    menu_df = pd.read_csv(
        "MENU_CLEAN.csv",
        usecols=["MENU_ID", "R_ID", "F_ID", "CUISINE", "PRICE", "PRICE_RANGE"],
        low_memory=False
    )
    food_df = pd.read_csv("FOOD_CLEAN.csv",low_memory=False)

    # Auto-detect real header row in ORDERS file
    with open("ORDERS_CLEAN.csv", "r", encoding="utf-8", errors="ignore") as file:
        lines = file.readlines()

    header_row = 0
    for i, line in enumerate(lines):
        if line.startswith("ORDER_ID"):
            header_row = i
            break

    orders_df = pd.read_csv(
        "ORDERS_CLEAN.csv",
        skiprows=header_row,
        low_memory=False
    )

    orders_df.columns = orders_df.columns.str.strip().str.upper()

    # Remove repeated header/conflict rows if present
    orders_df = orders_df[orders_df["ORDER_ID"].astype(str) != "ORDER_ID"]
    orders_df = orders_df[~orders_df["ORDER_ID"].astype(str).str.contains("<<<<<<<|=======|>>>>>>>", regex=True, na=False)]

    # Convert required numeric/date columns
    orders_df["ORDER_DATE"] = pd.to_datetime(orders_df["ORDER_DATE"], errors="coerce")
    orders_df["SALES_AMOUNT"] = pd.to_numeric(orders_df["SALES_AMOUNT"], errors="coerce")
    orders_df["SALES_QTY"] = pd.to_numeric(orders_df["SALES_QTY"], errors="coerce")
    orders_df["ORDER_YEAR"] = pd.to_numeric(orders_df["ORDER_YEAR"], errors="coerce")
    orders_df["ORDER_MONTH"] = pd.to_numeric(orders_df["ORDER_MONTH"], errors="coerce")
    orders_df["WEEKEND_FLAG"] = pd.to_numeric(orders_df["WEEKEND_FLAG"], errors="coerce")
    orders_df["USER_ID"] = pd.to_numeric(orders_df["USER_ID"], errors="coerce")
    orders_df["R_ID"] = pd.to_numeric(orders_df["R_ID"], errors="coerce")

    orders_df = orders_df.dropna(subset=["ORDER_ID", "SALES_AMOUNT", "USER_ID", "R_ID"])
    orders_df = orders_df.drop_duplicates(subset=["ORDER_ID"])

    return users_df, orders_df, restaurant_df, menu_df, food_df

@st.cache_resource
def load_model_files():
    model = joblib.load("logistic_high_revenue_model.pkl")
    scaler = joblib.load("scaler.pkl")
    model_features = joblib.load("model_features.pkl")
    top_cities = joblib.load("top_cities.pkl")
    top_cuisines = joblib.load("top_cuisines.pkl")

    return model, scaler, model_features, top_cities, top_cuisines


users_df, orders_df, restaurant_df, menu_df, food_df = load_data()
model, scaler, model_features, top_cities, top_cuisines = load_model_files()

orders_restaurant_df = orders_df.merge(
    restaurant_df,
    left_on="R_ID",
    right_on="ID",
    how="left"
)

orders_users_df = orders_df.merge(
    users_df,
    on="USER_ID",
    how="left"
)

full_orders_df = orders_users_df.merge(
    restaurant_df,
    left_on="R_ID",
    right_on="ID",
    how="left"
)

menu_food_df = menu_df.merge(
    food_df,
    on="F_ID",
    how="left"
)

menu_full_df = menu_food_df.merge(
    restaurant_df,
    left_on="R_ID",
    right_on="ID",
    how="left"
)

st.sidebar.title("🍽️ Food Delivery Analytics")
st.sidebar.markdown("---")
st.sidebar.success("Final Analytics Project")
st.sidebar.info("Interactive Business Intelligence Web Application")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.title("🍽️ Food Delivery Analytics Dashboard")

st.write(
    "This application provides business intelligence, customer analytics, "
    "menu pricing analysis, and predictive modeling for food delivery platforms."
)

st.caption("Business Intelligence | Visual Analytics | Predictive Modeling")

tab1, tab2, tab3 = st.tabs([
    "📌 KPIs & Key Insights",
    "📊 Visual Analytics",
    "🤖 High Revenue Restaurant Prediction"
])

with tab1:
    st.header("📌 Business KPIs & Key Insights")

    total_revenue = orders_df["SALES_AMOUNT"].sum()
    total_orders = orders_df["ORDER_ID"].nunique()
    active_customers = orders_df["USER_ID"].nunique()
    avg_order_value = total_revenue / total_orders
    avg_menu_price = menu_df["PRICE"].mean()

    repeat_customers = orders_df.groupby("USER_ID")["ORDER_ID"].count().reset_index()

    repeat_customers_count = repeat_customers[
        repeat_customers["ORDER_ID"] > 1
    ]["USER_ID"].nunique()

    repeat_customer_pct = repeat_customers_count / active_customers * 100

    weekend_orders_pct = (
        orders_df[orders_df["WEEKEND_FLAG"] == 1]["ORDER_ID"].nunique()
        / total_orders * 100
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Revenue", f"₹{total_revenue/1_000_000:.1f}M")
    c2.metric("Total Orders", f"{total_orders/1000:.0f}K")
    c3.metric("Active Customers", f"{active_customers/1000:.0f}K")
    c4.metric("Average Order Value", f"₹{avg_order_value:.0f}")

    c5, c6, c7, c8 = st.columns(4)

    c5.metric("Repeat Customers", f"{repeat_customers_count/1000:.0f}K")
    c6.metric("Repeat Customer %", f"{repeat_customer_pct:.1f}%")
    c7.metric("Weekend Orders %", f"{weekend_orders_pct:.1f}%")
    c8.metric("Average Menu Price", f"₹{avg_menu_price:.0f}")

    st.divider()

    st.subheader("🔎 Key Business Insights")

    top_city = orders_restaurant_df.groupby("CITY")["SALES_AMOUNT"].sum().sort_values(ascending=False).index[0]
    top_cuisine = orders_restaurant_df.groupby("CUISINE")["SALES_AMOUNT"].sum().sort_values(ascending=False).index[0]
    top_restaurant = orders_restaurant_df.groupby("NAME")["SALES_AMOUNT"].sum().sort_values(ascending=False).index[0]
    top_order_city = orders_restaurant_df.groupby("CITY")["ORDER_ID"].nunique().sort_values(ascending=False).index[0]
    top_menu_cuisine = menu_df.groupby("CUISINE")["MENU_ID"].nunique().sort_values(ascending=False).index[0]
    highest_price_cuisine = menu_df.groupby("CUISINE")["PRICE"].mean().sort_values(ascending=False).index[0]

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"🏙️ **Top Revenue City:** {top_city}")
        st.info(f"🍱 **Top Revenue Cuisine:** {top_cuisine}")
        st.info(f"🏆 **Top Revenue Restaurant:** {top_restaurant}")
        st.info(f"📦 **Top Order City:** {top_order_city}")

    with col2:
        st.success(f"🔁 Repeat customer rate is **{repeat_customer_pct:.1f}%**, showing customer retention strength.")
        st.success(f"📅 Weekend orders contribute **{weekend_orders_pct:.1f}%**, indicating stronger weekday ordering behavior.")
        st.success(f"💰 Average order value is **₹{avg_order_value:.0f}**, showing healthy customer spending.")
        st.success(f"🍽️ **{top_menu_cuisine}** has the widest menu presence, while **{highest_price_cuisine}** has higher average pricing.")


with tab2:
    st.header("📊 Visual Analytics")

    st.subheader("Filters")

    f1, f2, f3, f4 = st.columns(4)

    selected_city = f1.multiselect(
        "City",
        sorted(orders_restaurant_df["CITY"].dropna().unique())
    )

    selected_cuisine = f2.multiselect(
        "Cuisine",
        sorted(orders_restaurant_df["CUISINE"].dropna().unique())
    )

    selected_year = f3.multiselect(
        "Order Year",
        sorted(orders_df["ORDER_YEAR"].dropna().unique())
    )

    selected_price_range = f4.multiselect(
        "Price Range",
        sorted(menu_df["PRICE_RANGE"].dropna().unique())
    )

    filtered_orders_restaurant_df = orders_restaurant_df.copy()
    filtered_full_orders_df = full_orders_df.copy()
    filtered_menu_df = menu_df.copy()
    filtered_menu_full_df = menu_full_df.copy()

    if selected_city:
        filtered_orders_restaurant_df = filtered_orders_restaurant_df[
            filtered_orders_restaurant_df["CITY"].isin(selected_city)
        ]

        filtered_full_orders_df = filtered_full_orders_df[
            filtered_full_orders_df["CITY"].isin(selected_city)
        ]

        filtered_menu_full_df = filtered_menu_full_df[
            filtered_menu_full_df["CITY"].isin(selected_city)
        ]

    if selected_cuisine:
        filtered_orders_restaurant_df = filtered_orders_restaurant_df[
            filtered_orders_restaurant_df["CUISINE"].isin(selected_cuisine)
        ]

        filtered_full_orders_df = filtered_full_orders_df[
            filtered_full_orders_df["CUISINE"].isin(selected_cuisine)
        ]

        filtered_menu_df = filtered_menu_df[
            filtered_menu_df["CUISINE"].isin(selected_cuisine)
        ]

        filtered_menu_full_df = filtered_menu_full_df[
            filtered_menu_full_df["CUISINE"].isin(selected_cuisine)
        ]

    if selected_year:
        filtered_orders_restaurant_df = filtered_orders_restaurant_df[
            filtered_orders_restaurant_df["ORDER_YEAR"].isin(selected_year)
        ]

        filtered_full_orders_df = filtered_full_orders_df[
            filtered_full_orders_df["ORDER_YEAR"].isin(selected_year)
        ]

    if selected_price_range:
        filtered_menu_df = filtered_menu_df[
            filtered_menu_df["PRICE_RANGE"].isin(selected_price_range)
        ]

        filtered_menu_full_df = filtered_menu_full_df[
            filtered_menu_full_df["PRICE_RANGE"].isin(selected_price_range)
        ]

    st.subheader("📥 Download Filtered Data")

    d1, d2 = st.columns(2)

    csv_orders = filtered_orders_restaurant_df.to_csv(index=False).encode("utf-8")

    d1.download_button(
        label="Download Orders Data",
        data=csv_orders,
        file_name="filtered_orders_data.csv",
        mime="text/csv"
    )

    csv_menu = filtered_menu_df.to_csv(index=False).encode("utf-8")

    d2.download_button(
        label="Download Menu Data",
        data=csv_menu,
        file_name="filtered_menu_data.csv",
        mime="text/csv"
    )

    st.divider()

    if filtered_orders_restaurant_df.empty:
        st.warning("No records found for the selected filters.")
        st.stop()

    st.subheader("Business & Sales Overview")

    col1, col2 = st.columns(2)

    revenue_trend = (
        filtered_orders_restaurant_df.groupby(["ORDER_YEAR", "ORDER_MONTH"])["SALES_AMOUNT"]
        .sum()
        .reset_index()
    )

    revenue_trend["YEAR_MONTH"] = (
        revenue_trend["ORDER_YEAR"].astype(str)
        + "-"
        + revenue_trend["ORDER_MONTH"].astype(str).str.zfill(2)
    )

    fig1 = px.line(
        revenue_trend,
        x="YEAR_MONTH",
        y="SALES_AMOUNT",
        markers=True,
        title="Revenue Trend Over Time"
    )


    col1.plotly_chart(fig1, width="stretch")
    col1.info("Insight: Revenue trend helps identify growth, decline, and seasonal movement across selected filters.")

    top_restaurants_revenue = (
        filtered_orders_restaurant_df.groupby("NAME")["SALES_AMOUNT"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(
        top_restaurants_revenue,
        x="SALES_AMOUNT",
        y="NAME",
        orientation="h",
        title="Top Restaurants by Revenue",
        text_auto=".2s"
    )
    fig2.update_layout(yaxis={"categoryorder": "total ascending"})


    col2.plotly_chart(fig2, width="stretch")
    col2.info("Insight: A smaller group of restaurants contributes significantly to total revenue.")

    col3, col4 = st.columns(2)

    top_cities_revenue = (
        filtered_orders_restaurant_df.groupby("CITY")["SALES_AMOUNT"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig3 = px.bar(
        top_cities_revenue,
        x="SALES_AMOUNT",
        y="CITY",
        orientation="h",
        title="Top Cities by Revenue",
        text_auto=".2s"
    )
    fig3.update_layout(yaxis={"categoryorder": "total ascending"})

    col3.plotly_chart(fig3, width="stretch")
    col3.info("Insight: City-level revenue highlights the strongest food delivery markets.")

    cuisine_revenue = (
        filtered_orders_restaurant_df.groupby("CUISINE")["SALES_AMOUNT"]
        .sum()
        .sort_values(ascending=False)
        .head(8)
        .reset_index()
    )

    fig4 = px.pie(
        cuisine_revenue,
        names="CUISINE",
        values="SALES_AMOUNT",
        hole=0.45,
        title="Revenue Contribution by Cuisine"
    )

    col4.plotly_chart(fig4, width="stretch")
    col4.info("Insight: Cuisine contribution shows which food categories drive the highest sales.")

    st.divider()

    st.subheader("Customer & Restaurant Performance")

    col5, col6 = st.columns(2)

    age_group_customers = (
        filtered_full_orders_df.groupby("AGE_GROUP")["USER_ID"]
        .nunique()
        .reset_index()
        .rename(columns={"USER_ID": "ACTIVE_CUSTOMERS"})
    )

    fig5 = px.bar(
        age_group_customers,
        x="AGE_GROUP",
        y="ACTIVE_CUSTOMERS",
        title="Active Customers by Age Group",
        text_auto=".2s"
    )


    col5.plotly_chart(fig5, width="stretch")
    col5.info("Insight: Age group distribution identifies the strongest ordering customer segment.")

    top_restaurants_orders = (
        filtered_orders_restaurant_df.groupby("NAME")["ORDER_ID"]
        .nunique()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig6 = px.bar(
        top_restaurants_orders,
        x="ORDER_ID",
        y="NAME",
        orientation="h",
        title="Top Restaurants by Orders",
        text_auto=True
    )
    fig6.update_layout(yaxis={"categoryorder": "total ascending"})


    col6.plotly_chart(fig6, width="stretch")
    col6.info("Insight: Restaurants with high order volume show strong customer demand and operational performance.")

    col7, col8 = st.columns(2)

    cuisine_gender_orders = (
        filtered_full_orders_df.groupby(["CUISINE", "GENDER"])["ORDER_ID"]
        .nunique()
        .reset_index()
    )

    if not filtered_full_orders_df.empty:
        top_cuisine_list = (
            filtered_full_orders_df["CUISINE"]
            .value_counts()
            .head(6)
            .index
        )

        cuisine_gender_orders = cuisine_gender_orders[
            cuisine_gender_orders["CUISINE"].isin(top_cuisine_list)
        ]

    fig7 = px.bar(
        cuisine_gender_orders,
        x="CUISINE",
        y="ORDER_ID",
        color="GENDER",
        barmode="group",
        title="Cuisine Preference by Gender",
        text_auto=".2s"
    )

    col7.plotly_chart(fig7, width="stretch")
    col7.info("Insight: Cuisine preference by gender supports customer segmentation and targeted marketing.")

    filtered_user_ids = filtered_full_orders_df["USER_ID"].dropna().unique()
    filtered_users_df = users_df[users_df["USER_ID"].isin(filtered_user_ids)]

    occupation_customers = (
        filtered_users_df.groupby("OCCUPATION")["USER_ID"]
        .nunique()
        .sort_values(ascending=False)
        .head(6)
        .reset_index()
    )

    fig8 = px.pie(
        occupation_customers,
        names="OCCUPATION",
        values="USER_ID",
        hole=0.45,
        title="Customer Distribution by Occupation"
    )

    col8.plotly_chart(fig8, width="stretch")
    col8.info("Insight: Occupation distribution shows the dominant customer groups using the platform.")

    st.divider()

    st.subheader("Menu & Pricing Intelligence")

    if filtered_menu_df.empty:
        st.warning("No menu records found for the selected filters.")
    else:
        col9, col10 = st.columns(2)

        avg_price_cuisine = (
            filtered_menu_df.groupby("CUISINE")["PRICE"]
            .mean()
            .sort_values(ascending=False)
            .head(8)
            .reset_index()
        )

        fig9 = px.bar(
            avg_price_cuisine,
            x="CUISINE",
            y="PRICE",
            title="Average Menu Price by Cuisine",
            text_auto=".2s"
        )

        col9.plotly_chart(fig9, width="stretch")
        col9.info("Insight: Average menu price by cuisine highlights premium and budget cuisine categories.")

        menu_items_cuisine = (
            filtered_menu_df.groupby("CUISINE")["MENU_ID"]
            .nunique()
            .sort_values(ascending=False)
            .head(8)
            .reset_index()
        )

        fig10 = px.bar(
            menu_items_cuisine,
            x="MENU_ID",
            y="CUISINE",
            orientation="h",
            title="Total Menu Items by Cuisine",
            text_auto=".2s"
        )
        fig10.update_layout(yaxis={"categoryorder": "total ascending"})

        col10.plotly_chart(fig10, width="stretch")
        col10.info("Insight: Menu item distribution shows cuisines with the highest menu variety.")

        col11, col12 = st.columns(2)

        price_range_distribution = (
            filtered_menu_df.groupby("PRICE_RANGE")["MENU_ID"]
            .nunique()
            .reset_index()
        )

        fig11 = px.pie(
            price_range_distribution,
            names="PRICE_RANGE",
            values="MENU_ID",
            hole=0.45,
            title="Price Range Distribution"
        )

        col11.plotly_chart(fig11, width="stretch")
        col11.info("Insight: Price range distribution explains whether the platform is budget-heavy or premium-focused.")

        expensive_items = (
            filtered_menu_full_df.groupby("ITEM")["PRICE"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig12 = px.bar(
            expensive_items,
            x="PRICE",
            y="ITEM",
            orientation="h",
            title="Top Expensive Menu Items",
            text_auto=".2s"
        )
        fig12.update_layout(yaxis={"categoryorder": "total ascending"})

        col12.plotly_chart(fig12, width="stretch")
        col12.info("Insight: Expensive menu items reveal premium pricing opportunities.")


with tab3:
    st.header("🤖 High Revenue Restaurant Prediction System")

    st.write(
        "This system predicts whether a restaurant has high revenue potential "
        "based on business planning features such as city, cuisine, cost, menu price, "
        "menu variety, and cuisine diversity."
    )

    st.info(
        "Note: The model uses Top 40 trained cities and cuisines. Any city or cuisine outside these categories is treated as 'Other'. Prediction still depends on cost, average menu price, menu variety, and unique cuisine count, so the model can predict both high and low revenue potential."
    )

    col1, col2 = st.columns(2)

    with col1:
        city_input = st.selectbox(
            "Select City",
            sorted(list(top_cities)) + ["Other"]
        )

        cuisine_input = st.selectbox(
            "Select Cuisine",
            sorted(list(top_cuisines)) + ["Other"]
        )

        cost_input = st.number_input(
            "Restaurant Cost",
            min_value=0.0,
            value=500.0
        )

    with col2:
        avg_menu_price_input = st.number_input(
            "Average Menu Price",
            min_value=0.0,
            value=200.0
        )

        menu_variety_input = st.number_input(
            "Menu Variety",
            min_value=0,
            value=50
        )

        unique_cuisine_count_input = st.number_input(
            "Unique Cuisine Count",
            min_value=1,
            value=2
        )

    if st.button("Predict Restaurant Revenue Potential"):
        with st.spinner("Generating prediction..."):
            city_value = city_input if city_input in top_cities else "Other"
            cuisine_value = cuisine_input if cuisine_input in top_cuisines else "Other"

            input_data = pd.DataFrame({
                "COST": [cost_input],
                "AVG_MENU_PRICE": [avg_menu_price_input],
                "MENU_VARIETY": [menu_variety_input],
                "UNIQUE_CUISINE_COUNT": [unique_cuisine_count_input],
                "CITY": [city_value],
                "CUISINE": [cuisine_value]
            })

            input_encoded = pd.get_dummies(
                input_data,
                columns=["CITY", "CUISINE"],
                drop_first=True
            )

            input_encoded = input_encoded.reindex(
                columns=model_features,
                fill_value=0
            )

            input_scaled = scaler.transform(input_encoded)

            prediction = model.predict(input_scaled)[0]
            prediction_probability = model.predict_proba(input_scaled)[0][1]

        st.divider()

        if prediction == 1:
            st.success("✅ High Revenue Potential Restaurant")
            st.metric(
                "High Revenue Probability",
                f"{prediction_probability * 100:.2f}%"
            )

            st.subheader("📈 Business Recommendation")

            st.write(
                "This restaurant profile shows strong potential based on pricing, "
                "menu diversity, cuisine positioning, and market demand."
            )

            st.success(
                "Recommendation: Focus on expansion, premium menu offerings, "
                "and customer retention strategies."
            )
        else:
            st.warning("⚠️ Low Revenue Potential Restaurant")
            st.metric(
                "High Revenue Probability",
                f"{prediction_probability * 100:.2f}%"
            )

            st.subheader("📉 Business Recommendation")

            st.write(
                "This restaurant profile may require improvements in pricing strategy, "
                "menu diversification, or cuisine positioning."
            )

            st.warning(
                "Recommendation: Improve menu variety, optimize pricing, "
                "and target stronger market segments."
            )

st.divider()
st.caption(
    "Developed by Yatesh Kumar | Food Delivery Analytics Project | Streamlit Web Application"
)