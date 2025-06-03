import pygame
import math
from typing import Dict, Any, Callable

class UIController:
    def __init__(self, config: dict):
        self.config = config
        self.sidebar_width = 300
        self.control_height = 120
        self.stats_height = 200
        
        # UI State
        self.is_paused = False
        self.show_vision = True
        self.simulation_speed = 1.0
        
        # Parameter controls
        self.sliders = {}
        self.buttons = {}
        
        # Stats tracking
        self.current_stats = {
            "alive_prey": 0,
            "avg_fitness": 0.0,
            "avg_reward": 0.0,
            "generation": 0,
            "step": 0,
            "total_prey": 0,
            "total_predators": 0
        }
        
        self._init_controls()
    
    def _init_controls(self):
        """Initialize UI controls"""
        # Sliders for prey parameters
        self.sliders["prey_speed_min"] = Slider(20, 120, 200, 20, 0.1, 5.0, self.config["trait_range"]["speed"][0])
        self.sliders["prey_speed_max"] = Slider(20, 150, 200, 20, 0.1, 5.0, self.config["trait_range"]["speed"][1])
        self.sliders["prey_agility_min"] = Slider(20, 190, 200, 20, 0.01, 2.0, self.config["trait_range"]["agility"][0])
        self.sliders["prey_agility_max"] = Slider(20, 220, 200, 20, 0.01, 2.0, self.config["trait_range"]["agility"][1])
        self.sliders["prey_vision_min"] = Slider(20, 260, 200, 20, 1.0, 10.0, self.config["trait_range"]["vision"][0])
        self.sliders["prey_vision_max"] = Slider(20, 290, 200, 20, 1.0, 10.0, self.config["trait_range"]["vision"][1])
        
        # Sliders for predator parameters
        self.sliders["predator_speed"] = Slider(20, 350, 200, 20, 1.0, 20.0, self.config["predator_speed"])
        self.sliders["predator_vision"] = Slider(20, 380, 200, 20, 5.0, 40.0, self.config["predator_vision"])
        
        # Simulation control sliders
        self.sliders["mutation_rate"] = Slider(20, 440, 200, 20, 0.01, 0.5, self.config["mutation_rate"])
        self.sliders["num_prey"] = Slider(20, 480, 200, 20, 10, 100, self.config["num_prey"])
        self.sliders["num_predators"] = Slider(20, 520, 200, 20, 1, 20, self.config["num_predators"])
        
        # Buttons
        self.buttons["play_pause"] = Button(20, 580, 80, 40, "▶ Play", self._toggle_pause)
        self.buttons["reset"] = Button(110, 580, 80, 40, "Reset", self._reset_simulation)
        self.buttons["save"] = Button(200, 580, 80, 40, "Save", self._save_config)
        self.buttons["toggle_vision"] = Button(20, 630, 120, 30, "Hide Vision", self._toggle_vision)
        self.buttons["speed_up"] = Button(150, 630, 40, 30, "2x", self._speed_up)
        self.buttons["speed_down"] = Button(200, 630, 40, 30, "1x", self._speed_down)
    
    def handle_event(self, event):
        """Handle pygame events"""
        for slider in self.sliders.values():
            slider.handle_event(event)
        
        for button in self.buttons.values():
            button.handle_event(event)
        
        # Handle keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._toggle_pause()
            elif event.key == pygame.K_v:
                self._toggle_vision()
            elif event.key == pygame.K_r:
                self._reset_simulation()
        
        # Update config when sliders change
        self._update_config_from_sliders()
    
    def _update_config_from_sliders(self):
        """Update config based on slider values"""
        self.config["trait_range"]["speed"] = (
            self.sliders["prey_speed_min"].value,
            self.sliders["prey_speed_max"].value
        )
        self.config["trait_range"]["agility"] = (
            self.sliders["prey_agility_min"].value,
            self.sliders["prey_agility_max"].value
        )
        self.config["trait_range"]["vision"] = (
            self.sliders["prey_vision_min"].value,
            self.sliders["prey_vision_max"].value
        )
        self.config["predator_speed"] = self.sliders["predator_speed"].value
        self.config["predator_vision"] = self.sliders["predator_vision"].value
        self.config["mutation_rate"] = self.sliders["mutation_rate"].value
        self.config["num_prey"] = int(self.sliders["num_prey"].value)
        self.config["num_predators"] = int(self.sliders["num_predators"].value)
    
    def _toggle_pause(self):
        self.is_paused = not self.is_paused
        self.buttons["play_pause"].text = "⏸ Pause" if not self.is_paused else "▶ Play"
        print(f"Simulation {'PAUSED' if self.is_paused else 'RESUMED'}")
    
    def _reset_simulation(self):
        print("Reset requested (will need manual restart)")
    
    def _save_config(self):
        import json
        with open("saved_config.json", "w") as f:
            json.dump(self.config, f, indent=2)
        print("Configuration saved to saved_config.json!")
    
    def _toggle_vision(self):
        self.show_vision = not self.show_vision
        self.buttons["toggle_vision"].text = "Show Vision" if not self.show_vision else "Hide Vision"
    
    def _speed_up(self):
        self.simulation_speed = min(4.0, self.simulation_speed * 2)
        self.buttons["speed_up"].text = f"{self.simulation_speed:.0f}x"
    
    def _speed_down(self):
        self.simulation_speed = max(0.25, self.simulation_speed / 2)
        self.buttons["speed_down"].text = f"{self.simulation_speed:.1f}x"
    
    def update_stats(self, env, generation, step):
        """Update current statistics"""
        alive_prey = sum(1 for p in env.prey if p.alive)
        
        if alive_prey > 0:
            avg_fitness = sum(p.fitness for p in env.prey if p.alive) / alive_prey
        else:
            avg_fitness = 0.0
            
        if env.predators:
            avg_reward = sum(pr.total_reward for pr in env.predators) / len(env.predators)
        else:
            avg_reward = 0.0
        
        self.current_stats = {
            "alive_prey": alive_prey,
            "avg_fitness": avg_fitness,
            "avg_reward": avg_reward,
            "generation": generation,
            "step": step,
            "total_prey": len(env.prey),
            "total_predators": len(env.predators)
        }
    
    def render(self, screen):
        """Render all UI elements"""
        self._draw_sidebar(screen)
        self._draw_stats_panel(screen)
    
    def _draw_sidebar(self, screen):
        """Draw control sidebar"""
        # Sidebar background
        sidebar_rect = pygame.Rect(0, 0, self.sidebar_width, screen.get_height())
        pygame.draw.rect(screen, (45, 45, 55), sidebar_rect)
        
        font_title = pygame.font.Font(None, 28)
        font_label = pygame.font.Font(None, 20)
        font_small = pygame.font.Font(None, 16)
        
        # Title
        title = font_title.render("EVOLVION CONTROL", True, (255, 255, 255))
        screen.blit(title, (20, 20))
        
        # Prey Parameters Section
        y = 70
        prey_title = font_label.render("PREY PARAMETERS", True, (100, 200, 255))
        screen.blit(prey_title, (20, y))
        
        # Draw sliders with labels
        self._draw_labeled_slider(screen, "Speed Min", self.sliders["prey_speed_min"], font_small)
        self._draw_labeled_slider(screen, "Speed Max", self.sliders["prey_speed_max"], font_small)
        self._draw_labeled_slider(screen, "Agility Min", self.sliders["prey_agility_min"], font_small)
        self._draw_labeled_slider(screen, "Agility Max", self.sliders["prey_agility_max"], font_small)
        self._draw_labeled_slider(screen, "Vision Min", self.sliders["prey_vision_min"], font_small)
        self._draw_labeled_slider(screen, "Vision Max", self.sliders["prey_vision_max"], font_small)
        
        # Predator Parameters Section
        pred_title = font_label.render("PREDATOR PARAMETERS", True, (255, 100, 100))
        screen.blit(pred_title, (20, 320))
        
        self._draw_labeled_slider(screen, "Speed", self.sliders["predator_speed"], font_small)
        self._draw_labeled_slider(screen, "Vision", self.sliders["predator_vision"], font_small)
        
        # Simulation Parameters
        sim_title = font_label.render("⚙️ SIMULATION", True, (100, 255, 100))
        screen.blit(sim_title, (20, 410))
        
        self._draw_labeled_slider(screen, "Mutation Rate", self.sliders["mutation_rate"], font_small)
        self._draw_labeled_slider(screen, "Number of Prey", self.sliders["num_prey"], font_small)
        self._draw_labeled_slider(screen, "Number of Predators", self.sliders["num_predators"], font_small)
        
        # Control Buttons
        for button in self.buttons.values():
            button.draw(screen)
        
        # Keyboard shortcuts info
        shortcuts_y = 680
        shortcuts_title = font_small.render("KEYBOARD SHORTCUTS:", True, (200, 200, 200))
        screen.blit(shortcuts_title, (20, shortcuts_y))
        
        shortcuts = [
            "SPACE - Pause/Resume",
            "V - Toggle Vision",
            "R - Reset Request",
            "ESC - Exit"
        ]
        
        for i, shortcut in enumerate(shortcuts):
            shortcut_surf = font_small.render(shortcut, True, (150, 150, 150))
            screen.blit(shortcut_surf, (20, shortcuts_y + 20 + i * 16))
    
    def _draw_labeled_slider(self, screen, label, slider, font):
        """Draw slider with label and value"""
        # Label
        label_surf = font.render(label, True, (200, 200, 200))
        screen.blit(label_surf, (slider.rect.x, slider.rect.y - 18))
        
        # Value
        value_text = f"{slider.value:.2f}" if isinstance(slider.value, float) else str(int(slider.value))
        value_surf = font.render(value_text, True, (255, 255, 255))
        screen.blit(value_surf, (slider.rect.right + 10, slider.rect.y))
        
        # Slider
        slider.draw(screen)
    
    def _draw_stats_panel(self, screen):
        """Draw statistics panel"""
        stats_y = screen.get_height() - self.stats_height - 20
        stats_rect = pygame.Rect(10, stats_y, self.sidebar_width - 20, self.stats_height)
        pygame.draw.rect(screen, (35, 35, 45), stats_rect)
        pygame.draw.rect(screen, (100, 100, 120), stats_rect, 2)
        
        font_title = pygame.font.Font(None, 24)
        font_stat = pygame.font.Font(None, 18)
        
        # Title
        title = font_title.render("LIVE STATISTICS", True, (255, 255, 255))
        screen.blit(title, (20, stats_y + 10))
        
        y = stats_y + 40
        stats_text = [
            f"Generation: {self.current_stats['generation'] + 1}",
            f"Step: {self.current_stats['step'] + 1}",
            f"Prey Alive: {self.current_stats['alive_prey']}/{self.current_stats.get('total_prey', 0)}",
            f"Avg Fitness: {self.current_stats['avg_fitness']:.1f}",
            f"Avg Reward: {self.current_stats['avg_reward']:.2f}",
            f"Speed: {self.simulation_speed:.1f}x",
            f"Status: {'⏸ PAUSED' if self.is_paused else '▶ RUNNING'}"
        ]
        
        colors = [
            (200, 200, 200),  # Generation
            (200, 200, 200),  # Step
            (100, 150, 255),  # Prey alive
            (100, 255, 100),  # Fitness
            (255, 100, 100),  # Reward
            (255, 255, 100),  # Speed
            (255, 255, 100) if "PAUSED" in stats_text[6] else (100, 255, 100)  # Status
        ]
        
        for i, (text, color) in enumerate(zip(stats_text, colors)):
            surf = font_stat.render(text, True, color)
            screen.blit(surf, (20, y + i * 22))


class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.dragging = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self._update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_value(event.pos[0])
    
    def _update_value(self, mouse_x):
        rel_x = mouse_x - self.rect.x
        rel_x = max(0, min(rel_x, self.rect.width))
        self.value = self.min_val + (rel_x / self.rect.width) * (self.max_val - self.min_val)
    
    def draw(self, screen):
        # Background
        pygame.draw.rect(screen, (80, 80, 90), self.rect)
        pygame.draw.rect(screen, (60, 60, 70), self.rect, 2)
        
        # Handle
        handle_pos = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = int(self.rect.x + handle_pos * self.rect.width)
        handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 2, 10, self.rect.height + 4)
        pygame.draw.rect(screen, (100, 150, 255), handle_rect)


class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
        self.pressed = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.rect.collidepoint(event.pos):
                self.callback()
            self.pressed = False
    
    def draw(self, screen):
        # Button background
        color = (70, 130, 255) if self.hovered else (50, 100, 200)
        if self.pressed:
            color = (30, 80, 180)
        
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (100, 150, 255), self.rect, 2)
        
        # Button text
        font = pygame.font.Font(None, 16)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)