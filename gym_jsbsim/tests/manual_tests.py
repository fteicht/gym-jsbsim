import unittest
import time
from gym_jsbsim.environment import JsbSimEnv
from typing import Type
from gym_jsbsim import tasks
from gym_jsbsim.tests.stubs import TaskStub
from gym_jsbsim.agents import RandomAgent, ConstantAgent, RepeatAgent


class TestJsbSimInstance(unittest.TestCase):
    def setUp(self, task_type: Type[tasks.FlightTask]= TaskStub):
        self.env = None
        self.env = JsbSimEnv(task_type)
        self.env.reset()

    def tearDown(self):
        self.env.close()

    def test_long_episode_random_actions(self):
        self.setUp()
        tic = time.time()
        self.env.reset()
        for i in range(2000):
            self.env.step(action=self.env.action_space.sample())
            print(f'jsbsim {i / 10} s\n')
        toc = time.time()
        wall_time = (toc - tic)
        sim_time = self.env.sim['simulation/jsbsim-time-sec']
        print(f'Simulated {sim_time} s of flight in {wall_time} s')

    def test_render_episode(self):
        self.setUp()
        render_every = 5
        self.env.reset()
        for i in range(1000):
            action = self.env.action_space.sample()
            obs, _, _, _ = self.env.step(action=action)
            if i % render_every == 0:
                self.env.render(mode='human', action_names=self.env.task.action_names, action_values=action)

    def test_render_steady_level_flight_random(self):
        """ Runs steady level flight task with a random agent. """
        self.setUp(task_type=tasks.SteadyLevelFlightTask)
        agent = RandomAgent(self.env.action_space)
        render_every = 5
        ep_reward = 0
        done = False
        state = self.env.reset()
        step_number = 0
        while not done:
            action = agent.act(state)
            state, reward, done, info = self.env.step(action)
            ep_reward += reward
            if step_number % render_every == 0:
                self.env.render(mode='human', action_names=self.env.task.action_names, action_values=action)
            step_number += 1

    def test_run_episode_steady_level_flight_no_render(self):
        self.setUp(task_type=tasks.SteadyLevelFlightTask)
        agent = RandomAgent(self.env.action_space)
        report_every = 20
        EPISODES = 10

        for _ in range(EPISODES):
            ep_reward = 0
            done = False
            state = self.env.reset()
            step_number = 0
            while not done:
                action = agent.act(state)
                state, reward, done, info = self.env.step(action)
                ep_reward += reward
                if step_number % report_every == 0:
                    print(f'time:\t{self.env.jsbsim.get_sim_time()} s')
                    print(f'last reward:\t{reward}')
                    print(f'episode reward:\t{ep_reward}')
                step_number += 1

    def test_steady_level_flight_constant_with_flightgear_render(self):
        self.setUp(task_type=tasks.SteadyLevelFlightTask)
        agent = RepeatAgent(self.env.action_space,
                            self.env.task.action_names,
                            self.env.task.state_names)
        EPISODES = 50
        report_every = 20

        for _ in range(EPISODES):
            ep_reward = 0
            done = False
            state = self.env.reset()
            self.env.render(mode='flightgear')
            step_number = 0
            while not done:
                action = agent.act(state)
                state, reward, done, info = self.env.step(action)
                ep_reward += reward
                if step_number % report_every == 0:
                    print(f'time:\t{self.env.jsbsim.get_sim_time()} s')
                    print(f'last reward:\t{reward}')
                    print(f'episode reward:\t{ep_reward}')
                    print(f'throttle:\t{self.env.jsbsim["fcs/throttle-pos-norm"]}')
                step_number += 1


class FlightGearRenderTest(unittest.TestCase):
    def setUp(self, aircraft_name: str='c172p', task_type: Type[tasks.FlightTask]=TaskStub):
        self.env = None
        self.env = JsbSimEnv(aircraft_name=aircraft_name, task_type=task_type)
        self.env.reset()

    def tearDown(self):
        self.env.close()

    def test_render_steady_level_flight(self):
        self.setUp(aircraft_name='c172x', task_type=tasks.SteadyLevelFlightTask)
        agent = ConstantAgent(self.env.action_space)
        render_every = 5
        report_every = 20
        EPISODES = 5

        for _ in range(EPISODES):
            ep_reward = 0
            done = False
            state = self.env.reset()
            self.env.render(mode='flightgear')
            step_number = 0
            while not done:
                action = agent.act(state)
                state, reward, done, info = self.env.step(action)
                ep_reward += reward
                if step_number % render_every == 0:
                    self.env.render(mode='flightgear')
                if step_number % report_every == 0:
                    print(f'time:\t{self.env.jsbsim.get_sim_time()} s')
                    print(f'last reward:\t{reward}')
                    print(f'episode reward:\t{ep_reward}')
                    print(f'thrust:\t{self.env.jsbsim["propulsion/engine/thrust-lbs"]}')
                    print(f'engine running:\t{self.env.jsbsim["propulsion/engine/set-running"]}')
                step_number += 1

class HeadingControlTest(unittest.TestCase):
    def setUp(self, aircraft_name: str='c172p', task_type: Type[tasks.FlightTask]=tasks.HeadingControlTask):
        self.env = None
        self.env = JsbSimEnv(aircraft_name=aircraft_name, task_type=task_type)
        self.env.reset()

    def tearDown(self):
        self.env.close()

    def test_render_heading_control(self):
        self.setUp(aircraft_name='c172x', task_type=tasks.HeadingControlTask)
        agent = RandomAgent(self.env.action_space)
        render_every = 5
        report_every = 20
        EPISODES = 50

        for _ in range(EPISODES):
            ep_reward = 0
            done = False
            state = self.env.reset()
            self.env.render(mode='flightgear')
            step_number = 0
            while not done:
                action = agent.act(state)
                state, reward, done, info = self.env.step(action)
                ep_reward += reward
                if step_number % render_every == 0:
                    self.env.render(mode='flightgear')
                if step_number % report_every == 0:
                    print(f'time:\t{self.env.jsbsim.get_sim_time()} s')
                    print(f'last reward:\t{reward}')
                    print(f'episode reward:\t{ep_reward}')
                    print(f'heading:\t{self.env.jsbsim["attitude/psi-deg"]}')
                    print(f'target heading:\t{self.env.jsbsim["target/heading-deg"]}')
                    print('\n')
                step_number += 1