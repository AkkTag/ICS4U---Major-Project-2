import pygame
#pygame.init()

font_title = pygame.font.SysFont("cambria", 40, bold=True)

class LoadingScreen:
    def __init__(self, screen_width=896, screen_height=640):
        """
        Initialize the loading screen.
        
        Args:
            screen_width: Width of the screen
            screen_height: Height of the screen
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Semi-light blue background colour (RGB)
        self.background_colour = (50, 50, 255)  # Dark blue
        self.inner_rect = pygame.Rect(50, 50, self.screen_width - 100, self.screen_height - 100)  # Inner rectangle for design
        self.inner_rect_colour = (125, 175, 255)  # Lighter blue for inner rectangle

        self.inner2_rect = pygame.Rect(60, 60, self.screen_width - 120, self.screen_height - 120)
        self.inner2_rect_colour = (6, 18, 36)

        
        # Loading text settings
        self.loading_text = "TELEPORTING..."
        self.font_size = 48
        self.text_colour = (245, 215, 120)  # White text
        
        # --- DRAW HEADER TEXT ---
        # title_surf = font_title.render("CHALLENGE", True, TEXT_GOLD)
        # screen.blit(title_surf, (screen.width // 2 - title_surf.get_width() // 2, 40))

        # Animation timer for pulsing or dots effect
        self.animation_timer = 0
        self.animation_speed = 0.5  # seconds for full cycle
        
        # Image-based loading bar animation
        self.loading_bar_image = pygame.image.load("game_assets/'D' Currency PNG.png")
        self.loading_bar_image = pygame.transform.scale(self.loading_bar_image, (80, 80))  # Adjust size as needed
        self.max_bar_items = 5  # Maximum number of images to display
    
    def render(self, screen, elapsed_time=0):
        """
        Render the loading screen.
        
        Args:
            screen: The pygame display surface
            elapsed_time: Total time elapsed (used for animations)
        """
        # Draw semi-light blue background
        screen.fill(self.background_colour)
        screen.fill(self.inner_rect_colour, self.inner_rect)  # Draw inner rectangle for design
        screen.fill(self.inner2_rect_colour, self.inner2_rect) #Draw inner2 rectangle for added effect

        # Create font and render text
        # font = pygame.font.Font(None, self.font_size)
        text_surface = font_title.render(self.loading_text, True, self.text_colour)
        
        # Center the text on screen
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 15))
        screen.blit(text_surface, text_rect)
        
        # animation dots is an option
        self.render_animation(screen, elapsed_time)
        #self.render_with_progress(screen, progress=0.0) - implement this if time allows
    
    def render_animation(self, screen, elapsed_time):
        
        """
        Render a loading bar animation by duplicating an image.
        
        Args:
            screen: The pygame display surface
            elapsed_time: Total time elapsed
        """
        # Calculate number of images to show (1 to max_bar_items, cycling)
        bar_count = (int(elapsed_time * 2) % self.max_bar_items) + 1
        
        # Calculate starting position to center the bar
        image_width = self.loading_bar_image.get_width()
        spacing = 10  # Space between images
        total_width = (bar_count * image_width) + ((bar_count - 1) * spacing)
        start_x = (self.screen_width - total_width) // 2
        
        # Draw each image in the loading bar
        bar_y = (self.screen_height // 2) + 70
        for i in range(bar_count):
            x_pos = start_x + (i * (image_width + spacing))
            screen.blit(self.loading_bar_image, (x_pos, bar_y))
    
    def render_with_progress(self, screen, progress=0.5):
        """
        Render loading screen with a progress bar.
        
        Args:
            screen: The pygame display surface
            progress: Progress value from 0.0 to 1.0
        """
        # Draw background
        screen.fill(self.background_colour)
        
        # Draw text
        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.loading_text, True, self.text_colour)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        screen.blit(text_surface, text_rect)
        
        # Draw progress bar
        bar_width = 300
        bar_height = 30
        bar_x = (self.screen_width - bar_width) // 2
        bar_y = self.screen_height // 2 + 50
        
        # Background bar (dark)
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        
        # Filled bar (lighter blue)
        filled_width = int(bar_width * progress)
        pygame.draw.rect(screen, (70, 130, 180), (bar_x, bar_y, filled_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Percentage text
        percentage_text = f"{int(progress * 100)}%"
        percentage_surface = font.render(percentage_text, True, self.text_colour)
        percentage_rect = percentage_surface.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 + 110)
        )
        screen.blit(percentage_surface, percentage_rect)


#testing purposes
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((896, 640))
    pygame.display.set_caption("Loading Screen Test")
    
    loading = LoadingScreen()
    clock = pygame.time.Clock()
    elapsed = 0
    
    running = True
    while running:
        elapsed += clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Test basic loading screen
        loading.render(screen, elapsed)
        
        pygame.display.update()
    
    pygame.quit()
