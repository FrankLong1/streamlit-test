import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(
    page_title="Global Trade Routes & Tariff Impact",
    page_icon="🌍",
    layout="wide"
)

# Title and description
st.title("🌍 Global Trade Routes & Tariff Impact")
st.markdown("""
This interactive map visualizes major trade routes around the world and their relationship with tariffs.
Hover over routes to see detailed information about trade volume and tariff impacts.
""")

# Sample data - in a real app, this would come from a database or API
def create_sample_data():
    # Sample trade routes with origin, destination, and tariff impact
    routes = [
        {"origin": "USA", "dest": "China", "volume": 100, "tariff_impact": 0.25},
        {"origin": "Germany", "dest": "USA", "volume": 80, "tariff_impact": 0.15},
        {"origin": "Japan", "dest": "USA", "volume": 70, "tariff_impact": 0.20},
        {"origin": "China", "dest": "Germany", "volume": 90, "tariff_impact": 0.10},
        {"origin": "Brazil", "dest": "China", "volume": 60, "tariff_impact": 0.30},
        {"origin": "India", "dest": "USA", "volume": 50, "tariff_impact": 0.18},
        {"origin": "UK", "dest": "USA", "volume": 65, "volume": 65, "tariff_impact": 0.12},
        {"origin": "Australia", "dest": "China", "volume": 45, "tariff_impact": 0.22},
    ]
    return pd.DataFrame(routes)

# Create the map
def create_trade_map(df):
    fig = go.Figure()

    # Add trade routes
    for _, row in df.iterrows():
        fig.add_trace(go.Scattergeo(
            lon=[0, 0],  # Will be updated with actual coordinates
            lat=[0, 0],  # Will be updated with actual coordinates
            mode='lines',
            line=dict(
                width=row['volume']/20,  # Line width based on trade volume
                color=f'rgba(255, 0, 0, {row["tariff_impact"]})',  # Color intensity based on tariff impact
            ),
            name=f"{row['origin']} → {row['dest']}",
            hoverinfo='text',
            text=f"Route: {row['origin']} → {row['dest']}<br>" +
                 f"Trade Volume: {row['volume']}B USD<br>" +
                 f"Tariff Impact: {row['tariff_impact']*100}%"
        ))

    # Update layout
    fig.update_layout(
        title='Global Trade Routes and Tariff Impact',
        geo=dict(
            showland=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
            showcountries=True,
            projection_type='natural earth'
        ),
        height=800,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    return fig

# Create sidebar filters
st.sidebar.header("Filters")
min_volume = st.sidebar.slider("Minimum Trade Volume (B USD)", 0, 100, 0)
max_tariff = st.sidebar.slider("Maximum Tariff Impact (%)", 0, 100, 100) / 100

# Load and filter data
df = create_sample_data()
filtered_df = df[
    (df['volume'] >= min_volume) &
    (df['tariff_impact'] <= max_tariff)
]

# Display the map
st.plotly_chart(create_trade_map(filtered_df), use_container_width=True)

# Add some statistics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Routes Displayed", len(filtered_df))
with col2:
    st.metric("Average Trade Volume", f"${filtered_df['volume'].mean():.1f}B")
with col3:
    st.metric("Average Tariff Impact", f"{filtered_df['tariff_impact'].mean()*100:.1f}%")

# Add explanation
st.markdown("""
### How to Interpret the Map
- **Line Width**: Represents trade volume (thicker lines = higher volume)
- **Line Color**: Represents tariff impact (darker red = higher tariffs)
- **Hover**: Mouse over routes to see detailed information
""") 