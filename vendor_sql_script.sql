SELECT
    vendor_id,
    vendor_name,

    COUNT(DISTINCT jpin) AS sku_count,

    SUM(
        CASE
            WHEN final_suggestion > 0
            THEN 1
            ELSE 0
        END
    ) AS skus_requiring_replenishment,

    SUM(final_suggestion) AS total_suggested_units,

    SUM(final_cases_suggestion) AS total_suggested_cases,

    ROUND(
        SUM(final_value),
        2
    ) AS total_suggested_value,

    ROUND(
        SUM(final_tonnage),
        3
    ) AS total_suggested_tonnage,

    SUM(
        CASE
            WHEN mov_check = 'PASS'
            THEN 1
            ELSE 0
        END
    ) AS mov_pass_count,

    SUM(
        CASE
            WHEN mov_check = 'FAIL'
            THEN 1
            ELSE 0
        END
    ) AS mov_fail_count

FROM final_replenishment_data

GROUP BY
    vendor_id,
    vendor_name

ORDER BY
    total_suggested_value DESC;
"""