import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

def train(env):
	'''Train a tabular q agent to learn the behavior for the required environment
	params: env - the game environment
	return:
			agent - the trained agent'''

	np.random.seed(123)
	env.seed(123)
	nb_actions = env.action_space.n

	# Next, we build a very simple model.
	model = Sequential()
	model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
	model.add(Dense(16))
	model.add(Activation('relu'))
	model.add(Dense(16))
	model.add(Activation('relu'))
	model.add(Dense(16))
	model.add(Activation('relu'))
	model.add(Dense(nb_actions))
	model.add(Activation('linear'))
	print(model.summary())

	memory = SequentialMemory(limit=50000, window_length=1)
	policy = BoltzmannQPolicy()
	dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10,
	               target_model_update=1e-2, policy=policy)
	dqn.compile(Adam(lr=1e-3), metrics=['mae'])

	# Okay, now it's time to learn something! We visualize the training here for show, but this
	# slows down training quite a lot. You can always safely abort the training prematurely using
	# Ctrl + C.
	dqn.fit(env, nb_steps=500000, visualize=False, verbose=1)

	dqn.test(env, nb_episodes=5, visualize=True)

	return dqn

def generate(agent, env, number_of_traces):
	'''Takes a trained agent and plays the game in the given environment, and writes the expert traces to a file.
	params: agent - trained agent
			env - the game environment
	return:
			none
	'''

	for n in range(number_of_traces):
		filename = 'file'+n+'.txt'
		f = open(filename, 'w')

		#need expert
		for i_episode in range(20):
		    observation = env.reset()
		    for t in range(100):
		        env.render()
		        for i in range(len(observation)):
		        	f.write(str(observation[i])+',')
		        #action = env.action_space.sample()
		        action = agent.act(observation,eps=1)
		        f.write(str(action))
		        f.write('\n')
		        observation, reward, done, info = env.step(action)
		        if done:
		            print("Episode finished after {} timesteps".format(t+1))
		            break

		f.close()

if __name__ == '__main__':
	number_of_traces = 1
	env = gym.make('CartPole-v0')
	agent = train(env)
	#generate(agent, env, number_of_traces)



