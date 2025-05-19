from tqdm import tqdm


def train_unet(model, dataloader, optimizer, criterion, device):
    model.train()
    running_loss = 0.0
    for images, masks in tqdm(dataloader, desc="Training Batch"):  
        images, masks = images.to(device), masks.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, masks)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    return running_loss / len(dataloader)


def main():
    # 데이터 경로
    train_image_dir = "/kaggle/input/qweqras/train/images"
    train_mask_dir = "/kaggle/working/train_mask2"


    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor()
    ])


    train_dataset = FireSegmentationDataset(train_image_dir, train_mask_dir, transform)
    train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)


    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = UNet().to(device)
    criterion = nn.BCEWithLogitsLoss()  # 이진 크로스엔트로피
    optimizer = optim.Adam(model.parameters(), lr=1e-4)


    num_epochs = 20
    for epoch in range(num_epochs):
        loss = train_unet(model, train_loader, optimizer, criterion, device)
        print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {loss:.4f}", flush=True)
    

    torch.save(model.state_dict(), "unet_model.pth")
    print("Model saved to unet_model.pth")

if __name__ == "__main__":
    main()
