from arl.env import BaseEnv
from arl.policy.modelfree.dqn import DQNPolicy
import torch
import torch.nn.functional as F


class ConvolutionalQNet(torch.nn.Module):
    """加入卷积层的Q网络"""

    def __init__(self, action_dim, in_channels=4):
        super(ConvolutionalQNet, self).__init__()
        self.conv1 = torch.nn.Conv2d(in_channels, 32, kernel_size=8, stride=4)
        self.conv2 = torch.nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv3 = torch.nn.Conv2d(64, 64, kernel_size=3, stride=1)
        self.fc4 = torch.nn.Linear(7 * 7 * 64, 512)
        self.head = torch.nn.Linear(512, action_dim)

    def forward(self, x):
        x = x / 255
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.fc4(x))
        return self.head(x)


class DQNAtariPolicy(DQNPolicy):
    def __init__(self, cfg: dict, env: BaseEnv) -> None:
        super().__init__(cfg, env)

    def set_qnet(self) -> None:
        self.q_net = ConvolutionalQNet(self.action_dim)
