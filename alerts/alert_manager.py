import datetime

def _time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def send_caregiver_alert(fall_type, risk_level):
    print("\n📲 CAREGIVER ALERT")
    print("Time:", _time())
    print("Fall:", fall_type)
    print("Risk:", risk_level)


def send_emergency_alert(fall_type, risk_level):
    print("\n🚨 EMERGENCY ALERT")
    print("Time:", _time())
    print("Fall:", fall_type)
    print("Risk:", risk_level)