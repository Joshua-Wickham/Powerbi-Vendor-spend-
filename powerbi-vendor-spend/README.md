# Power BI Vendor Spend Dashboard (Data Model + Build Guide)

A star-schema dataset and DAX measure library for a vendor spend
dashboard in Power BI — the data-modeling and DAX side of a BI
project, packaged so you can open Power BI Desktop, import the CSVs,
and build the report on top.

> **Note:** this repo contains the data model (CSV tables) and DAX
> measures, not a `.pbix` file — Power BI Desktop is required to
> actually build and view the report. That's intentional: recruiters
> and interviewers care more about whether you understand star schemas
> and DAX than whether you can open a pre-built file.

## What's included

- **`generate_star_schema.py`** — generates the dataset (Python 3,
  standard library only). Re-run anytime to regenerate fresh sample
  data.
- **`data/fact_po_lines.csv`** — the fact table: one row per PO line
  item (vendor, material, plant, date, quantity, price, net value)
- **`data/dim_vendor.csv`** — vendor dimension (id, name, category)
- **`data/dim_material.csv`** — material dimension (id, description,
  material group)
- **`data/dim_date.csv`** — a standard date dimension (year, month,
  quarter, day of week) covering the last 180 days, for time
  intelligence measures
- **`dax_measures.txt`** — ready-to-paste DAX measures: total spend,
  average line value, month-over-month change, YTD spend, top vendor,
  % of total spend, and a vendor concentration flag

## How to build the report

1. Open Power BI Desktop → **Get Data → Text/CSV** → import all four
   files in `data/`.
2. Go to **Model view** and set up relationships:
   - `fact_po_lines[vendor_id]` → `dim_vendor[vendor_id]`
   - `fact_po_lines[material_id]` → `dim_material[material_id]`
   - `fact_po_lines[date]` → `dim_date[date]`
   - Right-click `dim_date` → **Mark as date table** → select `date`
3. Add the measures from `dax_measures.txt` (Model view → New Measure).
4. Suggested report pages:
   - **Overview**: KPI cards for Total Spend, Active Vendors, Spend
     YTD, Top Vendor; a bar chart of spend by vendor
   - **Trends**: a line chart of Total Spend by month, with the MoM
     Spend Change % measure as a KPI or tooltip
   - **Vendor Detail**: a table of vendors with Total Spend, % of
     Total Spend, and the High Concentration Vendor flag; a slicer
     for material group and plant

## Concepts this demonstrates

- **Star schema design** — separating fact (transactions) from
  dimensions (vendor, material, date), the standard BI data model
- **DAX measures** — aggregations, time intelligence (YTD, MoM), and
  business-rule logic (concentration flag) beyond basic SUM/COUNT
- **Vendor spend analysis** — the kind of report a purchasing or
  accounting team uses to track spend concentration and trends

## Notes

All data in `data/` is randomly generated for demonstration and does
not reflect any real employer's records.
