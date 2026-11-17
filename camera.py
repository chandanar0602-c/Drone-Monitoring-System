def read_camera():
    # No physical camera or SIYI video receiver is connected in this build.
    return {"status": "UNAVAILABLE – NO CAMERA HARDWARE",
            "stream_available": False,
            "source": "C20 camera / SIYI HM30 integration point",
            "latency_ms": None,
            "note": "A real video stream requires the ground video receiver and stream URL."}
