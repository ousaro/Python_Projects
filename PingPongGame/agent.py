import random
import torch
from collections import deque
from PingPongAI import PingPongGame
import numpy as np
from model import Linear_QNet, QTrainer
from helper import plot


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:

    def __init__(self):
        self.nb_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate <1
        self.memory = deque(maxlen=MAX_MEMORY) # popleft() if the size is exeeded
        self.model = Linear_QNet(7,256,3)
        self.trainer = QTrainer(self.model,lr=LR,gamma=self.gamma)

    def get_state(self, game):

        player_dir_u = game.playerDirection == "Up"
        player_dir_d = game.playerDirection == "Down"

        dir_u = game.opponentDirection == "Up"
        dir_d = game.opponentDirection == "Down"



        states = [
            # danger
            game.ball.rect.x + game.ball.width >= game.screen_width,
            #player position
                #up
            game.player1.rect.y < game.player2.rect.y,

                # down
            game.player1.rect.y > game.player2.rect.y,


            #move direction
            dir_u,
            dir_d,

            # ball postion
            game.ball.rect.y < game.player2.rect.y, # ball up
            game.ball.rect.y > game.player2.rect.y + game.player2.height  # down down
        ]

        return np.array(states, dtype=int)

    def remember(self, state, action, reward, new_state, gameover):
        self.memory.append((state, action, reward, new_state, gameover))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, new_states, gameovers= zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, new_states, gameovers)

    def train_short_memory(self, state, action, reward, new_state, gameover):
        self.trainer.train_step(state, action, reward, new_state, gameover)

    def get_action(self, state):
        # random moves: tradeoff explotraion / exploitation
        self.epsilon = 80 - self.nb_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon: # to make a random moves in the first few games
            move_idx = random.randint(0,1)
            final_move[move_idx] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            # to get the index of the max ele and make it 1 (item is used to make the tensor one element)
            move_idx = torch.argmax(prediction).item()
            final_move[move_idx] =1

        return final_move

def train():
    plot_score = []
    plot_mean_score = []
    total_score = 0
    record = 0
    agent = Agent()
    game = PingPongGame()
    while True:

        #get old state
        state_old = agent.get_state(game)

        #get move
        final_move = agent.get_action(state_old)

        #perform move and get new state
        reward, gameover, score = game.Play_Step(final_move)
        state_new= agent.get_state(game)

        #train short memory
        agent.train_short_memory(state_old,final_move,reward,state_new,gameover)

        # remember
        agent.remember(state_old, final_move, reward, state_new, gameover)

        if gameover:
            # train long memory, plot result
            game.restart()
            agent.nb_games +=1
            agent.train_long_memory()

            if score>record:
                record= score
                agent.model.save()

            print("Game",agent.nb_games, "Score", score, "Record",record)

            plot_score.append(score)
            total_score += score
            mean_score = total_score/agent.nb_games
            plot_mean_score.append(mean_score)
            plot(plot_score,plot_mean_score)


if __name__ == "__main__":
    train()