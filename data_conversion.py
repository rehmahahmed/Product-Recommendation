import pandas as pd
import json

def convert_csv_to_json(csv_file_path, output_file_path, limit=500):
    df = pd.read_csv(csv_file_path)
    df.columns = [c.strip() for c in df.columns]

    needed_cols = ['product', 'category', 'sub_category', 'brand', 'sale_price']
    df = df[needed_cols].dropna().head(limit)

    nodes = []
    edges = []

    existing_ids = set() # Track ALL node IDs to avoid duplicates

    for index, row in df.iterrows():
        prod_id = f"prod_{index}"
        cat_id = f"cat_{row['category'].replace(' ', '_')}"
        brand_id = f"brand_{row['brand'].replace(' ', '_')}"
        # Create an attribute ID based on sub_category
        attr_id = f"attr_{row['sub_category'].replace(' ', '_')}"

        # 1. Add Product Node
        if prod_id not in existing_ids:
            nodes.append({
                "id": prod_id,
                "type": "product",
                "name": row['product'],
                "price": float(row['sale_price']),
                "in_stock": True if (index % 5 != 0) else False
            })
            existing_ids.add(prod_id)

        # 2. Add Category Node
        if cat_id not in existing_ids:
            nodes.append({"id": cat_id, "type": "category", "name": row['category']})
            existing_ids.add(cat_id)

        # 3. Add Brand Node
        if brand_id not in existing_ids:
            nodes.append({"id": brand_id, "type": "brand", "name": row['brand']})
            existing_ids.add(brand_id)

        # 4. Add Attribute Node (CRITICAL FIX HERE)
        if attr_id not in existing_ids:
            nodes.append({"id": attr_id, "type": "attribute", "name": row['sub_category']})
            existing_ids.add(attr_id)

        # 5. Create Edges
        edges.append({"source": prod_id, "target": cat_id, "relation": "IS_A"})
        edges.append({"source": prod_id, "target": brand_id, "relation": "HAS_BRAND"})
        edges.append({"source": prod_id, "target": attr_id, "relation": "HAS_ATTRIBUTE"})

    graph_data = {"nodes": nodes, "edges": edges}

    with open(output_file_path, 'w') as f:
        json.dump(graph_data, f, indent=2)

    print(f"Success! Created {output_file_path} with explicit attribute nodes.")

if __name__ == "__main__":

    convert_csv_to_json("BigBasket Products.csv", "data.json")
