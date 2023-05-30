import time
from typing import List, Tuple, Callable

class ActionQueue():
    def __init__(self) -> None:
        super().__init__()
        self.action_queue: List[Tuple[float, Callable]] = []
        self.new_actions: List[Tuple[float, Callable]] = []
        self.internal_time = time.time()

    def add_delayed_action(self, action: Callable, delay_ms: float) -> None:
        self.new_actions.append((self.internal_time + delay_ms / 1000, action))
        return self

    def clear_queue(self):
        self.action_queue.clear()
        
    def clear_new_actions(self):
        self.new_actions.clear()
        
    def update(self) -> None:
        self.internal_time = time.time()
        for new_action in self.new_actions:
            self.action_queue.append(new_action)
            
        self.clear_new_actions()
        for action in self.action_queue:
            if self.internal_time > action[0]:
                action[1].__call__()
                self.action_queue.remove(action)
                
    def get_action_queue(self) -> List[Tuple[float, Callable]]:
        return self.action_queue;