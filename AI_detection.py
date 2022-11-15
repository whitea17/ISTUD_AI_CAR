import jetson.inference
import jetson.utils

import argparse
import sys

# parser for command line args
parser = argparse.ArgumentParser(description="An AI program that is scared of Footwear")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="Output URI for video stream")

# default args used by jetson.inference library
opt_input_URI="v4l2:///dev/video0"
opt_network="ssd-mobilenet-v2"
opt_overlay="box,labels,conf"
# % of confidence required for detection to be detected. 0.5 = 50%
opt_threshold=0.30
opt_threshold_as_str= "--threshold=" + str(opt_threshold) # threshold value must also be included in static args

# more default args, placed here instead of as cli arguments
static_args = ['--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes', '--overlay=box,labels,conf', opt_threshold_as_str]
new_args = [''] # empty str array list

# Attempt to parse cli arguments and splice in static args to sys.argv
try:
	opt = parser.parse_known_args()[0]
	new_args = sys.argv[:3] + static_args + sys.argv[3:]
	print(new_args)

except:
	print("Parsing failed!")
	parser.print_help()
	sys.exit(0)

# create network for footwear detection
aiBrains = jetson.inference.detectNet(opt_network, new_args, opt_threshold)

# input and output sources
input = jetson.utils.videoSource(opt_input_URI, argv=new_args)
output = jetson.utils.videoOutput(opt.output_URI, argv=new_args) # output is not needed, only used for debugging

# main loop
while True:
	# grab next frame
	frame = input.Capture()

	# check frame for footwear
	results = aiBrains.Detect(frame, overlay=opt_overlay)


	# search through all detections for most confident detection
	counter = 0
	most_confident_index = 0
	most_confident_val = -1

	for footwear_obj in results:
		# If the next detection has a higher confidence than the current most c.
		if(footwear_obj.Confidence >= most_confident_val):
			most_confident_index = counter	# set the most_confident_index to current index
			most_confident_val = footwear_obj.Confidence # Update confidence value

		counter = counter + 1 # move for loop index forward by 1
	
	# Check if a footwear object has been detected, (default most_confident_val val. will change if there is a detection)
	if(most_confident_val != -1):
		x_middle_of_frame = frame.width / 2 # find half way point of image in pixels
		x_center_point_of_footwear_detection = results[most_confident_index].Center[0] #results[n].Center format is ('x-val', 'y-val)
		
		# Determine where the most confident object detection is on screen and avoid it
		if(x_center_point_of_footwear_detection > x_middle_of_frame):
			print("Turn left!")
		else:
			print("Turn right!")
	else:
		# No footwear object detection found, moving forward
		print("Drive forward!")


	# render image for debugging purposes
	output.Render(frame)

	# close if video input if it is no longer available
	if not input.IsStreaming():
		break
