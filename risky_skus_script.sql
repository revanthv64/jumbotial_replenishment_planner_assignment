SELECT
    facility_id,
    facility_name,

    vendor_id,
    vendor_name,

    jpin,
    title,

    max_drr,
    current_inventory,

    ROUND(
        CAST(current_inventory AS REAL)
        / NULLIF(max_drr, 0),
        2
    ) AS current_days_of_inventory,

    inv_norm,
    safety_stock,

    final_suggestion,
    final_days_of_inventory,

    inventory_priority

FROM replenishment_data

WHERE
    max_drr > 0

ORDER BY
    current_days_of_inventory ASC

LIMIT 10
    