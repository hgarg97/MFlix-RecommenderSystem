# MFlix - Your Movie Recommender

## Overview

MFlix is a movie recommender system designed to assist users in discovering personalized movie recommendations based on their preferences. The system incorporates a user-friendly interface, a sophisticated recommendation algorithm, and an AI-powered chatbot to enhance the movie selection process.

## Features

1. **AI Chatbot Interaction**: Engage with an AI chatbot to provide preferences and receive tailored movie recommendations.
2. **Top 5 Recommendations**: Display personalized movie recommendations based on the user's preferences and historical data.
3. **Search Functionality**: Search for movies within the database to explore details and receive similar recommendations.
4. **Image Processing for Recommendations**: Utilize image processing techniques to recommend movies based on poster similarity (Subject to data availability).
5. **Sentiment Analysis-based Recommendations**: Analyze movie reviews to provide recommendations based on positive and negative sentiments.
6. **Integration of Multiple Recommendation Algorithms**: Combine content-based, collaborative, matrix factorization, and sentiment analysis-based filtering for accurate recommendations.

## Why MFlix?

- **Enhanced User Experience**: MFlix aims to reduce search time and enhance user satisfaction by providing tailored movie recommendations.
- **Dynamic Recommendations**: Unlike traditional recommender systems, MFlix adapts to dynamic user preferences through chatbot interactions.
- **Innovative Features**: Incorporating image processing and sentiment analysis adds a unique dimension to the recommendation process.

## Data Sources

- IMDB
- MovieLens
- Other publicly available datasets

## Core Algorithms

- BERT for text-based recommendation analysis
- Content-based filtering
- Collaborative filtering
- Matrix factorization
- Image-to-vector
- Sentiment analysis

## Technologies Used

- BERT for text analysis
- Various recommender system algorithms
- Frontend and backend development tools
- Flask or Django for the UI development
- Gemini API for chatbot integration

## Demonstration

We will provide a live demonstration of the MFlix website during the presentation. Additionally, we may conduct a satisfaction survey to gather feedback from users.

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
