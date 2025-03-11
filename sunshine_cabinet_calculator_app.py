import streamlit as st

def calculate_cabinet_and_digits(
    allowed_sq_ft, digit_ranges, maverik_height_ratio=0.5, price_changer_type="2", include_third_cabinet=False, separate_cabinets=False
):
    # Adjust digit ranges based on Price Changer type
    adjusted_digit_ranges = {}
    for digit_size, (min_width, max_width, min_height, max_height) in digit_ranges.items():
        if price_changer_type == "4":
            adjusted_digit_ranges[digit_size] = (min_width, max_width, min_height * 2, max_height * 2)
        else:
            adjusted_digit_ranges[digit_size] = (min_width, max_width, min_height, max_height)

    # Iterate over digit sizes, starting from the largest
    best_config = None
    for digit_size in sorted(adjusted_digit_ranges.keys(), reverse=True):  # Start from the largest digit
        min_width, max_width, min_height, max_height = adjusted_digit_ranges[digit_size]

        # Instead of starting with the largest cabinet size, start with the smallest
        for width in [min_width, max_width]:  # Test smaller first
            for height in [min_height, max_height]:  # Test smaller first
                sunshine_width_ft = width / 12
                sunshine_height_ft = height / 12

                # Calculate Maverik Cabinet dimensions
                if separate_cabinets:
                    maverik_width_ft = sunshine_width_ft * (13 / 11)  # Adjust for separate cabinet ratio
                else:
                    maverik_width_ft = sunshine_width_ft
                
                maverik_height_ft = maverik_width_ft * maverik_height_ratio
                maverik_sq_ft = maverik_width_ft * maverik_height_ft

                # Calculate Sunshine Cabinet square footage
                sunshine_sq_ft = sunshine_width_ft * sunshine_height_ft

                # Start with only Maverik and Sunshine Cabinets
                total_sq_ft = maverik_sq_ft + sunshine_sq_ft
                bonfire_height_ft = 0
                bonfire_sq_ft = 0

                # If Bonfire Cabinet is included, check if it fits
                if include_third_cabinet:
                    bonfire_width_ft = sunshine_width_ft
                    if total_sq_ft + (bonfire_width_ft * (30 / 12)) <= allowed_sq_ft:
                        bonfire_height_ft = 30 / 12
                        bonfire_sq_ft = bonfire_width_ft * bonfire_height_ft
                    elif total_sq_ft + (bonfire_width_ft * (18 / 12)) <= allowed_sq_ft:
                        bonfire_height_ft = 18 / 12
                        bonfire_sq_ft = bonfire_width_ft * bonfire_height_ft
                
                # Update total square footage
                total_sq_ft += bonfire_sq_ft
                leftover_sq_ft = allowed_sq_ft - total_sq_ft

                # If this configuration fits, update the best configuration found
                if total_sq_ft <= allowed_sq_ft:
                    best_config = {
                        "digit_size": digit_size,
                        "sunshine_width": width,
                        "sunshine_height": height,
                        "maverik_width": maverik_width_ft * 12,  # Convert back to inches
                        "maverik_height": maverik_height_ft * 12,
                        "bonfire_width": sunshine_width_ft * 12,
                        "bonfire_height": bonfire_height_ft * 12 if bonfire_height_ft > 0 else "Not Added",
                        "total_sq_ft_used": total_sq_ft,
                        "leftover_sq_ft": leftover_sq_ft
                    }
                    break  # Stop checking once a valid configuration is found for this digit size
            if best_config:
                break  # Stop checking once a valid configuration is found for this digit size

        if best_config:
            break  # Stop checking once we find the largest possible digit size

    return best_config

# Define digit ranges: (min_width, max_width, min_height, max_height) in inches
digit_ranges = {
    10: (56, 60, 22, 24),
    13: (72, 78, 27, 29),
    16: (83, 90, 30, 32),
    20: (102, 108, 35, 38),
    24: (108, 126, 42, 44),
    28: (126, 144, 47, 51),
    32: (144, 170, 52, 56),
    36: (196, 222, 64, 64),
    40: (207, 232, 66, 72),
    48: (252, 288, 77, 84),
    61: (316, 364, 94, 105),
    76: (368, 416, 111, 123),
    89: (460, 512, 130, 138),
    114: (540, 600, 156, 167),  # Largest possible cabinet size
}

# Streamlit App
st.title("Sunshine Cabinet Calculator")
st.write("Find the largest cabinet configuration within the allowed square footage.")

# User Input
allowed_sq_ft = st.number_input("Enter the allowed square footage (in feet):", min_value=1.0, step=1.0)
price_changer_type = st.radio("Select Price Changer Type:", ["2", "4"])
include_third_cabinet = st.checkbox("Add Bonfire, Trucks & RV Cabinet")
separate_cabinets = st.checkbox("Separate Cabinets")

# Calculate when user clicks the button
if st.button("Calculate"):
    result = calculate_cabinet_and_digits(
        allowed_sq_ft, digit_ranges, price_changer_type=price_changer_type, include_third_cabinet=include_third_cabinet, separate_cabinets=separate_cabinets
    )
    
    if result:
        st.success(f"**Largest Configuration Found:**")
        st.write(f"Digit Size: **{result['digit_size']}\"**")
        st.write(f"Sunshine Cabinet: **{result['sunshine_width']}\" wide**, **{result['sunshine_height']}\" tall**")
        st.write(f"Maverik Cabinet: **{result['maverik_width']}\" wide**, **{result['maverik_height']}\" tall**")
        if include_third_cabinet:
            st.write(f"Bonfire, Trucks & RV Cabinet: **{result['bonfire_width']}\" wide**, **{result['bonfire_height']}\" tall**")
        st.write(f"Total Square Footage Used: **{result['total_sq_ft_used']} sq ft**")
        st.write(f"Leftover Square Footage: **{result['leftover_sq_ft']} sq ft**")
    else:
        st.error("No feasible cabinet size found within the constraints.")
