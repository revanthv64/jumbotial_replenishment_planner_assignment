# jumbotial_replenishment_planner_assignment
# Replenishment Planner

## 1. Overview

This project builds a SKU-level **Replenishment Planner** for a fulfillment center.

The planner takes inventory, demand, supplier, MOQ/MOV, and lead-time data as inputs and generates **purchase order (PO) suggestions** for each SKU.

The objective is to determine:

* Whether a SKU requires replenishment
* The recommended replenishment quantity
* Whether the suggested order meets vendor MOQ/MOV requirements
* The final PO suggestion after applying business rules
* Supporting flags and calculations for operational decision-making

The solution also loads the base data and planner outputs into a **SQLite database** for structured querying and future analysis.

---

## 2. Project Structure

```text
Replenishment Planner
│
├── assignment_data.csv
├── replenishment_planner.ipynb
├── replenishment_output.csv
├── replenishment.db
└── README.md
```

### Files

| File                          | Description                                            |
| ----------------------------- | ------------------------------------------------------ |
| `assignment_data.csv`         | Input dataset provided for the assignment              |
| `replenishment_planner.ipynb` | Google Colab notebook containing the complete solution |
| `replenishment_output.csv`    | Final SKU-level replenishment recommendations          |
| `replenishment.db`            | SQLite database containing the input/output data       |
| `README.md`                   | Project documentation                                  |

---

## 3. Technology Stack

* **Python**
* **Pandas** – data processing and transformation
* **NumPy** – numerical calculations
* **SQLite** – database storage and querying
* **Google Colab** – execution environment

---

## 4. Input Data

The planner uses `assignment_data.csv` as its primary input.

The dataset contains SKU-level information related to:

* Inventory position
* Demand / consumption
* Lead time
* Supplier information
* Minimum Order Quantity (MOQ)
* Minimum Order Value (MOV)
* Vendor ordering criteria
* Other replenishment-related attributes

The notebook automatically reads the uploaded CSV and validates the required input.

---

## 5. Replenishment Logic

The planner follows a sequence of business rules to calculate the recommended purchase quantity.

### Step 1 — Calculate Inventory Position

The available inventory position is evaluated using the inventory and supply-related fields provided in the dataset.

### Step 2 — Determine Replenishment Requirement

The planner identifies SKUs where the expected inventory position is insufficient to cover the required demand/safety requirement.

SKUs that do not require replenishment receive a final suggestion of `0`.

### Step 3 — Calculate Initial Replenishment Quantity

For SKUs requiring replenishment, the system calculates the quantity required to restore inventory to the required level.

### Step 4 — Apply Vendor MOQ

Where applicable, the suggested quantity is adjusted to satisfy the vendor's **Minimum Order Quantity (MOQ)**.

### Step 5 — Validate Vendor MOV

Where the vendor's minimum ordering criterion is based on **Minimum Order Value (MOV)**, the planner checks whether the proposed order value meets the required threshold.

The planner identifies whether the order:

* `PASS` – satisfies the requirement
* `FAIL` – does not satisfy the requirement
* `N/A` – no replenishment is required

### Step 6 — Generate Final Suggestion

The final PO suggestion incorporates the replenishment requirement and applicable vendor constraints.

The resulting quantity is stored in the output as the **final replenishment suggestion**.

---

## 6. Output

The planner generates a CSV containing the original SKU-level information along with the calculated replenishment fields.

Key output fields include:

* Replenishment requirement
* Initial suggestion
* Final suggestion
* MOQ adjustment
* MOV validation
* Replenishment / ordering flags
* Other supporting calculations

The output is designed to allow an operations or supply-chain user to quickly identify **which SKUs need to be ordered and how much should be ordered**.

---

## 7. SQLite Database

The solution also creates a SQLite database:

```text
replenishment.db
```

The database provides a structured way to store and query the planner data.

Typical use cases include:

* Querying SKU-level recommendations
* Filtering SKUs requiring replenishment
* Analysing vendor-level requirements
* Validating planner calculations
* Supporting future dashboards or applications

Example SQL query:

```sql
SELECT *
FROM replenishment_output
WHERE final_suggestion > 0;
```

This returns all SKUs for which a purchase order is recommended.

---

## 8. Running the Solution

### Google Colab

1. Open the `replenishment_planner.ipynb` notebook in Google Colab.
2. Run the notebook from top to bottom.
3. When prompted, upload:

```text
assignment_data.csv
```

4. The notebook processes the input data.
5. The final output is generated as:

```text
replenishment_output.csv
```

6. The SQLite database is generated as:

```text
replenishment.db
```

---

## 9. Key Design Principles

The solution was designed with the following principles:

### Automation

The complete replenishment calculation is automated using Python rather than manually calculating PO quantities.

### Traceability

Intermediate calculations and flags are retained so that the final recommendation can be understood and validated.

### Business-rule driven

The planner explicitly incorporates vendor constraints such as MOQ and MOV rather than relying only on inventory levels.

### Data validation

Input data is cleaned and validated before calculations are performed to reduce errors caused by missing or inconsistent values.

### Extensibility

The logic is implemented using reusable functions so that additional replenishment rules can be added without redesigning the entire solution.

### Database-ready

The solution stores the processed data in SQLite, making it possible to extend the planner into a larger analytics or operational application.

---

## 10. Assumptions

The following assumptions are made where business rules or required fields are not explicitly defined:

1. Input values are interpreted according to their corresponding column definitions.
2. Missing numerical values are handled using predefined data-cleaning rules.
3. A SKU with no replenishment requirement receives a final suggestion of `0`.
4. MOQ/MOV rules are applied only when the corresponding vendor criteria are available.
5. Vendor ordering criteria determine whether MOQ or MOV validation is required.
6. The final suggestion is intended to represent the quantity that should be considered for purchase ordering.

---

## 11. Future Improvements

The planner can be extended with:

* Safety-stock calculations
* ABC/XYZ inventory classification
* Demand forecasting
* Supplier performance analysis
* Purchase-order consolidation by vendor
* Vendor-level MOQ/MOV optimization
* Power BI dashboards
* Automated database refresh
* Exception alerts for critical SKUs
* Web-based replenishment planning interface

---

## 12. Conclusion

This solution provides an automated and scalable approach to SKU-level replenishment planning.

It combines **inventory analysis, replenishment calculations, vendor constraints, data processing, and database storage** into a single workflow.

The resulting output can be used by supply-chain or procurement teams to identify replenishment requirements and support purchase-order decisions.

