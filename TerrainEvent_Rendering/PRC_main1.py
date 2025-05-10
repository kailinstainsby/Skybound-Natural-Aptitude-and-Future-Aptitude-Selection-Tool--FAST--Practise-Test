import pygame
import random

class QuizPopup:
    def __init__(self, screen, aircraft_count, waypoint_count, left_flashes, right_flashes, total_flashes, waypoints):
        self.correct_answers = 0
        self.incorrect_answers = 0

        self.screen = screen
        self.active = False
        self.selected_question = ""
        self.correct_answer = None
        self.options = []
        self.button_rects = []  # store button positions for click detection

        self.questions_asked = 0
        self.asked_questions = set()

        # store in-game variables
        self.left_flashes = left_flashes
        self.right_flashes = right_flashes
        self.total_flashes = total_flashes
        self.waypoints = waypoints

    def generate_question(self):
        if self.questions_asked >= 4:
            self.active = False
            return

        questions = [
            ("How many aircraft appeared on screen?", self.get_aircraft_count()),
            ("How many waypoints appeared on screen?", self.get_waypoint_count()),
            ("What is the total flashes the lights undertook?", self.get_total_flashes()),
            ("How many flashes did the left light undertake?", self.get_left_flashes()),
            ("How many flashes did the right light undertake?", self.get_right_flashes()),
        ]

        if self.waypoints:
            questions.append((
                f"What was the Waypoint at position {random.randint(1, len(self.waypoints))}?",
                random.choice(self.waypoints)
            ))

        available_questions = [q for q in questions if q[0] not in self.asked_questions]
        if not available_questions:
            self.active = False
            return

        self.selected_question, self.correct_answer = random.choice(available_questions)
        self.asked_questions.add(self.selected_question)
        self.questions_asked += 1
        
        # Generate three false answers
        false_answers = set()
        while len(false_answers) < 3:
            rand_option = random.randint(1, 10) if isinstance(self.correct_answer, int) else random.choice(self.waypoints)
            if rand_option != self.correct_answer:
                false_answers.add(rand_option)
        
        self.options = list(false_answers) + [self.correct_answer]
        random.shuffle(self.options)  # Shuffle answers
        self.active = True  # Activate the quiz


    def draw(self):
        if not self.active:
            return

        self.screen.fill((255, 255, 255))  #white background
        font = pygame.font.Font(None, 40)

        # draw question
        question_surface = font.render(self.selected_question, True, (50, 50, 50))
        question_rect = question_surface.get_rect(center=(self.screen.get_width() / 2, 100))
        self.screen.blit(question_surface, question_rect)

        #draw answer buttons
        button_width = self.screen.get_width() - 200
        button_height = 60
        start_y = 200
        button_gap = 20

        self.button_rects = []  #store button rects for click detection
        for i, option in enumerate(self.options):
            rect = pygame.Rect(
                (self.screen.get_width() - button_width) // 2, 
                start_y + i * (button_height + button_gap), 
                button_width, 
                button_height
            )
            self.button_rects.append((rect, option))  #store button rect with option value
            
            pygame.draw.rect(self.screen, (220, 220, 220), rect)  # Draw button
            text_surface = font.render(str(option), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if not self.active:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:  #detect mouse click
            mouse_pos = pygame.mouse.get_pos()
            for rect, option in self.button_rects:
                if rect.collidepoint(mouse_pos):  # check if clicked inside button
                    if option == self.correct_answer:
                        print("Correct Answer!")
                        self.correct_answers += 1 
                    else:
                        print("Wrong Answer!")
                        self.incorrect_answers += 1 


                    if self.questions_asked < 3:
                        self.generate_question()  # Load next question
                    else:
                        self.active = False

    def get_aircraft_count(self):
        return self.aircraft_count

    def get_waypoint_count(self):
        return self.waypoint_count

    def get_total_flashes(self):
        return self.total_flashes

    def get_left_flashes(self):
        return self.left_flashes

    def get_right_flashes(self):
        return self.right_flashes
