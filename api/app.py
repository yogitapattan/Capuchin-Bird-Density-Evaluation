from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import tensorflow as tf
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense
from itertools import groupby
import os
from tempfile import NamedTemporaryFile
import librosa

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_model():
  model = Sequential()

  model.add(Conv2D(16, 3, activation='relu', input_shape=(1491, 257, 1)))
  model.add(Conv2D(16, 3, activation = 'relu'))
  model.add(Flatten())
  model.add(Dense(32, activation='relu'))
  model.add(Dense(1, activation='sigmoid'))
  model.load_weights('capuchin_audio_classifier_e4_weights.h5')
  return model

def load_mp3_16k_mono(filename):
    audio, _ = librosa.load(filename, sr=16000, mono=True)
    audio = tf.convert_to_tensor(audio, dtype=tf.float32)
    return audio

def preprocess_mp3(sample, index):
  sample = sample[0]
  zero_padding = tf.zeros([48000]-tf.shape(sample), dtype=tf.float32)
  wav = tf.concat([zero_padding, sample], 0)
  spectrogram = tf.signal.stft(wav, frame_length=320, frame_step=32)
  spectrogram = tf.abs(spectrogram)
  spectrogram = tf.expand_dims(spectrogram, axis=2) 
  return spectrogram

def get_density(count):
  if count==0:
     return 'None'
  elif count<5:
     return 'Rare'
  elif count<=10:
     return 'Common'
  else:
     return 'Abundant'

model = get_model()

@app.get("/")
def index():
   return {"message": "Welcome!"}

@app.post("/capuchin")
async def evaluate(file: UploadFile = File(...)):
    # Save the uploaded file to a temporary location
    with NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_filename = tmp.name

    wav = load_mp3_16k_mono(tmp_filename)
    audio_slices = tf.keras.utils.timeseries_dataset_from_array(wav, wav, sequence_length=48000, sequence_stride=48000, batch_size=1)
    audio_slices = audio_slices.map(preprocess_mp3)
    audio_slices = audio_slices.batch(64)

    y_hat = model.predict(audio_slices)
    scores = [1 if prediction > 0.99 else 0 for prediction in y_hat]
    count = tf.math.reduce_sum([key for key, group in groupby(scores)]).numpy()
    density = get_density(count)

    # Delete the temporary file
    os.remove(tmp_filename)

    res =  {
       'capuchin_count': str(count),
       'density': density
    } 
    return res

    
#uvicorn app:app --reload
