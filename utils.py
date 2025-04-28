import os
import re

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'csv', 'xls', 'xlsx'}

def extract_form16_data(file_path):
    """Extract tax data from Form 16"""
    # This is a basic implementation - you may want to use OCR or PDF parsing libraries
    # for more sophisticated extraction
    try:
        import PyPDF2
        tax_data = {}
        
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            # Basic extraction - you'll need to adjust patterns based on your Form 16 format
            income_pattern = r"Gross Total Income.*?₹\s*([\d,]+)"
            tax_pattern = r"Total Tax Payable.*?₹\s*([\d,]+)"
            
            import re
            income_match = re.search(income_pattern, text)
            if income_match:
                tax_data['income'] = float(income_match.group(1).replace(',', ''))
            
            tax_match = re.search(tax_pattern, text)
            if tax_match:
                tax_data['tax_payable'] = float(tax_match.group(1).replace(',', ''))
                
        return tax_data
    except Exception as e:
        logging.error(f"Error extracting Form 16 data: {str(e)}")
        return None

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_tax_data(tax_data):
    """Validate tax data input"""
    errors = []
    
    if tax_data.income < 0:
        errors.append({
            'field': 'income',
            'message': 'Income cannot be negative',
            'severity': 'high'
        })
    
    if tax_data.dependents < 0:
        errors.append({
            'field': 'dependents',
            'message': 'Number of dependents cannot be negative',
            'severity': 'high'
        })
    
    if tax_data.mortgage_interest < 0:
        errors.append({
            'field': 'mortgage_interest',
            'message': 'Mortgage interest cannot be negative',
            'severity': 'medium'
        })
    
    if tax_data.property_tax < 0:
        errors.append({
            'field': 'property_tax',
            'message': 'Property tax cannot be negative',
            'severity': 'medium'
        })
    
    if tax_data.charitable_contributions < 0:
        errors.append({
            'field': 'charitable_contributions',
            'message': 'Charitable contributions cannot be negative',
            'severity': 'medium'
        })
    
    if tax_data.medical_expenses < 0:
        errors.append({
            'field': 'medical_expenses',
            'message': 'Medical expenses cannot be negative',
            'severity': 'medium'
        })
    
    if tax_data.retirement_contributions < 0:
        errors.append({
            'field': 'retirement_contributions',
            'message': 'Retirement contributions cannot be negative',
            'severity': 'medium'
        })
    
    if tax_data.business_income < 0:
        errors.append({
            'field': 'business_income',
            'message': 'Business income cannot be negative',
            'severity': 'medium'
        })
    
    # Check for potential errors/inconsistencies
    if tax_data.self_employed and tax_data.business_income == 0:
        errors.append({
            'field': 'business_income',
            'message': 'You marked self-employed but reported no business income',
            'severity': 'low'
        })
    
    if tax_data.business_expenses > tax_data.business_income:
        errors.append({
            'field': 'business_expenses',
            'message': 'Business expenses exceed business income',
            'severity': 'medium'
        })
    
    if tax_data.medical_expenses > tax_data.income * 0.5:
        errors.append({
            'field': 'medical_expenses',
            'message': 'Medical expenses seem unusually high (>50% of income)',
            'severity': 'low'
        })
    
    if tax_data.charitable_contributions > tax_data.income * 0.5:
        errors.append({
            'field': 'charitable_contributions',
            'message': 'Charitable contributions seem unusually high (>50% of income)',
            'severity': 'low'
        })
    
    return errors

def format_currency(amount):
    """Format a number as Indian Rupees"""
    if amount is None:
        return "₹0.00"
    return "₹{:,.2f}".format(amount)