from decimal import Decimal, ROUND_HALF_UP, InvalidOperation, getcontext
import os
from datetime import date, timedelta

getcontext().prec = 28

def to_decimal(value):
    try:
        if ":" in value:
            h, m = value.split(":")
            return Decimal(h) + (Decimal(m) / Decimal(60))
        return Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"Valor inválido: {value}")

def format_money(value):
    return f"${value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):,.2f}"

def calc_week(hours, planning, training, rate_normal, rate_training):
    # Planning usa o mesmo valor que as horas normais
    pay_normal = (hours * rate_normal).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    pay_planning = (planning * rate_normal).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    pay_training = (training * rate_training).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return pay_normal + pay_planning + pay_training

def clear_terminal():
    if os.name == 'nt':
        _ = os.system('cls')
    elif os.name == 'posix':
        _ = os.system('clear')

def main():
    print("=== PAYMENT CALCULATOR ===\n")

    teacher_name = input("Teacher's name: ").strip() or "ISABELA"
    print("\nEnter information for both weeks:\n")

    # Current dates and planning rate
    current_date = date.today()
    weekday = int(current_date.strftime("%w"))
    start1 = current_date - timedelta(days= weekday - 1 + 7)
    end1 = start1 + timedelta(days=4)
    start2 = current_date + timedelta(days= weekday - 1)
    end2 = start2 + timedelta(days=4)
    rate_training = Decimal("15")

    # WEEK 1
    print(f"Week 1 ({start1} - {end1})")
    hours1 = to_decimal(input("Hours worked: ").strip())
    planning1 = to_decimal(input("Planning hours: ").strip())
    training1 = to_decimal(input("Training hours: ").strip())
    print()

    # WEEK 2
    print(f"Week 2 ({start2} - {end2})")
    hours2 = to_decimal(input("Hours worked: ").strip())
    planning2 = to_decimal(input("Planning hours: ").strip())
    training2 = to_decimal(input("Training hours: ").strip())
    print()

    # Rates
    print("RATES:")
    rate_normal = to_decimal(input("Normal/Planning rate ($/hour): ").strip())
    print()

    # Extras
    print("EXTRAS:")
    gas = to_decimal(input("Gas ($): ").strip())
    tolls = to_decimal(input("Tolls ($): ").strip())
    print()

    # Calculations
    total_week1 = calc_week(hours1, planning1, training1, rate_normal, rate_training)
    total_week2 = calc_week(hours2, planning2, training2, rate_normal, rate_training)
    subtotal = total_week1 + total_week2
    total = subtotal + gas + tolls

    # Output
    print("=" * 40)
    print(f"{teacher_name.upper()}'S PAYMENT\n")
    print(f"Week {start1} - {end1}")
    print(f"{hours1}h + {planning1}h planning + {training1}h training\n")
    print(f"Week {start2} - {end2}")
    print(f"{hours2}h + {planning2}h planning + {training2}h training\n")
    print(f"+ {format_money(gas)} for gas")
    print(f"+ {format_money(tolls)} for tolls\n")
    print(
        f"TOTAL = {format_money(subtotal)} + {format_money(tolls)} + {format_money(gas)} = {format_money(total)}"
    )
    print("=" * 40)

if __name__ == "__main__":
    while True:
        main()
        decision = input('\nPara sair digite "sair"')
        
        if decision.lower() == 'sair':
            clear_terminal()
            break
        
        clear_terminal()
        