import json
import networkx as nx

class ProductGraph:
    def __init__(self, data_file):
        self.G = nx.Graph()
        self.load_data(data_file)

    def load_data(self, data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        # Add Nodes
        for node in data['nodes']:
            self.G.add_node(node['id'], **node)
        
        # Add Edges
        for edge in data['edges']:
            self.G.add_edge(edge['source'], edge['target'], relation=edge['relation'])

    def get_product_details(self, product_id):
        if product_id in self.G.nodes:
            return self.G.nodes[product_id]
        return None

    def get_all_product_names(self):
        # Safe check for 'type' to avoid crashes on attribute nodes
        return {
            n: self.G.nodes[n]['name'] 
            for n in self.G.nodes 
            if self.G.nodes[n].get('type') == 'product'
        }

    def find_substitutes(self, product_id, max_price=None, required_tags=None):
        target_node = self.G.nodes[product_id]
        
        # 1. Traversal: Find the category and brand of the requested product
        category_node = None
        target_brand_node = None
        
        for neighbor in self.G.neighbors(product_id):
            edge_data = self.G.get_edge_data(product_id, neighbor)
            if edge_data['relation'] == 'IS_A':
                category_node = neighbor
            elif edge_data['relation'] == 'HAS_BRAND':
                target_brand_node = neighbor

        # If no category found, we can't find similar items
        if not category_node:
            return []

        # 2. Candidate Collection: Get all siblings in that category
        candidates = []
        for neighbor in self.G.neighbors(category_node):
            if neighbor == product_id: continue # Skip self
            
            node_data = self.G.nodes[neighbor]
            if node_data.get('type') == 'product':
                candidates.append((neighbor, node_data))

        # 3. Filtering & Scoring
        scored_candidates = []
        
        for cand_id, cand_data in candidates:
            # Filter: Stock (Must be True)
            if not cand_data.get('in_stock', False): 
                continue
            
            # Filter: Price (Must be within budget if budget is set)
            if max_price and cand_data.get('price', 0) > max_price: 
                continue

            # Filter: Tags (Must match all required tags)
            # We look at the candidate's neighbors to find its attributes
            cand_tags = []
            for n in self.G.neighbors(cand_id):
                if self.G.nodes[n].get('type') == 'attribute':
                    cand_tags.append(self.G.nodes[n].get('name', ''))
            
            if required_tags:
                # If candidate tags don't include ALL required tags, skip
                if not set(required_tags).issubset(set(cand_tags)):
                    continue

            # Scoring Logic
            score = 0
            reasons = []

            # Check Brand Match
            cand_brand = None
            for n in self.G.neighbors(cand_id):
                if self.G.nodes[n].get('type') == 'brand':
                    cand_brand = n
                    break
            
            if cand_brand and cand_brand == target_brand_node:
                score += 10
                reasons.append("same_brand_match")
            else:
                reasons.append("diff_brand_alternative")

            # Check Price Difference
            # Use .get() for safety, default to 0
            cand_price = cand_data.get('price', 0)
            target_price = target_node.get('price', 0)

            if cand_price < target_price:
                score += 5
                reasons.append("cheaper_option")
            elif cand_price > target_price:
                reasons.append("premium_option")

            reasons.append("same_category")

            scored_candidates.append({
                "name": cand_data['name'],
                "price": cand_price,
                "score": score,
                "reasons": reasons
            })

        # Sort by score descending (Highest score first)
        scored_candidates.sort(key=lambda x: x['score'], reverse=True)
        
        # Return top 3
        return scored_candidates[:3]