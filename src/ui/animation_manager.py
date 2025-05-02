from kivy.animation import Animation
from kivy.utils import get_color_from_hex

class AnimationManager:
    @staticmethod
    def button_press(button):
        pass
    #     """Create press animation for buttons"""
    #     # Simple fade animation for button press
    #     fade_out = Animation(
    #         opacity=0.7,
    #         duration=0.1,
    #         transition='in_out_quad'
    #     )
    #     fade_in = Animation(
    #         opacity=1.0,
    #         duration=0.1,
    #         transition='in_out_quad'
    #     )
    #     color_change = Animation(
    #         background_color=(0.3, 0.7, 0.9, 1),
    #         duration=0.1
    #     ) + Animation(
    #         background_color=button.background_color,
    #         duration=0.1
    #     )
        
    #     # Combine animations
    #     anim = fade_out + fade_in
    #     anim &= color_change  # Run color change in parallel
    #     anim.start(button)

    # @staticmethod
    # def highlight_input(input_widget, success=True):
    #     """Create highlight animation for input widgets"""
    #     color = (0.9, 1, 0.9, 1) if success else (1, 0.9, 0.9, 1)
    #     anim = Animation(
    #         background_color=color,
    #         duration=0.3
    #     ) + Animation(
    #         background_color=(1, 1, 1, 1),
    #         duration=0.3
    #     )
    #     anim.start(input_widget)

    # @staticmethod
    # def fade_in(widget, duration=0.3):
    #     """Create fade in animation"""
    #     widget.opacity = 0
    #     anim = Animation(
    #         opacity=1,
    #         duration=duration
    #     )
    #     anim.start(widget)

    # @staticmethod
    # def fade_out(widget, duration=0.3):
    #     """Create fade out animation"""
    #     anim = Animation(
    #         opacity=0,
    #         duration=duration
    #     )
    #     anim.start(widget)