from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
ann_dir = ROOT / "data" / "annotations"
rows = []
for p in ann_dir.rglob("*.xml"):
    try:
        root = ET.parse(p).getroot()
    except ET.ParseError:
        continue  # pliki-śmieci z macOS
    objs = root.findall("object")
    for i, obj in enumerate(objs):
        bb = obj.find("bndbox")
        label = obj.find("name").text
        rows.append({
            "patient": p.parent.name,
            "cls": p.parent.name[0],
            "label_xml": label,
            "label_mismatch": label.upper() != p.parent.name[0],
            "obj_idx": i,
            "sop_uid": p.stem,
            "xmin": int(bb.find("xmin").text),
            "ymin": int(bb.find("ymin").text),
            "xmax": int(bb.find("xmax").text),
            "ymax": int(bb.find("ymax").text),
        })

df = pd.DataFrame(rows)
df.to_csv(ROOT / "data" / "annotations.csv", index=False)
print(len(df))
print(df.groupby("cls").agg(obiekty=("sop_uid", "count"), pacjenci=("patient", "nunique")))
print(df["label_mismatch"].sum())