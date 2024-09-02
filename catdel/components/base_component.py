from catdel.state_manager import StateManager
sm = StateManager.get_instance()

class BaseComponent:
    
    def __init__(self):
        pass


    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)
    
    def call(self, *args, **kwargs):
        raise NotImplementedError
