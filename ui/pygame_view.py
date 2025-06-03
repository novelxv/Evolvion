import pygame
import sys

def render(env, gen, step):
    screen = pygame.display.get_surface()
    if screen is None:
        return

    screen.fill(env.config["white"])

    for agent in env.agents:
        agent.draw(screen)

    font = pygame.font.SysFont("Arial", 18)
    text = font.render(f"Gen: {gen+1} | Step: {step+1}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
