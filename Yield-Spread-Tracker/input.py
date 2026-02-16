# input.py

def get_country_pair():
    """
    Captures two countries from the user and ensures they are supported.
    """
    # This list matches the keys in your broker.py COUNTRY_MAP
    SUPPORTED_COUNTRIES = ["US", "UK", "GERMANY", "JAPAN", "AUSTRALIA", "CANADA"]
    
    print("\n" + "="*40)
    print(" YIELD SPREAD TRACKER")
    print("="*40)
    print(f"Supported: {', '.join(SUPPORTED_COUNTRIES)}")
    print("-"*40)

    # Capture Country A
    while True:
        country_a = input("Enter Primary Country (e.g., AUSTRALIA): ").strip().upper()
        if country_a in SUPPORTED_COUNTRIES:
            break
        print(f"❌ Error: {country_a} not supported. Try again.")

    # Capture Country B
    while True:
        country_b = input("Enter Benchmark Country (e.g., US): ").strip().upper()
        if country_b == country_a:
            print("❌ Error: Benchmark must be different from Primary. Try again.")
            continue
        if country_b in SUPPORTED_COUNTRIES:
            break
        print(f"❌ Error: {country_b} not supported. Try again.")

    return country_a, country_b

if __name__ == "__main__":
    # Test run logic
    a, b = get_country_pair()
    print(f"\n✅ Request Registered: {a} vs {b}")