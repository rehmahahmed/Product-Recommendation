# Product Recommendation System

A **Classical AI** application that uses a **Knowledge Graph (KG)** to suggest logical product substitutes when an item is out of stock. Built with **Python**, **NetworkX**, and **Streamlit**.

## 📌 Overview

This project implements a product substitution assistant without using Black-box Machine Learning or LLMs. Instead, it relies on **explicit graph reasoning** and **rule-based logic**.

When a user requests a product that is "Out of Stock," the system:

1.  **Traverses the Knowledge Graph** to understand the product's category, brand, and attributes.
2.  **Identifies Siblings** (products in the same category).
3.  **Filters & Scores candidates** based on logical constraints (Price, Stock, Dietary Tags).
4.  **Explains the decision** (e.g., "Same Brand," "Cheaper Option") using deterministic rules.

## 🚀 How to Run Locally

### Prerequisites

  * Python 3.8+
  * pip

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/shopkeeper-ai.git
cd shopkeeper-ai
```

### Step 2: Install Dependencies

```bash
pip install networkx streamlit pandas
```

### Step 3: Generate the Knowledge Graph

This script converts the raw CSV dataset into a graph structure (`data.json`) composed of Nodes and Edges.

```bash
python convert_csv_to_graph.py
```

### Step 4: Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

-----

## 🧠 Knowledge Graph Design

The backend is powered by **NetworkX**. We model the retail inventory as a directed graph.

### Nodes (Entities)

  * **Product:** The item itself (e.g., `id: "prod_1", name: "Lays Classic", price: 20`)
  * **Category:** The grouping (e.g., `id: "cat_Snacks", name: "Snacks"`)
  * **Brand:** The manufacturer (e.g., `id: "brand_Lays", name: "Lays"`)
  * **Attribute:** Specific tags (e.g., `id: "attr_Masala", name: "Masala"`)

### Edges (Relationships)

  * `(Product) --[IS_A]--> (Category)`
  * `(Product) --[HAS_BRAND]--> (Brand)`
  * `(Product) --[HAS_ATTRIBUTE]--> (Attribute)`

-----

## 🔍 Search & Reasoning Method

The system uses a **2-Hop Neighbor Search** strategy combined with a **Weighted Scoring Algorithm**.

### 1\. Search Approach (Traversal)

Instead of a database query, we traverse the graph edges:

1.  **Start Node:** The requested product (e.g., *Product A*).
2.  **Hop 1:** Traverse `IS_A` edge to find the **Category Node**.
3.  **Hop 2:** Traverse backward from Category to find all **Sibling Products** (Candidates).

### 2\. Constraint Handling (The Filter)

Before scoring, candidates are strictly filtered out if they fail these checks:

  * **Stock Status:** Must be `in_stock = True`.
  * **Price:** Must be `<= Max Price` (if set by user).
  * **Tags:** Must possess all `HAS_ATTRIBUTE` connections requested (e.g., "Vegetarian").

### 3\. Explanation Rule Mechanism (The Scorer)

Valid candidates are ranked based on a rule-based point system. The highest scorers are recommended.

| Rule | Condition | Points | Human Explanation |
| :--- | :--- | :--- | :--- |
| **Brand Loyalty** | `candidate.brand == target.brand` | **+10** | "🔹 Same Brand" |
| **Price Saver** | `candidate.price < target.price` | **+5** | "💰 Cheaper Option" |
| **Premium** | `candidate.price > target.price` | **+0** | "💎 Premium Option" |
| **Category** | `candidate.category == target.category` | **N/A** | "📂 Same Category" |

-----

## 📂 Project Structure

```text
├── app.py                   # Main Streamlit Frontend Application
├── graph_engine.py          # Backend Logic: Graph construction, Search, Scoring
├── data_conversion.py  # ETL Script: Converts CSV -> JSON Graph
├── data.json                # The Knowledge Graph (Generated file)
├── logo.png                 # Project Branding
├── requirements.txt         # Dependencies
└── README.md                # Project Documentation
```


### Author

**Rehmah Ahmed Batki**

  * [Portfolio](https://rehmahprojects.com)
  * [Email](mailto:admin@rehmahprojects.com)
