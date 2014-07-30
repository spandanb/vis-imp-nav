from SimpleCV import Kinect

# Initialize the Kinect
kin = Kinect()
# Initialize the display
display = kin.getDepth().show()
# Run in a continuous loop forever
while (True):
    # Snaps a picture, and returns the grayscale depth map
    depth = kin.getDepth()
    # Show the actual image on the screen
    depth.save(display)
