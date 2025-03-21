# HomeTeam-AI-Code-Challenge

Code challenge for the position AI Engineer at HomeTeam.

---

# How to reproduce the solution

## First Step

Clone this repo 
``` bash
git clone git@github.com:FranSPG/HomeTeam-AI-Code-Challenge.git
cd HomeTeam-AI-Code-Challenge 
```

---

## Second step
``` bash
docker-compose build 
```
![step_1.png](docs_images/step_1.png)
---

## Third step
``` bash
docker-compose up 
```
![step_2.png](docs_images/step_2.png)

## Fourth step
Open the following link with your browser:

http://localhost/docs#/default/process_video_process_video__post


## Fifth step
Click the 'Try Out' button and fill up the parameters

![step_5.png](docs_images/step_5.png)

Once the process is finished you will get a link to download the processed video to your local machine.


---
# My approach

I decided to design a continuous operational pipeline with a production-first mindset, 
prioritizing how the model would be deployed and used in the real world rather than focusing solely on the model itself.
For the model, I opted for the out-of-the-box YOLOv11m model,
as my experience suggested that it would provide an acceptable level of performance 
for the sample video provided. I wanted to avoid over-engineering the model and instead, 
focused on other critical aspects of the solution. Of course, there’s always room for improvement
from the model’s perspective. For instance, adjusting confidence thresholds, using masks to prevent 
detections in undesired areas, and fine-tuning the model with annotated data specific to this kind of 
fisheye-like camera would likely improve detection accuracy in this particular case.

To serve the model, I chose NVIDIA Triton Inference Server. 
This choice allows me to easily abstract away the model management from the code, 
providing a scalable, efficient, and production-ready environment to serve the model,
enabling smooth inference operations.

For the API, I leveraged FastAPI because of its integration with Swagger.
This gave me an easy way to expose an endpoint with a user-friendly interface,
allowing for fast iterations and testing with different videos, frame rates, and resolution configurations.

I packaged everything using Docker and managed the containers with a Docker Compose file.
This setup streamlines deployment and makes it easy to manage dependencies and configuration.

---
# Future improvements
- Place the camera higher to get a clearer view of the field and players. This adjustment will allow the model to detect the ball and people more easily, improving overall accuracy and performance. By providing a better angle, the model will have fewer occlusions and clearer frames to work with.
- Create a custom dataset specifically for this type of camera. Open-source models are typically trained on images captured with standard lenses, not fisheye-like cameras. Since the visual distortion in fisheye images can affect detection, having a dataset tailored to this camera type would allow the model to learn its unique characteristics. Fine-tuning the model with such data could significantly improve its detection capabilities in these specific conditions.
- Optimize the FastAPI implementation, particularly the handling of uploaded files. Right now, the process for managing and storing uploaded videos feels a bit messy. Streamlining this part of the code, possibly by adding proper validation and efficient file storage mechanisms, will make the API more robust and user-friendly.


