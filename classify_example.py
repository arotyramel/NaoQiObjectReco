import classify_image as classifier

# only required for the example image
import os
import tensorflow as tf

#FLAGS = tf.app.flags.FLAGS

if __name__ == '__main__':
  example_image_path = tf.app.flags.FLAGS.model_dir
  print("example_image_path:", example_image_path)
  image = os.path.join(example_image_path, 'cropped_panda.jpg')
  print(classifier.run_inference_on_image(image)[0])

  #image2 = "220px-Binturong_in_Overloon.jpg"
  #print(classifier.run_inference_on_image(image2)[0])

  #image3 = "6a010535647bf3970b016765cbf839970b-500wi.jpg"
  #print(classifier.run_inference_on_image(image3)[0])
