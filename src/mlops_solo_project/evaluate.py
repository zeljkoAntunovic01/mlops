import torch
import typer
from mlops_solo_project.data import corrupt_mnist
from mlops_solo_project.model import Model

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")


def evaluate(model_checkpoint: str) -> None:
    """Evaluate a trained model."""
    print("Evaluating like my life depended on it")
    print(model_checkpoint)

    model = Model().to(DEVICE)
    model.load_state_dict(torch.load(model_checkpoint))

    test_images = torch.load("data/processed/test_images.pt")
    test_target = torch.load("data/processed/test_target.pt")
    test_set = torch.utils.data.TensorDataset(test_images, test_target)
    test_dataloader = torch.utils.data.DataLoader(test_set, batch_size=32)

    model.eval()
    correct, total = 0, 0
    for img, target in test_dataloader:
        img, target = img.to(DEVICE), target.to(DEVICE)
        y_pred = model(img)
        correct += (y_pred.argmax(dim=1) == target).float().sum().item()
        total += target.size(0)
    print(f"Test accuracy: {correct / total}")


if __name__ == "__main__":
    typer.run(evaluate)
