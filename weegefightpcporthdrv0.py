import tkinter as tk
from tkinter import ttk
import pygame
import os
import random
import math

# --- Game Constants ---
WIDTH, HEIGHT = 600, 360
BOTTOM_HEIGHT = 160
FPS = 60

# --- Color Palette (Vibes Intact) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (50, 50, 50)
DARK_GREY = (30, 30, 30)
LIGHT_GREY = (120, 120, 120)
PULSE_COLOR = (20, 0, 0)
DARK_RED = (100, 0, 0)
WEEGEE_GREEN = (0, 100, 20)
WEEGEE_BLUE = (40, 40, 180)
WEEGEE_SKIN = (200, 220, 180)
WEEGEE_EYES = (255, 10, 10)
MARIO_RED = (200, 0, 0)
MARIO_BLUE = (0, 0, 200)
SPAGHETTI_YELLOW = (255, 220, 100)
ROBOTNIK_ORANGE = (255, 140, 0)
NORRIS_BROWN = (139, 69, 19)
BOWSER_NOTE_RED = (255, 50, 50)
BOWSER_NOTE_YELLOW = (255, 200, 0)

class MusicVisualizer:
    """Creates a visual representation of music without playing audio files."""
    def __init__(self, surface):
        self.surface = surface
        self.notes = []
        self.beat_timer = 0
        self.beat_duration = 20  # Every 20 frames
        self.pulse_alpha = 0

    def update(self):
        self.beat_timer = (self.beat_timer + 1) % self.beat_duration
        if self.beat_timer == 0:
            self.pulse_alpha = 128  # Trigger a background pulse
            # Generate new notes for the visualizer
            for _ in range(random.randint(2, 5)):
                self.notes.append({
                    'pos': [WIDTH, random.randint(50, HEIGHT - 50)],
                    'speed': random.uniform(4.0, 8.0),
                    'color': random.choice([BOWSER_NOTE_RED, BOWSER_NOTE_YELLOW, WHITE]),
                    'size': random.randint(10, 30)
                })

        # Update existing notes
        for note in self.notes[:]:
            note['pos'][0] -= note['speed']
            if note['pos'][0] < 0:
                self.notes.remove(note)

        # Fade the pulse
        if self.pulse_alpha > 0:
            self.pulse_alpha -= 8

    def draw(self):
        # Draw the rhythmic background pulse
        if self.pulse_alpha > 0:
            pulse_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pulse_surf.fill((*PULSE_COLOR, self.pulse_alpha))
            self.surface.blit(pulse_surf, (0, 0))

        # Draw the visual notes
        for note in self.notes:
            pygame.draw.rect(self.surface, note['color'], (note['pos'][0], note['pos'][1], note['size'], 4))


class Game:
    """Manages the Pygame state and all procedurally drawn graphics."""
    def __init__(self, surface):
        self.surface = surface
        self.player_pos = [WIDTH // 2, HEIGHT - 40]
        self.projectiles = []
        self.effects = []
        
        self.weegee_max_health = 1000
        self.weegee_health = self.weegee_max_health
        self.weegee_pos = [WIDTH // 2, HEIGHT - 130]
        self.weegee_shake = 0

        self.game_state = "INTRO"
        self.intro_timer = FPS * 3
        
        # Initialize the procedural music
        self.music_viz = MusicVisualizer(self.surface)

    def update(self):
        # Handle different game states
        if self.game_state == "INTRO":
            self.surface.fill(BLACK)
            self.draw_intro_logo()
            self.intro_timer -= 1
            if self.intro_timer <= 0:
                self.game_state = "PLAYING"
            return

        if self.game_state == "GAMEOVER":
             self.surface.fill(BLACK)
             self.draw_text("WEEGEE IS DEFEATED", (WIDTH/2, HEIGHT/2), font_size=50)
             self.draw_text("YOU HAVE SAVED THE INTERNET", (WIDTH/2, HEIGHT/2 + 50), font_size=20)
             return

        # --- Main Gameplay Loop ---
        # Background
        self.surface.fill(DARK_RED)
        self.draw_background()

        # Procedural Music Vibe
        self.music_viz.update()
        self.music_viz.draw()

        # Characters
        self.draw_weegee()
        self.draw_player()
        
        # Projectiles and Effects
        self.update_projectiles()
        self.update_effects()

    # --- Vibe Drawing Functions ---
    def draw_intro_logo(self):
        i_color = (0, 200, 50)
        shadow_color = (0, 100, 25)
        w, h = 80, 200
        x, y = WIDTH/2 - w/2, HEIGHT/2 - h/2
        
        pygame.draw.rect(self.surface, shadow_color, (x + 10, y + 10, w, h))
        pygame.draw.rect(self.surface, i_color, (x, y, w, h))
        pygame.draw.rect(self.surface, i_color, (x - 20, y, w + 40, h/4))
        pygame.draw.rect(self.surface, i_color, (x - 20, y + h - h/4, w + 40, h/4))
        self.draw_text("Inteternenet", (WIDTH/2, HEIGHT - 40), font_size=30, color=i_color)

    def draw_background(self):
        for i in range(15):
            seed = i * 337
            x = (i * 70 + (pygame.time.get_ticks() // 100) * (seed % 5 - 2)) % (WIDTH + 100) - 50
            h = 100 + (seed % 150)
            w = 40 + (seed % 30)
            color_val = 60 + (seed % 40)
            pygame.draw.rect(self.surface, (color_val, color_val, color_val), (x, HEIGHT - h, w, h))

    def draw_player(self):
        x, y = self.player_pos
        pygame.draw.rect(self.surface, MARIO_BLUE, (x - 12, y, 24, 20))
        pygame.draw.rect(self.surface, MARIO_RED, (x - 12, y, 24, 10))
        pygame.draw.circle(self.surface, WEEGEE_SKIN, (x, y - 10), 10)
        pygame.draw.rect(self.surface, MARIO_RED, (x - 10, y - 25, 20, 8))
        pygame.draw.circle(self.surface, MARIO_RED, (x, y - 18), 8)

    def draw_weegee(self):
        shake_x = (random.random() - 0.5) * self.weegee_shake
        shake_y = (random.random() - 0.5) * self.weegee_shake
        x, y = self.weegee_pos[0] + shake_x, self.weegee_pos[1] + shake_y
        
        pygame.draw.rect(self.surface, WEEGEE_BLUE, (x - 120, y - 80, 240, 300))
        pygame.draw.rect(self.surface, WEEGEE_GREEN, (x - 110, y - 80, 220, 150))
        pygame.draw.circle(self.surface, SPAGHETTI_YELLOW, (x - 60, y), 20)
        pygame.draw.circle(self.surface, SPAGHETTI_YELLOW, (x + 60, y), 20)
        pygame.draw.ellipse(self.surface, WEEGEE_SKIN, (x - 100, y - 200, 200, 220))
        pygame.draw.rect(self.surface, WEEGEE_GREEN, (x - 80, y - 250, 160, 50))
        pygame.draw.ellipse(self.surface, WEEGEE_GREEN, (x-50, y-225, 100, 50))
        pygame.draw.circle(self.surface, WEEGEE_EYES, (x - 40, y - 150), 20 + math.sin(pygame.time.get_ticks()/200) * 5)
        pygame.draw.circle(self.surface, WEEGEE_EYES, (x + 40, y - 150), 20 + math.cos(pygame.time.get_ticks()/200) * 5)
        pygame.draw.rect(self.surface, BLACK, (x - 60, y - 120, 120, 20))
        self.weegee_shake *= 0.9

    def draw_text(self, text, pos, font_size=20, color=WHITE):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=pos)
        self.surface.blit(text_surface, text_rect)

    def update_projectiles(self):
        for proj in self.projectiles[:]:
            proj['pos'][1] -= proj['speed']
            if proj['pos'][1] < self.weegee_pos[1]:
                self.weegee_health -= proj['damage']
                self.weegee_shake = 20
                self.effects.append({'type': 'hit', 'pos': proj['pos'][:], 'life': 20, 'damage': proj['damage']})
                self.projectiles.remove(proj)
            else:
                self.draw_projectile(proj)

    def draw_projectile(self, proj):
        x, y = proj['pos']
        ptype = proj['type']
        if ptype == "robotnik":
            pygame.draw.ellipse(self.surface, NORRIS_BROWN, (x-20, y-15, 40, 30))
            pygame.draw.ellipse(self.surface, ROBOTNIK_ORANGE, (x-25, y, 50, 15))
            pygame.draw.rect(self.surface, BLACK, (x-15, y-10, 30, 5))
        elif ptype == "spaghetti":
            pygame.draw.circle(self.surface, WHITE, (x, y), 20)
            for _ in range(10):
                px = x + random.randint(-15, 15)
                py = y + random.randint(-15, 15)
                pygame.draw.circle(self.surface, SPAGHETTI_YELLOW, (px, py), 5)
        elif ptype == "norris":
            pygame.draw.rect(self.surface, NORRIS_BROWN, (x-30, y-10, 60, 15))
            pygame.draw.rect(self.surface, NORRIS_BROWN, (x-20, y-25, 40, 15))
            aura_color = (255, 255, 0, 100)
            radius = 30 + math.sin(pygame.time.get_ticks() / 100) * 10
            aura_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(aura_surf, aura_color, (radius, radius), radius)
            self.surface.blit(aura_surf, (x-radius, y-radius))

    def update_effects(self):
        for effect in self.effects[:]:
            effect['life'] -= 1
            if effect['life'] <= 0:
                self.effects.remove(effect)
            else:
                if effect['type'] == 'hit':
                    self.draw_text(str(effect['damage']), effect['pos'], font_size=30, color=SPAGHETTI_YELLOW)

    def attack(self):
        if self.game_state != "PLAYING": return
        self.weegee_health -= 10
        self.weegee_shake = 10
        self.effects.append({'type': 'hit', 'pos': [self.weegee_pos[0] + random.randint(-80, 80), self.weegee_pos[1] - 50], 'life': 20, 'damage': 10})

    def special_attack(self):
        if self.game_state != "PLAYING": return
        vibe = random.choice(["robotnik", "spaghetti", "norris"])
        damage_map = {"robotnik": 50, "spaghetti": 30, "norris": 200}
        self.projectiles.append({'type': vibe, 'pos': [self.player_pos[0], self.player_pos[1] - 40], 'speed': 8, 'damage': damage_map[vibe]})
        return f"UNLEASHED THE {vibe.upper()} VIBE!"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Weegee 3DS Showdown - GRAND FINALE")
        self.root.resizable(False, False)
        
        self.top_frame = tk.Frame(root, width=WIDTH, height=HEIGHT, bg="black")
        self.top_frame.pack()
        
        # **THE FIX IS HERE:** Using a helper function to convert RGB tuples to hex strings for Tkinter
        self.bottom_frame = tk.Frame(root, width=WIDTH, height=BOTTOM_HEIGHT, bg=self.rgb_to_hex(DARK_GREY))
        self.bottom_frame.pack(fill="both", expand=True)

        os.environ['SDL_WINDOWID'] = str(self.top_frame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        
        self.game = Game(self.screen)
        
        self.setup_bottom_screen()
        self.update_loop()

    def rgb_to_hex(self, rgb):
        """Translates an (R, G, B) tuple to a #RRGGBB string."""
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

    def setup_bottom_screen(self):
        style = ttk.Style()
        style.theme_use('clam')
        # **APPLYING THE FIX** to all Tkinter color settings
        dark_grey_hex = self.rgb_to_hex(DARK_GREY)
        weegee_eyes_hex = self.rgb_to_hex(WEEGEE_EYES)
        grey_hex = self.rgb_to_hex(GREY)
        light_grey_hex = self.rgb_to_hex(LIGHT_GREY)

        style.configure("red.Horizontal.TProgressbar", foreground='red', background='red', troughcolor=dark_grey_hex)
        style.configure('TButton', background=grey_hex, foreground='white', borderwidth=1, focusthickness=3, focuscolor='none')
        style.map('TButton', background=[('active', light_grey_hex)])

        self.health_label = tk.Label(self.bottom_frame, text="WEEGEE'S SOUL", bg=dark_grey_hex, fg=self.rgb_to_hex(WHITE))
        self.health_label.pack(pady=(5,0))
        self.health_bar = ttk.Progressbar(self.bottom_frame, orient="horizontal", length=WIDTH - 100,
                                          mode="determinate", maximum=self.game.weegee_max_health,
                                          style="red.Horizontal.TProgressbar")
        self.health_bar.pack(pady=5)
        
        controls_frame = tk.Frame(self.bottom_frame, bg=dark_grey_hex)
        controls_frame.pack(pady=5)

        self.attack_button = ttk.Button(controls_frame, text="Attack", command=self.do_attack)
        self.attack_button.pack(side="left", padx=10)

        self.special_button = ttk.Button(controls_frame, text="Unleash Vibe", command=self.do_special)
        self.special_button.pack(side="left", padx=10)
        
        self.status_text = tk.StringVar()
        self.status_text.set("The grand finale begins...")
        self.status_label = tk.Label(self.bottom_frame, textvariable=self.status_text, bg=dark_grey_hex, fg=weegee_eyes_hex)
        self.status_label.pack(pady=5)

    def do_attack(self):
        self.game.attack()
        self.status_text.set("A direct hit!")

    def do_special(self):
        msg = self.game.special_attack()
        if msg:
            self.status_text.set(msg)

    def update_loop(self):
        self.game.update()
        pygame.display.flip()

        self.health_bar['value'] = self.game.weegee_health
        if self.game.weegee_health <= 0 and self.game.game_state != "GAMEOVER":
            self.game.game_state = "GAMEOVER"
            self.status_text.set("VIBE OVERLOAD... CRITICAL FAILURE!")

        self.root.after(1000 // FPS, self.update_loop)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
