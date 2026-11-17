
def read_camera():
    """
    Camera monitoring module.

    Hardware is not connected in the current software-only build.
    Returns an explicit unavailable status instead of fake camera data.
    """

    return {
        "status": "UNAVAILABLE - NO CAMERA HARDWARE",
        "stream_available": False,
        "source": "C20 camera / SIYI HM30 integration point",
        "latency_ms": None,
        "note": (
            "A real video stream requires a connected camera, "
            "ground video receiver, and valid stream URL."
        )
    }
