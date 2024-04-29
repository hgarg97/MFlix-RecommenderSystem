# MFlix - Your Movie Recommender

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/hgarg97/MFlix-RecommenderSystem.git
   ```

2. Navigate to the project directory:

   ```bash
   cd MFlix-RecommenderSystem/src
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Flask Application

1. Make sure you are in the `mflix-app` directory.

   ```bash
   cd mflix-app
   ```

2. Run the Flask application:

   ```bash
   python app.py
   ```

3. Open your web browser and navigate to `http://127.0.0.1:5000/` to access the application.

## Installing Embeddings and Movie Details Data

To use pre-trained embeddings and movie details data, follow these steps:

1. Download the pre-trained embeddings from the provided Google Drive link: [Embeddings](https://drive.google.com/drive/folders/1Pz1mdHde2f7k1ODr8QlKTshbVzgz9jJR?usp=sharing).

2. Once downloaded, copy the files and paste them into the `static` folder of the MFlix-RecommenderSystem/src/mflix-app project directory.

3. Download the `Movies_Details.csv` file from the provided Google Drive link: [Movies_Details.csv](https://drive.google.com/file/d/1w9Vr9wNvhlhzmBCPbJpE5YzsnMvpbk9q/view?usp=drive_link).

4. Copy the downloaded `Movies_Details.csv` file and paste it into the `static` folder of the MFlix-RecommenderSystem/src/mflix-app project directory.

5. The embeddings and movie details data will now be available for use within the Flask application.
