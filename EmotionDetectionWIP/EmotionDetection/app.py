from detector import Detector
import sys

arg = sys.argv[1]
detector = Detector(arg)
detector.capture_video(1000)