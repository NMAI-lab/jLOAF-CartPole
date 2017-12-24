import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

def train(env, test =False):
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
	dqn.fit(env, nb_steps=100000, visualize=False, verbose=1)

	if test:
		dqn.test(env, nb_episodes=5, visualize=False)

	return dqn

def generate(agent, env, number_of_traces, visualize = False):
	'''Takes a trained agent and plays the game in the given environment, and writes the expert traces to n file.
	params: agent - trained agent
			env - the game environment
			number_of_traces - the number of games to run and get traces of
	return:
			none
	'''

	for n in range(number_of_traces):
		filename = 'file'+str(n)+'.txt'
		f = open(filename, 'w')

		#need expert
		for i_episode in range(5):
			observation = env.reset()
			s=''
			for t in range(200):
				if visualize:
					env.render()
				for i in range(len(observation)):
					s+=str(observation[i])
					s+=','
				#action = env.action_space.sample()
				action = agent.forward(observation)
				s+=str(action)
				s+='\n'
				observation, reward, done, info = env.step(action)
				if done:
					print("Episode finished after {} timesteps".format(t+1))
					break
			if t == 199:
				print('writing to file...')
				f.write(s)
				print('done')
		f.close()

if __name__ == '__main__':
	number_of_traces = 10
	env = gym.make('CartPole-v0')
	agent = train(env, test = True)
	agent.training = False
	generate(agent, env, number_of_traces)



