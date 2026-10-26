import matplotlib.pyplot as plt
import numpy as np
import random
import time

class VisualEnvironment3x3:
    def __init__(self):
        self.grid = np.random.choice([0, 1], size=(3, 3))
        self.agent_pos = [0, 0] 
        self.energia = 0
        self.puntaje = 0
        
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(5, 5))

    def render(self, step, action):
        self.ax.clear()
        self.ax.matshow(self.grid, cmap='Blues', vmin=0, vmax=1.5)
        
        self.ax.plot(self.agent_pos[1], self.agent_pos[0], 'ro', markersize=40)
        
        for i in range(3):
            for j in range(3):
                estado = "SUCIO" if self.grid[i, j] == 1 else "LIMPIO"
                self.ax.text(j, i, estado, ha='center', va='center', 
                             color='black', weight='bold', fontsize=10)

        self.ax.set_title(f"Paso: {step} | Acción: {action}\nPuntaje: {self.puntaje} | Energía: {self.energia}", pad=20)
        self.ax.set_xticks([0, 1, 2])
        self.ax.set_yticks([0, 1, 2])
        self.ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
        
        plt.draw()
        plt.pause(1.0) 

    def get_percept(self):
        return self.agent_pos.copy(), self.grid[self.agent_pos[0], self.agent_pos[1]]

    def execute_action(self, action):
        if action in ['Suck', 'Up', 'Down', 'Left', 'Right']:
            self.energia += 1
            self.puntaje -= 1

        if action == 'Suck':
            self.grid[self.agent_pos[0], self.agent_pos[1]] = 0
            self.puntaje += 10 
        elif action == 'Up' and self.agent_pos[0] > 0:
            self.agent_pos[0] -= 1
        elif action == 'Down' and self.agent_pos[0] < 2: 
            self.agent_pos[0] += 1
        elif action == 'Left' and self.agent_pos[1] > 0:
            self.agent_pos[1] -= 1
        elif action == 'Right' and self.agent_pos[1] < 2: 
            self.agent_pos[1] += 1

    def is_completely_clean(self):
        return np.sum(self.grid) == 0

class SystematicVacuumAgent:
    def act(self, percept):
        pos, status = percept
        fila = pos[0]
        columna = pos[1]
        
        if status == 1:
            return 'Suck'
        
        if fila % 2 == 0: 
            if columna < 2: return 'Right'
            elif fila < 2: return 'Down'
        else: 
            if columna > 0: return 'Left'
            elif fila < 2: return 'Down'
            
        return 'Fin' 

if __name__ == "__main__":
    env = VisualEnvironment3x3()
    agent = SystematicVacuumAgent() 

    env.render(step=0, action="Inicio")

    for paso in range(1, 30): 
        percept = env.get_percept()
        action = agent.act(percept)
        
        if action == 'Fin':
            if env.is_completely_clean():
                env.puntaje += 20 
            print("¡Entorno 3x3 completamente limpio y barrido finalizado!")
            print(f"Puntaje Final: {env.puntaje} | Energía Gastada: {env.energia}")
            break
            
        env.execute_action(action)
        env.render(step=paso, action=action)

    plt.ioff()
    plt.show()