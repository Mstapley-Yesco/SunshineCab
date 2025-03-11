import streamlit as st

def calculate_optimal_cabinet_size(
    allowed_sq_ft, digit_ranges, maverik_height_ratio=0.5, price_changer_type="4", include_third_cabinet=False, separate_cabinets=False
):
    # Adjust digit ranges based on Price Changer type (double height for type 4)
    adjusted_digit_ranges = {}
    for digit_size, (min_width, max_width, min_height, max_height) in digit_ranges.items():
        if price_changer_type == "4":
            adjusted_digit_ranges[digit_size] = (min_width, max_width, min_height * 2, max_height * 2)
        else:
            adjusted_digit_ranges[digit_size] = (min_width, max_width, min_height, max_height)

    best_config = None
    min_leftover_sq_ft = float('inf')  # Track the smallest leftover square footage

    for digit_size in sorted(adjusted_digit_ranges.keys(), reverse=True):  # Start from the largest digit
        min_width, max_width, min_height, max_height = adjusted_digit_ranges[digit_size]

        # Try all possible cabinet sizes within the given range
        for width in range(min_width, max_width + 1, 1):  
            for height in range(min_height, max_height + 1, 1):  
                sunshine_width_ft = width / 12
                sunshine_height_ft = height / 12

                if separate_cabinets:
                    maverik_width_ft = sunshine_width_ft * (13 / 11)  
                else:
                    maverik_width_ft = sunshine_width_ft
                
                maverik_height_ft = maverik_width_ft * maverik_height_ratio
                maverik_sq_ft = maverik_width_ft * maverik_height_ft

                sunshine_sq_ft = sunshine_width_ft * sunshine_height_ft

                total_sq_ft = maverik_sq_ft + sunshine_sq_ft
                bonfire_height_ft = 0
                bonfire_sq_ft = 0

                if include_third_cabinet:
                    bonfire_width_ft = sunshine_width_ft
                    if total_sq_ft + (bonfire_width_ft * (30 / 12)) <= allowed_sq_ft:
                        bonfire_height_ft = 30 / 12
                        bonfire_sq_ft = bonfire_width_ft * bonfire_height_ft
                    elif total_sq_ft + (bonfire_width_ft * (18 / 12)) <= allowed_sq_ft:
                        bonfire_height_ft = 18 / 12
                        bonfire_sq_ft = bonfire_width_ft * bonfire_height_ft
                
                total_sq_ft += bonfire_sq_ft
                leftover_sq_ft = allowed_sq_ft - total_sq_ft

                # Ensure it's within the allowed space and minimizes leftover space
                if total_sq_ft <= allowed_sq_ft and leftover_sq_ft < min_leftover_sq_ft:
                    min_leftover_sq_ft = leftover_sq_ft
                    best_config = {
                        "digit_size": digit_size,
                        "sunshine_width": width,
                        "sunshine_height": height,
                        "maverik_width": maverik_width_ft * 12,  # Convert back to inches
                        "maverik_height": maverik_height_ft * 12,
                        "total_sq_ft_used": total_sq_ft,
                        "leftover_sq_ft": leftover_sq_ft
                    }

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
    result = calculate_optimal_cabinet_size(
        allowed_sq_ft, digit_ranges, price_changer_type=price_changer_type, include_third_cabinet=include_third_cabinet, separate_cabinets=separate_cabinets
    )
    
    if result:
        st.success(f"**Largest Configuration Found:**")
        st.write(f"Digit Size: **{result['digit_size']}\"**")
        st.write(f"Sunshine Cabinet: **{result['sunshine_width']}\" wide**, **{result['sunshine_height']}\" tall**")
        st.write(f"Maverik Cabinet: **{result['maverik_width']}\" wide**, **{result['maverik_height']}\" tall**")
        st.write(f"Total Square Footage Used: **{result['total_sq_ft_used']} sq ft**")
        st.write(f"Leftover Square Footage: **{result['leftover_sq_ft']} sq ft**")
    else:
        st.error("No feasible cabinet size found within the constraints.")
