from guidance.controller import run_guidance
from alerts.alert_manager import (
    send_caregiver_alert,
    send_emergency_alert
)

# =====================================================
# FINAL DECISION ENGINE
# =====================================================
def final_decision(
    activity,
    fall_type,
    risk_level,
    sensor_data
):

    print("\n===== DECISION ENGINE =====")

    # =================================================
    # SAFE
    # =================================================
    if activity != "fall":

        return {

            "status": "SAFE",

            "guidance": [
                "🟢 No fall detected"
            ]
        }

    # =================================================
    # HIGH RISK
    # =================================================
    if risk_level == "high":

        send_emergency_alert(
            fall_type,
            risk_level
        )

        return {

            "status": "EMERGENCY ALERT",

            "guidance": [

                "🚨 Emergency alert triggered",
                "Medical assistance required immediately"
            ]
        }

    # =================================================
    # MEDIUM RISK
    # =================================================
    if risk_level == "medium":

        send_caregiver_alert(
            fall_type,
            risk_level
        )

        return {

            "status": "CAREGIVER ALERT",

            "guidance": [

                "📲 Caregiver notified",
                "Please remain calm",
                "Avoid sudden movement",
                "Help is on the way"
            ]
        }

    # =================================================
    # LOW RISK → DYNAMIC GUIDANCE
    # =================================================
    if risk_level == "low":

        guide_status, guide_messages = run_guidance(
            sensor_data
        )

        return {

            "status": guide_status,

            "guidance": guide_messages
        }

    # =================================================
    # UNKNOWN
    # =================================================
    return {

        "status": "UNKNOWN",

        "guidance": [
            "⚠ Unknown system state"
        ]
    }