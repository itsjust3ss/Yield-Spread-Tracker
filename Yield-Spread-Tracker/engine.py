# main.py
import broker, maths

print("--- YIELD SPREAD TRACKER ---")
c1 = input("Enter Country A (e.g., AUSTRALIA): ").upper()
c2 = input("Enter Country B (e.g., US): ").upper()

# 1. Fetch data for both
data_a = broker.fetch_yield(c1)
data_b = broker.fetch_yield(c2)

# 2. Analyze
if data_a is not None and data_b is not None:
    maths.calculate_ird_signal(data_a, data_b, c1, c2)
else:
    print("Invalid Country Selection. Check MAPPING in broker.py")