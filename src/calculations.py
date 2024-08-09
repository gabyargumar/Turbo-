def calculate_monthly_payment(principal, annual_rate, months):
    if annual_rate == 0:
        return principal / months
    monthly_rate = annual_rate / 12
    return (principal * monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)

def generate_amortization_schedule(principal, annual_rate, months):
    monthly_payment = calculate_monthly_payment(principal, annual_rate, months)
    schedule = []
    
    for _ in range(months):
        interest_payment = (principal * annual_rate / 12)
        principal_payment = monthly_payment - interest_payment
        principal -= principal_payment
        
        if principal < 0:
            principal = 0
        
        schedule.append({
            'Monthly Payment': round(monthly_payment, 2),
            'Principal Repayment': round(principal_payment, 2),
            'Total Payment': round(monthly_payment + interest_payment, 2),
            'Remaining Principal': round(principal, 2)
        })
    
    return schedule

def perform_calculation(principal, months):
    try:
        principal = float(principal)
        months = int(months)
        annual_rate = 0.14  # Fixed annual interest rate of 14%
        schedule = generate_amortization_schedule(principal, annual_rate, months)
        
        result = ""
        for i, payment in enumerate(schedule, start=1):
            result += (f"Payment {i}: Monthly Payment: ${payment['Monthly Payment']}, "
                       f"Principal Repayment: ${payment['Principal Repayment']}, "
                       f"Total Payment: ${payment['Total Payment']}, "
                       f"Remaining Principal: ${payment['Remaining Principal']}\n")
        return result.strip()
    
    except ValueError:
        return "Invalid input. Please enter numeric values."
