import os

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size) -> None:
        super().__init__()

        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=1, padding=1, dilation=1)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=1, kernel_size=3, stride=1, padding=0, dilation=1)

    def forward(self, x, image_input=None):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)

        #image_input = F.relu(self.conv1(image_input))
        #image_input = F.relu(self.conv2(image_input))

        return x
    
    def save(self, file_name="model.pth"):
        model_folder_path = "./model"

        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, lr, gamma) -> None:
        self.lr = lr
        self.gamma = gamma
        self.model = model

        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, game_over):
        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)

        if len(state.shape) == 1:
            # reshape to (1, x)
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            next_state = torch.unsqueeze(next_state, 0)
            game_over = (game_over, )

        # predicted Q values with current state
        pred = self.model(state)
        targ = pred.clone()

        # formula of Q_new = r + y * max(next_pred Q value) if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new

        for idx in range(len(game_over)):
            Q_new = reward[idx]

            if not game_over[idx]:
                Q_new += self.gamma * torch.max(self.model(next_state[idx]))

            targ[idx][torch.argmax(action).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(targ, pred)
        loss.backward()

        self.optimizer.step()
