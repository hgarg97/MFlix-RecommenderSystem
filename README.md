# MFlix - Your Movie Recommender

## Overview

MFlix is a movie recommender system designed to assist users in discovering personalized movie recommendations based on their preferences. The system incorporates a user-friendly interface, a sophisticated recommendation algorithm, and an AI-powered chatbot to enhance the movie selection process.

## Features

1. **AI Chatbot Interaction**: Engage with an AI chatbot named CavBot to provide preferences and receive tailored movie recommendations.
2. **Search Functionality**: Search for movies within the database to explore details and receive similar recommendations.
3. **Image Processing for Recommendations**: Utilize image processing techniques to recommend movies based on poster similarity using Image2Vec ResNet-18 Model.
4. **Ratings Based Genre Recommendations**: Genre based top recommendations using the past-user Ratings.
5. **Integration of Multiple Recommendation Algorithms**: Combine content-based, collaborative, matrix factorization, and sentiment analysis-based filtering for accurate recommendations.

## Why MFlix?

- **Enhanced User Experience**: MFlix aims to reduce search time and enhance user satisfaction by providing tailored movie recommendations.
- **Dynamic Recommendations**: Unlike traditional recommender systems, MFlix adapts to dynamic user preferences through chatbot interactions.
- **Innovative Features**: Incorporating image processing and sentiment analysis adds a unique dimension to the recommendation process.

## Data Sources

- MovieLens
- IMDB
- Other publicly available datasets

## Core Algorithms

- BERT for text-based recommendation analysis
- Google Gemini Powered ChatBot Integration
- Image-to-vector
- Matrix factorization
- Content-based filtering
- Collaborative filtering

## Technologies Used

- BERT for text analysis
- ResNet-18 for Image2Vec
- Various recommender system algorithms
- Frontend and backend development tools
- Flask for the UI development
- Gemini API for chatbot integration

## Contributors

- Saptarshi Mondal
- Rahul Gautam
- Harshit Garg
- Kanak Tiwari

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/hgarg97/MFlix-RecommenderSystem.git
   ```

2. Navigate to the project directory:

   ```bash
   cd MFlix-RecommenderSystem
   ```

3. Create a virtual environment (optional but recommended):

   ```bash
   conda create -n mflix python==3.10 -y
   ```

4. Activate the virtual environment:

   On Windows:

   ```bash
   conda activate mflix
   ```

   On macOS and Linux:

   ```bash
   source activate mflix
   ```
