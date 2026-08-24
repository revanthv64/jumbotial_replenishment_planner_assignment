SELECT
    facility_name,
    jpin,
    title,
    current_inventory,
    max_drr,
    current_days_raw,
    target_days,
    inventory_position,
    projected_inventory
FROM final_replenishment_data
WHERE current_inventory <= 0
ORDER BY max_drr DESC
LIMIT 10;