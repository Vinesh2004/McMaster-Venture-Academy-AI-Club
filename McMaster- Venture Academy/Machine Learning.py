import matplotlib.pyplot as plt
from detecto import core, utils, visualize

image = utils.read_image('orange.jpg')
plt.imshow(image)
plt.show()

model = core.Model()

labels,boxes,scores = model.predict_top(image)
visualize.show_labeled_image(image, boxes, labels)

print(labels)
print(boxes)
print(scores)