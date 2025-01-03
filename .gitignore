import streamlit as st

def calculate_cabinet_and_digits(allowed_sq_ft, digit_ranges, maverik_height_ratio=0.5, price_changer_type="2"):
    # Adjust digit ranges based on Price Changer type
    adjusted_digit_ranges = {}
    for digit_size, (min_width, max_width, min_height, max_height) in digit_ranges.items():
        if price_changer_type == "4":
            adjusted_digit_ranges[digit_size] = (min_width, max_width, min_height * 2, max_height * 2)
        else:
            adjusted_digit_ranges[digit_size] = (min_width, max_width, min_height, max_height)
    
    # Iterate over digit sizes, starting from the largest
    for digit_size, (min_width, max_width, min_height, max_height) in sorted(adjusted_digit_ranges.items(), key=lambda x: -x[0]):
        max_width_ft = max_width / 12
        max_height_ft = max_height / 12

        # Calculate Maverik Cabinet dimensions
        maverik_height_ft = max_width_ft * maverik_height_ratio
        maverik_sq_ft = max_width_ft * maverik_height_ft

        # Calculate Sunshine Cabinet square footage
        sunshine_sq_ft = max_width_ft * max_height_ft

        # Total square footage
        total_sq_ft = maverik_sq_ft + sunshine_sq_ft
        leftover_sq_ft = allowed_sq_ft - total_sq_ft

        # Check if it fits within allowed square footage
        if total_sq_ft <= allowed_sq_ft:
            return {
                "digit_size": digit_size,
                "sunshine_width": max_width,
                "sunshine_height": max_height,
                "maverik_width": max_width,
                "maverik_height": maverik_height_ft * 12,
                "total_sq_ft_used": total_sq_ft,
                "leftover_sq_ft": leftover_sq_ft
            }
    
    # If no feasible configuration is found
    return None

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

# Calculate when user clicks the button
if st.button("Calculate"):
    result = calculate_cabinet_and_digits(allowed_sq_ft, digit_ranges, price_changer_type=price_changer_type)
    
    if result:
        st.success(f"**Largest Configuration Found:**")
        st.write(f"Digit Size: **{result['digit_size']}\"**")
        st.write(f"Sunshine Cabinet: **{result['sunshine_width']}\" wide**, **{result['sunshine_height']}\" tall**")
        st.write(f"Maverik Cabinet: **{result['maverik_width']}\" wide**, **{result['maverik_height']}\" tall**")
        st.write(f"Total Square Footage Used: **{result['total_sq_ft_used']} sq ft**")
        st.write(f"Leftover Square Footage: **{result['leftover_sq_ft']} sq ft**")
    else:
        st.error("No feasible cabinet size found within the constraints.")
