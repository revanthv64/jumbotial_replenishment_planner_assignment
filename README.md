# Replenishment Planner
## Overview
# This project is a SKU-level inventory replenishment planner that determines how much of each SKU should be ordered based on demand, current inventory, incoming purchase orders, inventory norms, safety stock, vendor lead time, case size, and minimum order value (MOV).
## 1. How to Run

The solution is implemented as a Google Colab notebook using Python, Pandas, NumPy, and SQLite.

### Steps

1. Open `Jumbotail_assignment.ipynb` in Google Colab.
2. Upload `assignment_data.csv` when prompted.
3. Run the notebook cells from top to bottom.
4. The notebook:

   * Loads and validates the input data.
   * Parses the JSON inventory and PO fields.
   * Calculates inventory position, target coverage, and raw replenishment.
   * Applies case-size and MOV constraints.
   * Calculates final PO quantity, value, tonnage, DOI, and MOV checks.
   * Writes the processed data to `replenishment_output.csv`.
   * Creates a SQLite database `replenishment.db` containing the replenishment data.

The notebook expects `assignment_data.csv` to be available at `/content/assignment_data.csv`. The input used during development contained 1,389 rows and 36 columns.

---

## 2. Key Assumptions

### Inventory Target

I interpreted the inventory target as:

`Target Days = MAX(Inventory Norm, Vendor Lead Time) + Safety Stock`

and:

`Target Units = Target Days × Max DRR`

This ensures the target covers the larger of the required inventory norm or vendor lead time, with safety stock added on top.

### Inventory Position

Inventory position is calculated as:

`Current Inventory + Ordered Quantity`

Open/ordered supply is therefore considered before generating an additional PO suggestion.

### Raw Replenishment

Raw replenishment is:

`MAX(0, Target Units - Inventory Position)`

This prevents negative PO suggestions.

### Case and MOV Constraints

The final suggestion is converted into cases and constrained by:

* Vendor minimum order value (MOV).
* Maximum order cases.
* Case size.

The final unit suggestion is then:

`Final Suggestion = Final Cases × Case Size`

SKUs with zero demand are explicitly assigned zero replenishment.

### PO Value

PO value is calculated using cost price:

`Final Value = Final Suggestion × CP`

### Missing Numeric Values

Numeric fields are converted using `to_numeric(..., errors="coerce")`, with invalid or missing values treated as zero. This was chosen to make the planner robust to null or malformed numeric inputs.

---

## 3. Where AI Helped

AI was used primarily as a development and reasoning aid rather than as the source of the final business logic.

It helped with:

* Translating the replenishment requirements into Python calculations.
* Structuring the planner into separate, testable calculation steps.
* Handling JSON fields such as `inventory_breakup` and `open_po_details`.
* Debugging Python/Colab issues and iterating on the implementation.
* Designing the SQLite layer and useful SQL queries.
* Thinking through inventory-health, prioritization, MOV, and replenishment logic.

The final formulas and outputs were not accepted blindly. I manually reviewed the calculation flow and checked intermediate values such as inventory position, target units, raw replenishment, final cases, final units, and PO value.

## For example, the notebook explicitly validates required columns before processing and validates the parsed JSON fields before continuing.

## 4. What I Verified Manually

I manually checked:

* Input row and column counts.
* Presence of required fields.
* JSON parsing and handling of empty JSON values.
* Current DOI calculation.
* Inventory position calculation.
* Target coverage logic.
* Raw replenishment calculation.
* Case-size conversion.
* MOV constraints.
* Zero-demand SKU handling.
* Final PO quantity and PO value.
* SQLite table creation and row loading.

The notebook also performs validation after loading the processed data into SQLite.

---

## 5. What I Would Improve With More Time

1. **More sophisticated inventory health**

   * Add explicit overstock, understock, stockout, and healthy-stock classifications.
   * Incorporate projected DOI and lead-time risk more directly.

2. **Sales-band prioritization**

   * Use sales bands as an explicit prioritization layer so scarce purchasing capacity is allocated to higher-priority SKUs first.

3. **Better PO modelling**

   * Model individual open POs by promise date instead of relying primarily on aggregated ordered quantities.
   * Distinguish POs arriving within lead time from later POs.

4. **Capacity constraints**

   * Add facility/vendor-level constraints and optimize allocation when total required purchasing exceeds available capacity.

5. **Forecast quality**

   * Replace the current DRR-based approach with a more robust demand forecast incorporating seasonality, trends, and demand variability.

6. **Testing**

   * Add automated unit tests for edge cases such as zero DRR, missing values, very large MOV requirements, insufficient capacity, and conflicting constraints.

7. **Productionization**

   * Move the notebook logic into modular Python files
  
8. **Dashboard**
   * make a better streamlit dashboard for operational use

Overall, the current solution prioritizes **clarity, traceability, and a deterministic replenishment calculation** while leaving room for more advanced optimization and forecasting.
