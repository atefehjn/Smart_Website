import pickle

def load_model():
    model = pickle.load(open('app/model.pkl', 'rb'))
    return model

def prediction(data):
    model = load_model()
    result = model.predict(data)  
    return result
  










