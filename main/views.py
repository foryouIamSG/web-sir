from django.shortcuts import render, redirect
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from PIL import Image
import torch
from torchvision import transforms
from .forms import MyModelForm
import random
from huggingface_hub import InferenceClient
from io import BytesIO
from django.http import JsonResponse
import base64
from django.shortcuts import render
import os
import requests
from django.middleware.csrf import get_token

class_names = {
    0: 'Академизм',
    1: 'Барокко',
    2: 'Кубизм',
    3: 'Экспрессионизм',
    4: 'Японское искусство',
    5: 'Неоклассицизм',
    6: 'Поп-арт',
    7: 'Примитивизм',
    8: 'Реализм',
    9: 'Ренессанс',
    10: 'Рококо',
    11: 'Романтизм',
    12: 'Символизм'
}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_file = "main/static/main/models/efinet-bestloss.pth"
weights_file = "main/static/main/models/weights.pth"

def load_model_from_file(model_file, weights_file, device):
    model = torch.load(model_file, map_location=device)
    model.load_state_dict(torch.load(weights_file, map_location=device))
    model.eval()
    return model

model = load_model_from_file(model_file, weights_file, device)

def classify_image(model, image_file, class_names, device):
    image = Image.open(image_file)

    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        probabilities = torch.nn.functional.softmax(output, dim=1)[0]
        predicted_class_index = torch.argmax(probabilities).item()
        predicted_class_name = class_names.get(predicted_class_index)

    return predicted_class_name

def create_palette(image):
    image_array = np.array(image)
    reshaped_image_array = image_array.reshape(-1, 3)
    kmeans = MiniBatchKMeans(n_clusters=10, random_state=0)
    kmeans.fit(reshaped_image_array)
    colors = kmeans.cluster_centers_
    colors = colors.astype(int)
    return colors



def index(request):
    class_result = None
    palette = None
    random_items = None
    generated_image_pil = None

    if request.method == 'POST':
        form = MyModelForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            class_result = classify_image(model, image_file, class_names, device)
            if class_result:
                class_result = f"Класс изображения: {class_result}"
                image = Image.open(image_file)
                palette = create_palette(image)
                palette = palette.tolist()
            return render(request, 'main/index.html', {'form': form, 'palette': palette, 'class_result': class_result})

    else:
        form = MyModelForm()



    if 'action' in request.POST:
        action = request.POST['action']
        if action == 'generate_items':
            # Ваш список предметов
            items_list = ["apple", "cat", "George Washington", "rainbow", "pizza", "Mars", "coffee", "elephant", "football", "piano",
"star", "Vincenzo Gemito", "butterfly", "guitar", "Shakespeare", "wolf", "waterfall", "magnolia", "basketball",
"bird", "bear", "Sherlock Holmes", "banana", "starfish", "cosmos", "bear", "Mona Lisa", "painting",
"turtle", "book", "Font of Time", "sand", "lightning", "lion", "Picasso", "vodka", "dolphin", "computer",
"stone", "dragon", "oil", "cabbage", "mountain", "moon", "bee", "jazz", "eagle", "honey", "cardboard",
"phoenix", "clock", "sun", "lemon", "bar", "music", "cosmonaut", "orchid", "ship", "owl", "sound",
"dream", "fountain", "crocodile", "snow", "stargazer", "bank", "ink", "beauty", "penguin", "Martina Navratilova",
"camera", "potato", "George Orwell", "snail", "comet", "mouse", "machine", "ballet", "chocolate", "cat",
"laughter", "parrot", "fire", "flower", "house", "Vladimir Nabokov", "planet", "piano", "Mercury", "fox",
"drops", "fern", "doll", "magic", "bread", "gravity", "phone", "cookies", "Galileo Galilei",
"wave", "Alexander Solzhenitsyn", "horse", "flamingo", "water", "snowman", "nut", "fantasy", "sky", "joy", "mandarin", "James Dean", "ladder", "snake", "orangutan", "lantern", "kettle",
"ice cream", "rose", "paper", "Stefan Zweig", "film", "ant", "word", "lemonade", "bridge", "Milton Erickson",
"spice", "parachute", "sea", "tea", "whale", "harmony", "dog", "drawing", "tree", "book",
"mirror", "dove", "detective", "John Lennon", "sand", "fox", "Milton Friedman", "galaxy", "hill",
"steam locomotive", "palm tree", "sailboat", "car", "rose", "money", "cello", "fruit", "air", "guitar",
"elephant", "chocolate", "bird", "football", "orchid", "dragon", "coffee", "pizza", "cappuccino", "bee",
"joy", "cow", "paint", "jazz", "city", "giraffe", "rain", "cinema", "grandma", "sunshine",
"paper", "mushroom", "champion", "milk", "painting", "spaceship", "prince", "money", "queen", "raincoat",
"chair", "sound", "bird", "mushroom", "stone", "pigeon", "king", "pear", "computer", "lily", "university", "pearl", "friendship", "jeep", "smartphone", "cocktail", "tulip", "perfection", "starfall",
"carnation", "doggie", "robot", "beauty", "hockey", "planet", "T-shirt", "second", "word", "bus",
"canoe", "pillow", "keyboard", "smartphone", "kettle", "TV", "orange", "helicopter", "tractor", "spider",
"card", "pizza", "candy", "pie", "schoolboy", "mom", "dad", "pool", "candy"]
            # Генерируем случайные предметы
            random_items = random.sample(items_list, 3)

    return render(request, 'main/index.html', {'form': form, 'random_items': random_items})



