import gym
env = gym.make('MountainCar-v0')
f = open('file2.txt', 'w')

#need expert
for i_episode in range(20):
    observation = env.reset()
    for t in range(100):
        env.render()
        f.write(str(observation[0])+','+str(observation[1])+',')
        action = env.action_space.sample()
        f.write(str(action))
        f.write('\n')
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break

f.close()
