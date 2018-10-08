Productize lab deep clean neural network
========================================

This project uses the [Inception V3] neural network for [TensorFlow] machine
learning framework to build a graph model of clean, dirty and busy rooms.

It is based on the [Use Artificial Intelligence to Detect Messy/Clean Rooms!]
guide by Matt Farley, which in term are based on the TensorFlow [image
retraining] and [image recognition] examples.

Usage
-----

### Set-up

Train the neural network, resulting in the graph model and found labels
(best to do this on a fast computer):

```
pip install -r requirements-label.txt
python retrain.py \
    --image_dir $TRAINING_IMAGES \
    --output_graph=deep-clean-graph.pb \
    --output_labels=deep-clean-labels.txt \
    --tfhub_module https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1

```

### Testing

Label a test image. Best practice is to use an image that was not used during
training.

```
python label_image.py \
    --graph=deep-clean-graph.pb \
    --labels=deep-clean-labels.txt \
    --input_layer=Placeholder \
    --output_layer=final_result \
    --image=$IMAGE

```

### Deploying

Install dependencies on a Raspberry Pi:

```
sudo apt install libatlas-base-dev
pip3 install -r requirements-server.txt
```

Run the server:

```
python3 deep-clean-server.py
```

TODO: create a service

[Inception V3]: https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1
[TensorFlow]: https://www.tensorflow.org/
[Use Artificial Intelligence to Detect Messy/Clean Rooms!]: https://www.hackster.io/matt-farley/use-artificial-intelligence-to-detect-messy-clean-rooms-f224a2
[image retraining]: https://github.com/tensorflow/hub/tree/1fa48fe991f22bebf4c8d4cd375eaf0daf5fa937/examples/image_retraining
[image recognition]: https://github.com/tensorflow/tensorflow/tree/9590c4c32dd4346ea5c35673336f5912c6072bf2/tensorflow/examples/label_image
