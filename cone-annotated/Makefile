#
# Annotations in cones.xml were done with Dlib imglab
#

OBJECT_DETECTOR_APP = $(HOME)/Robotics/NeuralNetworks/git-repos/object_detector_app
MODELS = $(HOME)/Robotics/NeuralNetworks/git-repos/models
RACOON_DATASET = $(HOME)/Robotics/NeuralNetworks/git-repos/raccoon_dataset

all:
	echo What

cones.csv: cones.xml ../tools/tocsv.py
	python ../tools/tocsv.py cones.xml > cones.csv

train-set.csv test-set.csv: cones.csv
	../tools/splittext 8 2 < cones.csv
	( echo filename,width,height,class,xmin,ymin,xmax,ymax ; cat set-0 ) > train-set.csv
	( echo filename,width,height,class,xmin,ymin,xmax,ymax ; cat set-1 ) > test-set.csv

tf-train/cone_train.record: train-set.csv
	PYTHONPATH=$(OBJECT_DETECTOR_APP) python $(RACOON_DATASET)/generate_tfrecord.py --csv_input=train-set.csv  --output_path=tf-train/cone_train.record

tf-train/cone_val.record: test-set.csv
	PYTHONPATH=$(OBJECT_DETECTOR_APP) python $(RACOON_DATASET)/generate_tfrecord.py --csv_input=test-set.csv  --output_path=tf-train/cone_val.record

.PHONY: tf-train
tf-train: cone-tf-model/ssd_mobilenet_v1_cone.config cone-tf-model/cone_label_map.pbtxt tf-train/cone_train.record tf-train/cone_val.record 
	PYTHONPATH=$(OBJECT_DETECTOR_APP):$(MODELS)/research/slim \
	python $(OBJECT_DETECTOR_APP)/object_detection/train.py \
		--logtostderr \
		--train_dir=tf-train \
		--pipeline_config_path=cone-tf-model/ssd_mobilenet_v1_cone.config \

freeze:
	python /home/jhanna/.local/lib/python2.7/site-packages/tensorflow/python/tools/freeze_graph.py \
		--input_graph=tf-train/graph.pbtxt \
		--input_checkpoint=tf-train/model.ckpt-163788 \
		--output_graph=frozen_graph.pb \
		--output_node_names=softmax

export: cone-tf-model/ssd_mobilenet_v1_cone.config
	PYTHONPATH=$(OBJECT_DETECTOR_APP):$(MODELS)/research/slim \
	python $(OBJECT_DETECTOR_APP)/object_detection/export_inference_graph.py \
		--input_type image_tensor \
		--pipeline_config_path cone-tf-model/ssd_mobilenet_v1_cone.config \
		--checkpoint_path tf-train/model.ckpt-176848 \
		--inference_graph_path cone_graph.pb

run: cone-tf-model/cone_label_map.pbtxt cone_graph.pb
	python $(OBJECT_DETECTOR_APP)/object_detection_app.py -labels cone-tf-model/cone_label_map.pbtxt -ckpt cone_graph.pb 


fullclean:
	rm -rf tf-train
	rm -f train-set.csv test-set.csv
