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

	# print out all detections
	for footwear_obj in results:
		print(footwear_obj)

	# render image for debugging purposes
	output.Render(frame)

	# close if video input if it is no longer available
	if not input.IsStreaming():
		break
