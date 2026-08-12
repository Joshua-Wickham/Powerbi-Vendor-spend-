"""
generate_star_schema.py

Builds a small star-schema dataset — one fact table plus supporting
dimension tables — designed to be imported directly into Power BI
Desktop (or Excel Power Pivot) to build a vendor spend dashboard on top
of. This is the data-modeling step that comes before opening Power BI:
get the fact/dimension structure right first, then the report is just
drag-and-drop.

Tables created (all in data/):
  - fact_po_lines.csv   : one row per PO line item (the fact table)
  - dim_vendor.csv       : vendor attributes
  - dim_material.csv     : material/item attributes
  - dim_date.csv          : a standard date dimension for time intelligence

Run:
    python generate_star_schema.py
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(5)

VENDORS = [
    ("V01", "Meridian Fasteners", "Fasteners"),
    ("V02", "Coastal Hydraulics", "Hydraulics"),
    ("V03", "Northgate Machining", "Machining"),
    ("V04", "Vantage Bearings", "Bearings"),
    ("V05", "Ferro Industrial", "Industrial Supply"),
    ("V06", "Blackstone Tooling", "Tooling"),
]

MATERIALS = [
    ("M01", "Hydraulic Fitting 3/8in", "Hydraulics"),
    ("M02", "Steel Bracket 4in", "Structural"),
    ("M03", "Ball Bearing 20mm", "Bearings"),
    ("M04", "Hex Bolt M8x40", "Fasteners"),
    ("M05", "O-Ring Seal Kit", "Seals"),
    ("M06", "Roller Chain 10ft", "Drivetrain"),
]

PLANTS = ["Plant 1000", "Plant 1010", "Plant 1020"]


def build_dim_date(start, end, path="data/dim_date.csv"):
    rows = []
    current = start
    while current <= end:
        rows.append({
            "date": current.strftime("%Y-%m-%d"),
            "year": current.year,
            "month": current.month,
            "month_name": current.strftime("%B"),
            "quarter": f"Q{((current.month - 1) // 3) + 1}",
            "day_of_week": current.strftime("%A"),
        })
        current += timedelta(days=1)

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {path}")


def build_dim_vendor(path="data/dim_vendor.csv"):
    rows = [{"vendor_id": v, "vendor_name": name, "category": cat} for v, name, cat in VENDORS]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["vendor_id", "vendor_name", "category"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {path}")


def build_dim_material(path="data/dim_material.csv"):
    rows = [{"material_id": m, "material_desc": desc, "material_group": grp} for m, desc, grp in MATERIALS]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["material_id", "material_desc", "material_group"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {path}")


def build_fact_po_lines(start, end, n=150, path="data/fact_po_lines.csv"):
    rows = []
    span_days = (end - start).days
    for i in range(1, n + 1):
        vendor_id = random.choice(VENDORS)[0]
        material_id = random.choice(MATERIALS)[0]
        po_date = start + timedelta(days=random.randint(0, span_days))
        qty = random.randint(5, 300)
        unit_price = round(random.uniform(2.0, 55.0), 2)

        rows.append({
            "line_id": f"L{i:05d}",
            "po_number": f"45{100000 + (i // 3)}",
            "vendor_id": vendor_id,
            "material_id": material_id,
            "plant": random.choice(PLANTS),
            "date": po_date.strftime("%Y-%m-%d"),
            "quantity": qty,
            "unit_price": unit_price,
            "net_value": round(qty * unit_price, 2),
        })

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "line_id", "po_number", "vendor_id", "material_id", "plant",
            "date", "quantity", "unit_price", "net_value",
        ])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {path}")


if __name__ == "__main__":
    start = datetime.today() - timedelta(days=180)
    end = datetime.today()

    build_dim_date(start, end)
    build_dim_vendor()
    build_dim_material()
    build_fact_po_lines(start, end)
