is_log_enabled: bool = False

# I am still trying to figure what the StateMachine object does and how to properly implement
# it in my game


# object that can exit, enter, change, and get the name of the state
class State():
    def __init__(self):
        self.state = "StNormal"
        print(f"your state is {self.state}")
    def enter(self):
        pass
    def exit(self):
        self.state = "None"
    def update(self):
        pass
    def get_state_name(self):
        return self.state

# object that 
class StateMachine():
    def __init__(self):
        self.current_state = State()
        self.states = {}
        print(self.states)
    
    def start_machine(self, init_states = [State]):
        for state in init_states:
            print(state.get_state_name())
            self.states[state.get_state_name()] = state
            print(self.states)

        self.current_state = init_states[0]

        if is_log_enabled:
            print('starting state machine...')

        self.current_state.enter()
        print("state machine started with state:", self.current_state.get_state_name())

    # comment comment comment
    def update(self):
        if self.current_state == None:
            print('no current state...')
        else:
            self.current_state.update()
        
    def transition(self, new_state_name):
        new_state: State = self.states.get(new_state_name)
        self.current_state_name = self.current_state.get_state_name()
        if new_state == None:
            print("attempting to transition to non existent state")
        elif new_state != self.current_state:
            self.current_state.exit()
            
            if is_log_enabled:
                print('exiting state...')
            
            self.current_state = self.states[new_state.get_state_name()]

            if is_log_enabled:
                print('entering new state...')

            self.current_state.enter()
        else:
            if is_log_enabled:
                print("attempt to transition to " + new_state_name + " ignored since it is the current state...")