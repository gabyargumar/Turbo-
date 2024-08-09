def generate_amortization_schedule(principal, annual_rate, months):
    # Calculate the fixed principal repayment amount
    fixed_principal_repayment = principal / months
    # Convert annual rate to monthly rate
    schedule = []
    remaining_principal = principal
    
    for _ in range(months):
        # Calculate interest based on remaining principal
        interest_payment = remaining_principal * annual_rate
        # Total payment for the month
        total_payment = interest_payment + fixed_principal_repayment
        # Update remaining principal
        remaining_principal -= fixed_principal_repayment
        
        if remaining_principal < 0:
            remaining_principal = 0
        
        schedule.append({
            'Interes y Servicio': round(interest_payment, 2),
            'Abono a Capital': round(fixed_principal_repayment, 2),
            'Total Cancelar': round(total_payment, 2),
            'Capital Restante': round(remaining_principal, 2)
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
            result += (f"Pago {i}:\n"
                       f"Interes y Servicio: ${payment['Interes y Servicio']}\n"
                       f"Abono a Capital: ${payment['Abono a Capital']}\n"
                       f"Total Cancelar: ${payment['Total Cancelar']}\n"
                       f"Capital Restante: ${payment['Capital Restante']}\n"
                       "--------------------------------\n")
        return result.strip()
    
    except ValueError:
        return "Invalid input. Please enter numeric values."
