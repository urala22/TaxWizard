import numpy as np
from datetime import datetime

def calculate_tax_liability(tax_data):
    """
    Calculate the estimated tax liability based on the provided tax data
    """
    # Define basic tax brackets for 2023 (simplified for demonstration)
    # These would normally be more complex and based on filing status
    brackets = {
        'single': [
            (0, 11000, 0.10),
            (11001, 44725, 0.12),
            (44726, 95375, 0.22),
            (95376, 182100, 0.24),
            (182101, 231250, 0.32),
            (231251, 578125, 0.35),
            (578126, float('inf'), 0.37)
        ],
        'married': [
            (0, 22000, 0.10),
            (22001, 89450, 0.12),
            (89451, 190750, 0.22),
            (190751, 364200, 0.24),
            (364201, 462500, 0.32),
            (462501, 693750, 0.35),
            (693751, float('inf'), 0.37)
        ],
        'head_of_household': [
            (0, 15700, 0.10),
            (15701, 59850, 0.12),
            (59851, 95350, 0.22),
            (95351, 182100, 0.24),
            (182101, 231250, 0.32),
            (231251, 578100, 0.35),
            (578101, float('inf'), 0.37)
        ]
    }
    
    # Map the filing status from tax_data to the brackets
    filing_status_map = {
        'single': 'single',
        'married_joint': 'married',
        'married_separate': 'single',  # Simplified - would be different in reality
        'head_of_household': 'head_of_household'
    }
    
    status = filing_status_map.get(tax_data.filing_status, 'single')
    
    # Calculate adjusted gross income (AGI)
    agi = tax_data.income
    
    # Subtract retirement contributions (simplified)
    agi -= tax_data.retirement_contributions
    
    # For self-employed, subtract business expenses from business income
    if tax_data.self_employed:
        business_profit = max(0, tax_data.business_income - tax_data.business_expenses)
        agi += business_profit
    
    # Add rental income (simplified)
    rental_profit = max(0, tax_data.rental_income - tax_data.rental_expenses)
    agi += rental_profit
    
    # Add capital gains (simplified - would normally have different rates)
    agi += tax_data.capital_gains
    
    # Calculate standard deduction (2023 values, simplified)
    standard_deduction = {
        'single': 13850,
        'married': 27700,
        'head_of_household': 20800
    }.get(status, 13850)
    
    # Calculate itemized deductions
    itemized_deductions = (
        tax_data.mortgage_interest +
        tax_data.property_tax +
        tax_data.charitable_contributions +
        max(0, tax_data.medical_expenses - 0.075 * agi)  # Medical expenses over 7.5% of AGI
    )
    
    # Use the higher of standard or itemized deductions
    deduction = max(standard_deduction, itemized_deductions)
    
    # Calculate taxable income
    taxable_income = max(0, agi - deduction)
    
    # Calculate tax based on brackets
    tax = 0
    for lower, upper, rate in brackets[status]:
        if taxable_income > lower:
            tax += min(upper - lower, taxable_income - lower) * rate
        if taxable_income <= upper:
            break
    
    # Calculate dependent credit (simplified)
    dependent_credit = tax_data.dependents * 2000  # $2,000 per dependent in 2023
    
    # Subtract credits
    tax = max(0, tax - dependent_credit)
    
    return {
        'agi': agi,
        'taxable_income': taxable_income,
        'tax_liability': tax,
        'standard_deduction': standard_deduction,
        'itemized_deductions': itemized_deductions,
        'deduction_used': 'Itemized' if itemized_deductions > standard_deduction else 'Standard',
        'dependent_credit': dependent_credit
    }

def get_tax_optimization_strategies(tax_data):
    """
    Generate tax optimization strategies based on the user's tax data
    """
    strategies = []
    tax_calc = calculate_tax_liability(tax_data)
    
    # Check if user is using standard deduction but could benefit from itemizing
    if tax_calc['deduction_used'] == 'Standard' and tax_calc['itemized_deductions'] > 0.7 * tax_calc['standard_deduction']:
        strategies.append({
            'strategy': 'Increase Itemized Deductions',
            'description': 'Your itemized deductions are close to the standard deduction threshold. Consider increasing charitable contributions or bunching deductions to exceed the standard deduction amount.',
            'potential_savings': (tax_calc['standard_deduction'] - tax_calc['itemized_deductions']) * 0.22  # Approximate tax rate
        })
    
    # Retirement contribution strategy
    max_contribution = 22500  # 2023 401(k) limit
    if tax_data.retirement_contributions < max_contribution:
        potential_contribution = min(max_contribution - tax_data.retirement_contributions, 
                                  tax_calc['taxable_income'] * 0.1)  # Suggest 10% of taxable income
        if potential_contribution > 1000:
            strategies.append({
                'strategy': 'Increase Retirement Contributions',
                'description': f'Consider contributing up to ${int(potential_contribution)} more to your retirement accounts to reduce taxable income.',
                'potential_savings': potential_contribution * 0.22  # Approximate tax rate
            })
    
    # Self-employed tax strategies
    if tax_data.self_employed:
        # Home office deduction
        strategies.append({
            'strategy': 'Home Office Deduction',
            'description': 'If you work from home, consider taking the home office deduction to reduce your self-employment tax.',
            'potential_savings': tax_data.business_income * 0.02  # Rough estimate
        })
        
        # SEP IRA or Solo 401(k)
        strategies.append({
            'strategy': 'SEP IRA or Solo 401(k)',
            'description': 'As a self-employed individual, you can set up a SEP IRA or Solo 401(k) to save more for retirement and reduce taxes.',
            'potential_savings': tax_data.business_income * 0.05  # Rough estimate
        })
    
    # Dependent care FSA
    if tax_data.dependents > 0:
        strategies.append({
            'strategy': 'Dependent Care FSA',
            'description': 'If you have dependents requiring care, consider a Dependent Care FSA to pay for expenses with pre-tax dollars.',
            'potential_savings': 5000 * 0.22  # Maximum FSA contribution * approximate tax rate
        })
    
    # HSA contributions
    strategies.append({
        'strategy': 'Health Savings Account (HSA)',
        'description': 'If eligible, maximize HSA contributions to pay for medical expenses with pre-tax dollars.',
        'potential_savings': 3650 * 0.22  # 2023 individual HSA limit * approximate tax rate
    })
    
    # Capital loss harvesting if capital gains exist
    if tax_data.capital_gains > 0:
        strategies.append({
            'strategy': 'Tax-Loss Harvesting',
            'description': 'Consider selling investments at a loss to offset capital gains taxes.',
            'potential_savings': tax_data.capital_gains * 0.05  # Rough estimate
        })
    
    return strategies
