import requests
import os

# Define the URL of the API endpoint
url = "http://127.0.0.1:8000/api"

# Define class labels
class_labels = []
class_argmax = []

for filename in os.listdir("Test"):
    # Load an image file to send to the API
    image_path = os.path.join("Test", filename)
    class_labels.append(filename.split(".")[0])

    with open(image_path, "rb") as file:
        image_bytes = file.read()

    # Send a POST request to the API endpoint with the image data
    response = requests.post(url, files={"image": image_bytes})
    result = response.json()

    # Get the predicted class label
    class_argmax.append(result.get("argmax"))

    """
    predicted_probabilities = predictions[0].numpy()
    labels = [label.numpy().decode('utf-8') for label in predictions[1]]

    # Find the index of the maximum probability
    predicted_index = np.argmax(predicted_probabilities)

    # Get the corresponding label
    predicted_label = labels[predicted_index]

    # Print the predicted label
    print(f'Predicted label: {predicted_label}')
    """


    # Print the response
    print(result.get("argmax"))

# Print the class labels
print(class_labels)
print(class_argmax)
