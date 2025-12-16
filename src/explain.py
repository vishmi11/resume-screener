import numpy as np

def get_top_keywords(text, model, vectorizer, top_n=10):
    # Transform resume text
    tfidf_vector = vectorizer.transform([text])

    # Get predicted class index
    class_index = model.predict(tfidf_vector)[0]
    class_idx = list(model.classes_).index(class_index)

    # Get feature names
    feature_names = vectorizer.get_feature_names_out()

    # Get coefficients for this class
    class_weights = model.coef_[class_idx]

    # Calculate contribution score
    contributions = tfidf_vector.toarray()[0] * class_weights

    # Get top positive contributors
    top_indices = np.argsort(contributions)[-top_n:][::-1]

    top_keywords = [
        feature_names[i]
        for i in top_indices
        if contributions[i] > 0
    ]

    return top_keywords
