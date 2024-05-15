import streamlit as st

categories = {
    "Agriculture": [],
    "Energy and Power": [],
    "Chemicals": [],
    "Information and Communications Technology":[],
    "Manufacturing and Industrial": [
        "Aerospace",
        "Biopharmaceuticals Manufacturing",
        "Electronics",
        "Food Manufacturing",
        "Marine and Offshore Engineering",
        "Precision Engineering"
    ],
    "Built Environment": [
        "Architecture",
        "Construction",
        "Building services and Facility Management",
        "Landscaping"
    ],
    "Transport and Logistics": [
        "Air Transport",
        "Public Transport",
        "Sea Transport",
        "Logistics"
    ],
    "Business Services": [
        "Accountancy",
        "Advertising",
        "Consultancy",
        "Legal",
        "Human Resource",
        "Insurance",
        "Environmental Services",
        "Wholesale Trade"
    ],
    "Healthcare and Social Services": [
        "Healthcare",
        "Social Services",
        "Beauty Services"
    ],
    "Hospitality and Tourism": [
        "Hotel and Accommodation Services",
        "Tourism"
    ],
    "Food Services": [],
    "Education & Training": [
        "Early Childhood Care and Education",
        "Training and Adult Education"
    ],
    "Creative and Media": [
        "Arts, Entertainment and Recreation",
        "Design",
        "Media"
    ],
    "Retail and Real Estate": [
        "E-commerce",
        "Real Estate",
        "Consumer Retail",
        "Wholesale Trade"
    ],
}

def industry_selector():
    st.caption("Industry")
    cols = st.columns(3)
    selected_category = None  # Initialize selected_category
    # Loop through categories to check if any checkbox is selected
    any_selected = any(st.session_state.get(category) for category in categories.keys())

    for i, category in enumerate(categories.keys()):
        with cols[i % 3]:
            is_checked = st.session_state.get(category, False)
            if st.checkbox(
                category, 
                key=category, 
                value=is_checked, 
                disabled=False if not any_selected or is_checked else (category != st.session_state.selected_category)
            ):
                st.session_state.selected_category = category
                selected_category = category
            else:
                if is_checked:  # If a checkbox is unchecked, reset the selected category
                    del st.session_state.selected_category

    industry = ""
    if selected_category:
        # Get the industries for the selected category
        if len(categories[selected_category]) > 1:
            industries_options = categories[selected_category]
            industry = st.selectbox("Select a sub-industry", industries_options)
        else:
            industry = st.text_input("Enter the industry or short description of the company's goods/services", selected_category)

    else:
        industry = st.text_input("Enter the industry or short description of the company's goods/services", "")
    return industry