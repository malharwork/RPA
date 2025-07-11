import pandas as pd
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

class AgingReportGenerator:
    """Generates customer aging reports"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
        self.reports_folder = self.config.get('paths.reports_folder', 'reports')
    
    def generate_aging_report(self, customer_id: str, customer_name: str) -> str:
        """Generate aging report for customer"""
        try:
            self.logger.info(f"Generating aging report for customer: {customer_name}")
            print(f"📊 Generating aging report for: {customer_name}")
            
            # Create sample aging data (in real system, this would query the database)
            aging_data = self._create_sample_aging_data(customer_id, customer_name)
            
            # Create DataFrame
            df = pd.DataFrame(aging_data)
            
            # Generate report file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"AgingReport_{customer_id}_{timestamp}.xlsx"
            report_path = os.path.join(self.reports_folder, report_filename)
            
            # Ensure reports directory exists
            os.makedirs(self.reports_folder, exist_ok=True)
            
            # Write to Excel with formatting
            with pd.ExcelWriter(report_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Aging Report', index=False)
                
                # Get workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['Aging Report']
                
                # Add header formatting
                from openpyxl.styles import Font, PatternFill
                header_font = Font(bold=True)
                header_fill = PatternFill(start_color='CCCCCC', end_color='CCCCCC', fill_type='solid')
                
                for cell in worksheet[1]:
                    cell.font = header_font
                    cell.fill = header_fill
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            self.logger.info(f"Aging report generated: {report_path}")
            print(f"   ✅ Report saved: {report_filename}")
            
            return report_path
            
        except Exception as e:
            self.logger.error(f"Error generating aging report: {str(e)}")
            raise
    
    def _create_sample_aging_data(self, customer_id: str, customer_name: str) -> list:
        """Create sample aging data for demonstration"""
        # Sample invoice data
        base_date = datetime.now()
        
        aging_data = [
            {
                'Invoice_No': 'INV-2024001',
                'Invoice_Date': (base_date - timedelta(days=60)).strftime('%Y-%m-%d'),
                'Due_Date': (base_date - timedelta(days=30)).strftime('%Y-%m-%d'),
                'Amount': '$15,000',
                'Days_Overdue': '30',
                'Aging_Bucket': '31-60 Days',
                'Comments': 'Customer promised payment by month end'
            },
            {
                'Invoice_No': 'INV-2024002',
                'Invoice_Date': (base_date - timedelta(days=45)).strftime('%Y-%m-%d'),
                'Due_Date': (base_date - timedelta(days=15)).strftime('%Y-%m-%d'),
                'Amount': '$8,500',
                'Days_Overdue': '15',
                'Aging_Bucket': '1-30 Days',
                'Comments': 'Pending approval from customer finance team'
            },
            {
                'Invoice_No': 'INV-2024003',
                'Invoice_Date': (base_date - timedelta(days=90)).strftime('%Y-%m-%d'),
                'Due_Date': (base_date - timedelta(days=60)).strftime('%Y-%m-%d'),
                'Amount': '$12,200',
                'Days_Overdue': '60',
                'Aging_Bucket': '61-90 Days',
                'Comments': 'Customer in communication for payment plan'
            }
        ]
        
        return aging_data