from TicTacToeEnv import TicTacToe
import tensorflow as tf
import numpy as np

# This code aims to build a Policy based agent based heavily on a tutorial by Arthur Juliani on Medium
# That article can be found at https://medium.com/@awjuliani/super-simple-reinforcement-learning-tutorial-part-2-ded33892c724

# Boiler plate code to make graph formation and visualization easy
def fc_layer(input, size_in, size_out, name="fc", activation="relu"):
  print(name+":"+str(size_in)+","+str(size_out))
  with tf.name_scope(name):
    w = tf.Variable(tf.truncated_normal([size_in, size_out], stddev=0.1), name="W")
    b = tf.Variable(tf.constant(0.1, shape=[size_out]), name="B")
    logits = tf.matmul(input, w) + b
    act = eval("tf.nn.{}(logits)".format(activation))
    #tf.summary.histogram("weights", w)
    #tf.summary.histogram("biases", b)
    #tf.summary.histogram("activations", act)
    return act

gamma = 0.99

def discount_rewards(r):
    """ take 1D float array of rewards and compute discounted reward """
    discounted_r = np.zeros_like(r)
    running_add = 0
    for t in reversed(range(0, r.size)):
        running_add = running_add * gamma + r[t]
        discounted_r[t] = running_add
    return discounted_r


class PolicyGradient:

    def __init__(self, learning_rate, num_positions, num_actions, num_hidden):
        # Establish the feedforward network for the policy agent

        # Input for state
        self.state_in = tf.placeholder(shape=[None,num_positions], dtype=tf.float32)
        # Hidden layer for increase complexity in network
        hidden = fc_layer(input=self.state_in, size_in=num_positions, size_out=num_hidden, name="fc1")
        # Output layer of network
        self.output = fc_layer(input=hidden, size_in=num_hidden, size_out=num_actions, name="fc2", activation="softmax")
        # Chosen action after computation (highes in the output vector along axis 1)
        self.chosen_action = tf.argmax(self.output,1)

        # Training process

        # Holding the reward gotten
        self.reward_holder = tf.placeholder(shape=[None],dtype=tf.float32)
        # Holding the action taken
        self.action_holder = tf.placeholder(shape=[None],dtype=tf.int32)
        # Getting the output values from the network that cause the agent to take the actions that it did for each state
        self.indexes = tf.range(0, tf.shape(self.output)[0]) * tf.shape(self.output)[1] + self.action_holder
        self.responsible_outputs = tf.gather(tf.reshape(self.output, [-1]), self.indexes)
        # Qualified loss based on resulting reward_holder
        self.loss = -tf.reduce_mean(tf.log(self.responsible_outputs)*self.reward_holder)

        tvars = tf.trainable_variables()
        self.gradient_holders = []
        for idx,var in enumerate(tvars):
            placeholder = tf.placeholder(tf.float32,name=str(idx)+'_holder')
            self.gradient_holders.append(placeholder)
        self.gradients = tf.gradients(self.loss,tvars)
        optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
        self.update_batch = optimizer.apply_gradients(zip(self.gradient_holders,tvars))

if __name__ == "__main__":
    env = TicTacToe()

    tf.reset_default_graph() #Clear the Tensorflow graph.

    myAgent = PolicyGradient(learning_rate=1e-2,num_positions=9,num_actions=9,num_hidden=20) #Load the agent.

    total_episodes = 5000 #Set total number of episodes to train agent on.
    update_frequency = 5

    init = tf.global_variables_initializer()

    # Launch the tensorflow graph
    with tf.Session() as sess:
        sess.run(init)
        i = 0
        total_reward = []
        total_length = []

        gradBuffer = sess.run(tf.trainable_variables())
        for ix,grad in enumerate(gradBuffer):
            gradBuffer[ix] = grad * 0

        while i < total_episodes:
            s = env.reset()
            done = False
            running_reward = 0
            ep_history = []
            j=0
            while not done:
                #Probabilistically pick an action given our network outputs.
                a_dist = sess.run(myAgent.output,feed_dict={myAgent.state_in:[s]})
                a = np.random.choice(a_dist[0],p=a_dist[0])
                a = np.argmax(a_dist == a)

                s1,r,d,history = env.step(a) #Get our reward for taking an action given a bandit.
                ep_history.append([s,a,r,s1])
                done = d
                s = s1
                running_reward += r
                if d == True:
                    #Update the network.
                    ep_history = np.array(ep_history)
                    ep_history[:,2] = discount_rewards(ep_history[:,2])
                    feed_dict={myAgent.reward_holder:ep_history[:,2],
                            myAgent.action_holder:ep_history[:,1],myAgent.state_in:np.vstack(ep_history[:,0])}
                    grads = sess.run(myAgent.gradients, feed_dict=feed_dict)
                    for idx,grad in enumerate(grads):
                        gradBuffer[idx] += grad

                    if i % update_frequency == 0 and i != 0:
                        feed_dict= dictionary = dict(zip(myAgent.gradient_holders, gradBuffer))
                        _ = sess.run(myAgent.update_batch, feed_dict=feed_dict)
                        for ix,grad in enumerate(gradBuffer):
                            gradBuffer[ix] = grad * 0

                    total_reward.append(running_reward)
                    total_length.append(j)
                    break
                j+=1

                #Update our running tally of scores.
            if i % 100 == 0:
                print(np.mean(total_reward[-100:]))
            i += 1
            if i % 1000 == 0:
                for entry in history:
                    print(entry)
