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

# Calculate for 130 square feet with price changer type "4"
optimal_result = calculate_optimal_cabinet_size(130, digit_ranges, price_changer_type="4")

optimal_result
