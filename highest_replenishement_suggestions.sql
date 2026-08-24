SELECT
    facility_name,
    jpin,
    title,
    max_drr,
    current_inventory,
    inventory_position,
    target_units,
    raw_replenishment,
    desired_cases,
    final_cases_suggestion,
    final_value
FROM final_replenishment_data
WHERE final_suggestion > 0
ORDER BY final_value DESC
LIMIT 10;