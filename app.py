from flask import Flask,render_template,request, redirect
from sklearn.cluster import MiniBatchKMeans
from werkzeug.utils import secure_filename
import os
from skimage import io
import time
import numpy as np
app = Flask('__name__')
app.config["IMAGE_UPLOADS"] ="./static/images/"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/comprehension", methods=["GET", "POST"])
def FileUpload():       
    k= request.form.get('number')
    if request.method == "POST":
        k= request.form.get('number')
        if request.files:

            image = request.files["image"]

            if image.filename == "":
                print("No filename")
                return redirect('/')

            if allowed_image(image.filename) and k!=None:
                
                i=0
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], str(i)+".jpg"))
                
                input_img = io.imread('./static/images/0.jpg')
                img_data = (input_img / 255.0).reshape(-1, 3)
                #minibtach K means.
                kmeans = MiniBatchKMeans(int(k)).fit(img_data)

                k_colors = kmeans.cluster_centers_[kmeans.predict(img_data)]
                #k centers into colors 
                k_img = np.reshape(k_colors, (input_img.shape))
            
                io.imsave("./static/compressed/compressed-0.jpg",k_img)
                print("Image saved")

                return render_template('image_comprehension.html',k=k)

            else:
                print("That file extension is not allowed")
                return render_template('image_comprehension.html',k=k)
            try:
                os.remove("./static/compressed/compressed-0.jpg")
            except OSError:
                pass
        print(k)
        return render_template('image_comprehension.html',k=k)
    return render_template('image_comprehension.html',k=k)

if __name__ == "__main__":

    app.run(debug=True)
