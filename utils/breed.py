from tensorflow import keras
import numpy as np
import json

try:
    with open('models/class_names.json', 'r') as f:
        CLASS_NAMES = json.load(f)
except:
    print("Warning: class_names.json not found")
    CLASS_NAMES = []

def create_model():
    try:
        print("Loading saved model...")
        return keras.models.load_model('models/breed.h5')
    except:
        print("Couldn't load model, building new one...")
        
        base_model = keras.applications.EfficientNetB3(
            include_top=False,
            weights='imagenet',
            input_shape=(300, 300, 3)
        )
        
        x = base_model.output
        x = keras.layers.GlobalAveragePooling2D()(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.Dropout(0.5)(x)
        
        x = keras.layers.Dense(512, activation='relu')(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.Dropout(0.5)(x)
        
        x = keras.layers.Dense(256, activation='relu')(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.Dropout(0.3)(x)
        
        predictions = keras.layers.Dense(120, activation='softmax')(x)
        
        model = keras.Model(inputs=base_model.input, outputs=predictions)
        
        model.compile(
            optimizer=keras.optimizers.Adam(1e-4),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model

def preprocess_image(image):
    resized = image.resize((300, 300))
    img_array = keras.preprocessing.image.img_to_array(resized)
    img_array = np.expand_dims(img_array, axis=0)
    return keras.applications.efficientnet.preprocess_input(img_array)

def get_prediction(model, image):
    predictions = model.predict(image)
    top_idx = np.argmax(predictions[0])
    confidence = float(predictions[0][top_idx] * 100)
    
    breed_name = CLASS_NAMES[top_idx]
    clean_breed = breed_name.split('-')[-1].replace('_', ' ').title()

    if confidence >= 90:
        confidence_level = "Very High"
    elif confidence >= 70:
        confidence_level = "High" 
    elif confidence >= 50:
        confidence_level = "Moderate"
    elif confidence >= 30:
        confidence_level = "Low"
    else:
        confidence_level = "Very Low"

    if int(confidence) < 75:
        clean_breed = "Mixed Breed"
    
    return {
        "breed": clean_breed,
        "confidence": f"{confidence:.2f}%",
        "confidence_level": confidence_level
    }

