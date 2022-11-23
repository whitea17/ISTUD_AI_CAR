
# See here for more info on onnx models
# https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-ssd.md
MODEL="models/foot.onnx" # or "models/long_foot.onnx"
MODEL_LABELS="models/labels_for_both_foot_models.txt"

# More ouput options here: 
# https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-streaming.md
# Example OUTPUT_STREAM: OUTPUT_STREAM="rtp://ip_addr_of_pc:5004" 
OUTPUT_STREAM=""
INPUT_CAMERA="--device /dev/video0"

# Same tag used in docker build . -t local/istud_ai_car
CONTAINER_NAME="local/istud_ai_car"


sudo docker run --runtime nvidia -it --rm \
	-v /tmp/argus_socket:/tmp/argus_socket \
	-v /etc/enctune.conf:/etc/enctune.conf \
	--privileged --gpus all \
	-v /proc/device-tree/compatible:/proc/device-tree/compatible \
	-v /proc/device-tree/chosen:/proc/device-tree/chosen \
	-v /sys/devices/:/sys/devices/ \
	-v /sys/class/gpio:/sys/class/gpio \
	$INPUT_CAMERA \
    -e MODEL="$MODEL" \
    -e MODEL_LABELS="$MODEL_LABELS" \
    -e OUTPUT_STREAM="$OUTPUT_STREAM" \
    $CONTAINER_NAME