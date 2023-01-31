import torch
import torchvision
import torchreid

model = torchreid.models.build_model(
    name='resnet50',
    num_classes=2,
    loss='softmax',
    pretrained=True,
    use_gpu=True)
torchreid.utils.load_pretrained_weights(model, "mobilenetv2_1.4-bc1cc36b.pth")
model.eval()
example = torch.rand(1, 3, 320, 480)
traced_script_module = torch.jit.trace(model, example)
traced_script_module.save("model.pt")