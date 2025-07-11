import pandas as pd
import os
import logging
from typing import Tuple, Optional
import difflib

class SKUMapper:
    """Maps item descriptions to SKU codes"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
        self.mapping_file = self.config.get('paths.sku_mapping_file', 'config/sku_mapping.xlsx')
        self.mapping_df = self._load_sku_mapping()
    
    def _load_sku_mapping(self) -> pd.DataFrame:
        """Load SKU mapping from Excel file"""
        try:
            if os.path.exists(self.mapping_file):
                df = pd.read_excel(self.mapping_file)
                self.logger.info(f"Loaded SKU mapping with {len(df)} entries")
                return df
            else:
                self.logger.warning("SKU mapping file not found. Creating sample mapping.")
                return self._create_sample_mapping()
                
        except Exception as e:
            self.logger.error(f"Error loading SKU mapping: {str(e)}")
            return self._create_sample_mapping()
    
    def _create_sample_mapping(self) -> pd.DataFrame:
        """Create sample SKU mapping for demo"""
        sample_data = {
            'SKU': ['SKU-001', 'SKU-002', 'SKU-003', 'SKU-004', 'SKU-005'],
            'ItemDescription': [
                'Red Steel Widget 10kg',
                'Blue Aluminum Component 5kg', 
                'Green Plastic Part',
                'Steel Rod 1m',
                'Copper Wire 100m'
            ],
            'CustomerDescription': [
                'Red Widget',
                'Blue Component',
                'Green Part',
                'Steel Rod',
                'Copper Wire'
            ],
            'Customer': [
                'ABC Manufacturing',
                'XYZ Industries',
                'DEF Ltd',
                'All Customers',
                'All Customers'
            ]
        }
        
        df = pd.DataFrame(sample_data)
        
        # Create directory and save sample mapping
        os.makedirs(os.path.dirname(self.mapping_file), exist_ok=True)
        df.to_excel(self.mapping_file, index=False)
        
        self.logger.info(f"Created sample SKU mapping: {self.mapping_file}")
        return df
    
    def map_item_to_sku(self, item_description: str, customer_name: str = None) -> Tuple[Optional[str], bool]:
        """Map item description to SKU code"""
        try:
            self.logger.info(f"Mapping item: '{item_description}' for customer: '{customer_name}'")
            
            # First try exact match
            sku = self._exact_match(item_description, customer_name)
            if sku:
                return sku, True
            
            # Try fuzzy matching
            sku = self._fuzzy_match(item_description, customer_name)
            if sku:
                return sku, True
            
            # Try partial matching
            sku = self._partial_match(item_description, customer_name)
            if sku:
                return sku, True
            
            self.logger.warning(f"No SKU mapping found for: {item_description}")
            return None, False
            
        except Exception as e:
            self.logger.error(f"Error mapping SKU: {str(e)}")
            return None, False
    
    def _exact_match(self, item_description: str, customer_name: str = None) -> Optional[str]:
        """Try exact string matching"""
        # Check customer-specific descriptions first
        if customer_name:
            mask = (
                (self.mapping_df['CustomerDescription'].str.lower() == item_description.lower()) &
                (self.mapping_df['Customer'].str.lower() == customer_name.lower())
            )
            matches = self.mapping_df[mask]
            if not matches.empty:
                return matches.iloc[0]['SKU']
        
        # Check general item descriptions
        mask = self.mapping_df['ItemDescription'].str.lower() == item_description.lower()
        matches = self.mapping_df[mask]
        if not matches.empty:
            return matches.iloc[0]['SKU']
        
        return None
    
    def _fuzzy_match(self, item_description: str, customer_name: str = None, threshold: float = 0.8) -> Optional[str]:
        """Try fuzzy string matching"""
        best_match = None
        best_score = 0
        
        for _, row in self.mapping_df.iterrows():
            # Calculate similarity scores
            desc_score = difflib.SequenceMatcher(None, 
                                               item_description.lower(), 
                                               row['ItemDescription'].lower()).ratio()
            
            customer_desc_score = difflib.SequenceMatcher(None, 
                                                        item_description.lower(), 
                                                        row['CustomerDescription'].lower()).ratio()
            
            # Use the higher score
            score = max(desc_score, customer_desc_score)
            
            # Consider customer match if provided
            if customer_name and row['Customer'].lower() != 'all customers':
                if customer_name.lower() not in row['Customer'].lower():
                    score *= 0.5  # Reduce score for customer mismatch
            
            if score > best_score and score >= threshold:
                best_score = score
                best_match = row['SKU']
        
        if best_match:
            self.logger.info(f"Fuzzy match found with score {best_score:.2f}: {best_match}")
        
        return best_match
    
    def _partial_match(self, item_description: str, customer_name: str = None) -> Optional[str]:
        """Try partial string matching"""
        item_words = set(item_description.lower().split())
        
        for _, row in self.mapping_df.iterrows():
            desc_words = set(row['ItemDescription'].lower().split())
            customer_desc_words = set(row['CustomerDescription'].lower().split())
            
            # Calculate word overlap
            desc_overlap = len(item_words.intersection(desc_words)) / len(item_words.union(desc_words))
            customer_desc_overlap = len(item_words.intersection(customer_desc_words)) / len(item_words.union(customer_desc_words))
            
            # Use higher overlap score
            overlap = max(desc_overlap, customer_desc_overlap)
            
            if overlap >= 0.5:  # At least 50% word overlap
                self.logger.info(f"Partial match found with overlap {overlap:.2f}: {row['SKU']}")
                return row['SKU']
        
        return None