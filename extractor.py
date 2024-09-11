
import torch
import torchvision.models as models
import torchvision.transforms as transforms

class FeatureExtractor:
    def __init__(self, model="resnet50"):

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        if model == "resnet18":
            self.model = models.resnet18(pretrained=True)
        elif model == "resnet34":
            self.model = models.resnet34(pretrained=True)
        elif model == "resnet50":
            self.model = models.resnet50(pretrained=True)
        elif model == "resnet101":
            self.model = models.resnet101(pretrained=True)
        elif model == "resnet152":
            self.model = models.resnet152(pretrained=True)
        else:
            print("Model not found!")

        self.model.eval()
        self.model = self.model.to(self.device)

        self.preprocess = transforms.Compose([
            transforms.Resize(256),              
            transforms.CenterCrop(224),          
            transforms.ToTensor(),               
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), 
        ])

    
    def extract_features(self, image):

        image = self.preprocess(image)
        image = image.to(self.device)

        features = self.model(image).detach().cpu().numpy()

        return features

