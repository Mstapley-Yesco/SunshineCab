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

    best_fit = None  # Stores the best (largest) fit found

    # Iterate over digit sizes, starting from the LARGEST
    for digit_size, (min_width, max_width, min_height, max_height) in sorted(adjusted_digit_ranges.items(), key=lambda x: -x[0]):
        sunshine_width_ft = max_width / 12
        sunshine_height_ft = max_height / 12  # Adjusted for 4 price changers if needed

        # Calculate Maverik Cabinet dimensions
        if separate_cabinets:
            maverik_width_ft = sunshine_width_ft * (13 / 11)  # Adjust Maverik Cabinet width based on the 13:11 ratio
        else:
            maverik_width_ft = sunshine_width_ft  # Maverik Cabinet width matches Sunshine Cabinet width
        
        maverik_height_ft = maverik_width_ft * maverik_height_ratio
        maverik_sq_ft = maverik_width_ft * maverik_height_ft

        # Calculate Sunshine Cabinet square footage
        sunshine_sq_ft = sunshine_width_ft * sunshine_height_ft

        # Total square footage without the Bonfire Cabinet
        total_sq_ft = maverik_sq_ft + sunshine_sq_ft

        # Calculate Bonfire Cabinet dimensions if included
        bonfire_width_ft = sunshine_width_ft
        bonfire_height_ft = 0
        bonfire_sq_ft = 0
        if include_third_cabinet:
            if total_sq_ft + (bonfire_width_ft * (30 / 12)) <= allowed_sq_ft:
                bonfire_height_ft = 30 / 12
                bonfire_sq_ft = bonfire_width_ft * bonfire_height_ft
            elif total_sq_ft + (bonfire_width_ft * (18 / 12)) <= allowed_sq_ft:
                bonfire_height_ft = 18 / 12
                bonfire_sq_ft = bonfire_width_ft * bonfire_height_ft
            else:
                continue  # Move to the next (smaller) digit size

        # Update total square footage with Bonfire Cabinet
        total_sq_ft += bonfire_sq_ft
        leftover_sq_ft = allowed_sq_ft - total_sq_ft

        # Debug print statements to track the issue
        print(f"Checking digit size: {digit_size}\"")
        print(f"Sunshine Cabinet: {max_width}\" x {max_height}\" ({sunshine_sq_ft:.2f} sq ft)")
        print(f"Maverik Cabinet: {maverik_width_ft * 12}\" x {maverik_height_ft * 12}\" ({maverik_sq_ft:.2f} sq ft)")
        print(f"Total Sq Ft Used: {total_sq_ft:.2f} (Allowed: {allowed_sq_ft})\n")

        # If this configuration fits, store it as the best fit if it is the largest found so far
        if total_sq_ft <= allowed_sq_ft:
            if best_fit is None or digit_size > best_fit["digit_size"]:
                best_fit = {
                    "digit_size": digit_size,
                    "sunshine_width": max_width,
                    "sunshine_height": max_height,
                    "maverik_width": maverik_width_ft * 12,
                    "maverik_height": maverik_height_ft * 12,
                    "bonfire_width": bonfire_width_ft * 12,
                    "bonfire_height": bonfire_height_ft * 12 if bonfire_height_ft > 0 else "Not Added",
                    "total_sq_ft_used": total_sq_ft,
                    "leftover_sq_ft": leftover_sq_ft
                }

    return best_fit  # Return the LARGEST valid configuration found

# Define digit ranges
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
    114: (540, 600, 156, 167),
}

# Streamlit App
st.title("Sunshine Cabinet Calculator")

allowed_sq_ft = st.number_input("Enter the allowed square footage (in feet):", min_value=1.0, step=1.0)
price_changer_type = st.radio("Select Price Changer Type:", ["2", "4"])
include_third_cabinet = st.checkbox("Add Bonfire, Trucks & RV Cabinet")
separate_cabinets = st.checkbox("Separate Cabinets")

if st.button("Calculate"):
    result = calculate_cabinet_and_digits(
        allowed_sq_ft, digit_ranges, price_changer_type=price_changer_type, include_third_cabinet=include_third_cabinet, separate_cabinets=separate_cabinets
    )
    
    if result:
        st.success(f"**Largest Configuration Found:**")
        st.write(f"Digit Size: **{result['digit_size']}\"**")
        st.write(f"Total Square Footage Used: **{result['total_sq_ft_used']} sq ft**")
        st.write(f"Leftover Square Footage: **{result['leftover_sq_ft']} sq ft**")
    else:
        st.error("No feasible cabinet size found within the constraints.")
