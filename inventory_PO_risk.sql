SELECT
    facility_name,
    jpin,
    title,
    current_inventory,
    current_days_raw,
    max_drr,
    open_po_cases,
    open_po_value,
    earliest_promise_date,
    projected_inventory
FROM final_replenishment_data
WHERE max_drr > 0
  AND current_days_raw < target_days
  AND open_po_cases > 0
ORDER BY current_days_raw ASC
LIMIT 10;