from system import FallSystem

def main():

    system = FallSystem()

    # =========================
    # SAMPLE INPUT (timestamp data replaced by batch)
    # =========================

    fall_50 = [[0.1]*11 for _ in range(50)]
    type_80 = [[0.2]*11 for _ in range(80)]

    risk_data = {
        "RiskScore": [0.92],
        "Age": [82],
        "PreviousFalls": [6],
        "Location": ["bathroom"],
        "Time": ["night"],
        "Movement": ["unstable"],
        "AssistiveDevice": ["no"]
    }

    result = system.predict(fall_50, type_80, risk_data)

    print("\n================ FINAL RESULT ================")
    print(result)
    print("==============================================")


if __name__ == "__main__":
    main()