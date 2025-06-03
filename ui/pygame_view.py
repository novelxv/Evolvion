import pygame
import math
from ui.ui_controller import UIController

# Color scheme
DARK_BG = (25, 25, 35)
SIMULATION_BG = (240, 245, 250)
ACCENT_BLUE = (100, 150, 255)
ACCENT_GREEN = (100, 255, 150)
TEXT_WHITE = (255, 255, 255)

class ScreenRenderer:
    def __init__(self, config):
        self.config = config
        self.ui_controller = UIController(config)
        self.sidebar_width = 300
        
        # Performance tracking
        self.fitness_history = []
        self.reward_history = []
        self.population_history = []
        
    def render(self, env, gen, step, screen):
        """Main render function with modern UI"""
        # Update statistics
        self.ui_controller.update_stats(env, gen, step)
        
        # Check if paused
        if self.ui_controller.is_paused:
            return False  # Signal to pause simulation
        
        # Clear screen
        screen.fill(DARK_BG)
        
        # Draw simulation area
        self._draw_simulation_area(screen, env)
        
        # Draw agents in simulation area
        self._draw_agents(screen, env)
        
        # Draw UI panels
        self.ui_controller.render(screen)
        
        # Draw performance charts
        self._draw_performance_charts(screen, env, gen)
        
        pygame.display.flip()
        return True
    
    def handle_event(self, event):
        """Handle UI events"""
        self.ui_controller.handle_event(event)
        return not self.ui_controller.is_paused
    
    def _draw_simulation_area(self, screen, env):
        """Draw the main simulation area"""
        sim_rect = pygame.Rect(
            self.sidebar_width, 0,
            screen.get_width() - self.sidebar_width,
            screen.get_height()
        )
        
        # Simple gradient background - FIXED COLOR CALCULATION
        for y in range(0, sim_rect.height, 2):
            base_color = 240
            variation = int(5 * math.sin(y * 0.01))
            
            # Clamp to valid RGB range
            r = max(235, min(245, base_color + variation))
            g = max(240, min(250, base_color + variation + 3))
            b = max(245, min(255, base_color + variation + 6))
            
            color = (r, g, b)
            pygame.draw.line(screen, color, 
                           (sim_rect.x, sim_rect.y + y), 
                           (sim_rect.right, sim_rect.y + y))
        
        # Grid pattern
        grid_size = 50
        grid_color = (220, 225, 230)
        for x in range(sim_rect.x, sim_rect.right, grid_size):
            pygame.draw.line(screen, grid_color, (x, sim_rect.y), (x, sim_rect.bottom), 1)
        for y in range(sim_rect.y, sim_rect.bottom, grid_size):
            pygame.draw.line(screen, grid_color, (sim_rect.x, y), (sim_rect.right, y), 1)
        
        # Border
        pygame.draw.rect(screen, (150, 150, 160), sim_rect, 2)
    
    def _draw_agents(self, screen, env):
        """Draw agents with modern styling"""
        offset_x = self.sidebar_width
        
        for agent in env.agents:
            if not agent.alive:
                continue
                
            x = agent.x + offset_x
            y = agent.y
            
            # Draw vision circle if enabled
            if self.ui_controller.show_vision:
                # Get vision from agent attributes - try multiple ways
                vision = getattr(agent, 'vision', None)
                if vision is None and hasattr(agent, 'traits'):
                    vision = agent.traits.get('vision', 3.0)
                if vision is None:
                    vision = 3.0  # Default value
                    
                vision_radius = int(vision * agent.radius)
                if vision_radius > 0:
                    vision_surf = pygame.Surface((vision_radius * 2, vision_radius * 2), pygame.SRCALPHA)
                    
                    if agent.entity_class == "prey":
                        color = (100, 150, 255, 30)
                    else:
                        color = (255, 100, 100, 40)
                    
                    pygame.draw.circle(vision_surf, color, (vision_radius, vision_radius), vision_radius)
                    screen.blit(vision_surf, (int(x - vision_radius), int(y - vision_radius)))
            
            # Draw agent with glow effect
            if agent.entity_class == "prey":
                # Prey with blue glow
                glow_surf = pygame.Surface((agent.radius * 4, agent.radius * 4), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (0, 120, 255, 50), (agent.radius * 2, agent.radius * 2), agent.radius * 2)
                screen.blit(glow_surf, (int(x - agent.radius * 2), int(y - agent.radius * 2)))
                
                pygame.draw.circle(screen, (0, 120, 255), (int(x), int(y)), agent.radius)
                pygame.draw.circle(screen, (100, 180, 255), (int(x), int(y)), agent.radius, 2)
                
                # Fitness indicator
                if hasattr(agent, 'fitness') and agent.fitness > 0:
                    fitness_bar_width = int(min(30, agent.fitness / 10))
                    if fitness_bar_width > 0:
                        bar_rect = pygame.Rect(int(x - 15), int(y - agent.radius - 8), fitness_bar_width, 3)
                        pygame.draw.rect(screen, (100, 255, 100), bar_rect)
                
            else:  # Predator
                # Predator with red glow
                glow_surf = pygame.Surface((agent.radius * 4, agent.radius * 4), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (255, 60, 60, 70), (agent.radius * 2, agent.radius * 2), agent.radius * 2)
                screen.blit(glow_surf, (int(x - agent.radius * 2), int(y - agent.radius * 2)))
                
                pygame.draw.circle(screen, (255, 60, 60), (int(x), int(y)), agent.radius)
                pygame.draw.circle(screen, (255, 120, 120), (int(x), int(y)), agent.radius, 2)
                
                # Reward indicator
                if hasattr(agent, 'total_reward'):
                    reward_color = (100, 255, 100) if agent.total_reward > 0 else (255, 100, 100)
                    reward_text = f"{agent.total_reward:.1f}"
                    font = pygame.font.Font(None, 14)
                    text_surf = font.render(reward_text, True, reward_color)
                    screen.blit(text_surf, (int(x + agent.radius + 5), int(y - agent.radius)))
            
            # Draw velocity vector
            if hasattr(agent, 'vel_x') and hasattr(agent, 'vel_y'):
                if abs(agent.vel_x) > 0.1 or abs(agent.vel_y) > 0.1:
                    end_x = x + agent.vel_x * 10
                    end_y = y + agent.vel_y * 10
                    pygame.draw.line(screen, (0, 0, 0), (int(x), int(y)), (int(end_x), int(end_y)), 2)
    
    def _draw_performance_charts(self, screen, env, generation):
        """Draw real-time performance charts"""
        try:
            # Update history
            alive_prey = sum(1 for p in env.prey if p.alive)
            avg_fitness = sum(p.fitness for p in env.prey if p.alive) / max(alive_prey, 1) if alive_prey > 0 else 0
            avg_reward = sum(pr.total_reward for pr in env.predators) / len(env.predators) if env.predators else 0
            
            self.fitness_history.append(avg_fitness)
            self.reward_history.append(avg_reward)
            self.population_history.append(alive_prey)
            
            # Keep only last 100 points
            if len(self.fitness_history) > 100:
                self.fitness_history.pop(0)
                self.reward_history.pop(0)
                self.population_history.pop(0)
            
            # Chart area (top right)
            chart_x = screen.get_width() - 270
            chart_y = 20
            chart_w = 250
            chart_h = 80
            
            # Fitness chart
            self._draw_mini_chart(screen, "Avg Fitness", self.fitness_history, 
                                chart_x, chart_y, chart_w, chart_h, (100, 255, 100))
            
            # Reward chart
            self._draw_mini_chart(screen, "Avg Reward", self.reward_history,
                                chart_x, chart_y + 100, chart_w, chart_h, (255, 100, 100))
            
            # Population chart
            self._draw_mini_chart(screen, "Alive Prey", self.population_history,
                                chart_x, chart_y + 200, chart_w, chart_h, (100, 150, 255))
        except Exception as e:
            pass  # Skip charts if error
    
    def _draw_mini_chart(self, screen, title, data, x, y, w, h, color):
        """Draw a mini line chart"""
        if len(data) < 2:
            return
            
        try:
            # Background
            chart_bg = pygame.Surface((w, h + 25), pygame.SRCALPHA)
            pygame.draw.rect(chart_bg, (0, 0, 0, 120), chart_bg.get_rect())
            screen.blit(chart_bg, (x, y))
            
            # Title
            font = pygame.font.Font(None, 16)
            title_surf = font.render(title, True, TEXT_WHITE)
            screen.blit(title_surf, (x + 5, y + 5))
            
            # Chart area
            chart_rect = pygame.Rect(x + 5, y + 20, w - 10, h - 5)
            pygame.draw.rect(screen, (30, 30, 40), chart_rect)
            
            # Data range
            min_val = min(data)
            max_val = max(data)
            if max_val == min_val:
                max_val = min_val + 1
            
            # Draw line
            if len(data) > 1:
                points = []
                for i, value in enumerate(data):
                    px = chart_rect.x + (i / (len(data) - 1)) * chart_rect.width
                    py = chart_rect.bottom - ((value - min_val) / (max_val - min_val)) * chart_rect.height
                    points.append((int(px), int(py)))
                
                if len(points) > 1:
                    pygame.draw.lines(screen, color, False, points, 2)
            
            # Current value
            current_val = data[-1] if data else 0
            val_text = f"{current_val:.1f}"
            val_surf = font.render(val_text, True, color)
            screen.blit(val_surf, (x + w - val_surf.get_width() - 5, y + 5))
        except Exception as e:
            pass


# Global renderer instance
renderer = None

def render(env, gen, step):
    """Main render function called by simulation"""
    global renderer
    
    screen = pygame.display.get_surface()
    if screen is None:
        return True
    
    if renderer is None:
        renderer = ScreenRenderer(env.config)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        
        renderer.handle_event(event)
    
    return renderer.render(env, gen, step, screen)