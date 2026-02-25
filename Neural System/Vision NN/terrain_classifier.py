import torch
import torchvision.transforms as T
from PIL import Image
from torchvision import models

class TerrainClassifier:
    def __init__(self, device=None):
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = models.resnet50(num_classes=365)
        checkpoint = torch.hub.load_state_dict_from_url(
            "http://places2.csail.mit.edu/models_places365/resnet50_places365.pth.tar",
            progress=True
        )
        self.model.load_state_dict(checkpoint["state_dict"])
        self.model = self.model.to(self.device)
        self.model.eval()

        self.transform = T.Compose([
            T.Resize((224,224)),
            T.ToTensor(),
            T.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
        ])

        with open("categories_places365.txt") as f:
            self.scene_labels = [line.strip().split(" ")[0] for line in f]

    def predict(self, frame):
        image = Image.fromarray(frame)
        x = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(x)
            _, pred = outputs.max(1)

        scene = self.scene_labels[pred.item()]
        return {"scene": scene}
