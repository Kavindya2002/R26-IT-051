from guidance.live_analyzer import analyze_sensor_state

# =====================================================
# DYNAMIC GUIDANCE SYSTEM
# =====================================================
def run_guidance(sensor_data):

    messages = []

    state = analyze_sensor_state(sensor_data)

    messages.append(
        f"📡 Detected State: {state}"
    )

    # =================================================
    # NO MOVEMENT
    # =================================================
    if state == "no_movement":

        messages.append(
            "🚨 No movement detected"
        )

        messages.append(
            "Emergency services required"
        )

        return "ALERT", messages

    # =================================================
    # SIDE POSITION
    # =================================================
    elif state == "lying_side":

        messages.append(
            "🩺 Roll slowly onto your back"
        )

        messages.append(
            "🩺 Use your arms for support"
        )

        messages.append(
            "🩺 Sit carefully"
        )

        return "GUIDANCE MODE", messages

    # =================================================
    # BACK POSITION
    # =================================================
    elif state == "lying_back":

        messages.append(
            "🩺 Bend your knees slowly"
        )

        messages.append(
            "🩺 Turn to your side"
        )

        messages.append(
            "🩺 Push upward carefully"
        )

        return "GUIDANCE MODE", messages

    # =================================================
    # SITTING
    # =================================================
    elif state == "sitting":

        messages.append(
            "✅ Sitting position detected"
        )

        messages.append(
            "🩺 Stand slowly using support"
        )

        return "RECOVERING", messages

    # =================================================
    # STANDING
    # =================================================
    elif state == "standing":

        messages.append(
            "✅ Patient standing successfully"
        )

        messages.append(
            "Recovery complete"
        )

        return "RECOVERY SUCCESS", messages

    # =================================================
    # UNKNOWN
    # =================================================
    else:

        messages.append(
            "⚠ Unable to determine body position"
        )

        return "UNKNOWN", messages