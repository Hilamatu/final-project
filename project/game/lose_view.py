# import arcade
# import arcade.gui
# from game import constants

# class LoseView(arcade.View):    

#     def on_show(self):
#         """This method will run once the view changes"""

#         self._return_button = Restart

#         self.manager = arcade.gui.UIManager()
#         self.manager.enable()

       
#         arcade.set_background_color(arcade.color.BLUE_GRAY)

#         arcade.start_render()       

#         # Create a vertical BoxGroup to align buttons
#         self.v_box = arcade.gui.UIBoxLayout()

#         # Create a text label
#         ui_text_label = arcade.gui.UITextArea(text="YOU LOSE",
#                                               width=450,
#                                               height=40,
#                                               font_size=24,
#                                               font_name="Kenney Blocks")
#         self.v_box.add(ui_text_label.with_space_around(bottom=20))

        
#         self.v_box.add(ui_text_label.with_space_around(bottom=0))

#         return_view = self._return_button(text="Restart", width=200)
#         self.v_box.add(return_view.with_space_around(bottom=20))

#         self.manager.add(
#             arcade.gui.UIAnchorWidget(
#                 anchor_x="center_x",
#                 anchor_y="center_y",
#                 child=self.v_box)
#         )

#     def on_draw(self):
#         """ Draw this view """
#         arcade.start_render()
#         self.manager.draw()
#         arcade.draw_text("You Lose", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT - 70, arcade.color.WHITE, font_size=50, anchor_x="center")


# class Restart(arcade.gui.UIFlatButton):
#     """A class to handle the Restart button clik"""
#     def on_click(self, event: arcade.gui.UIOnClickEvent):
#         window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, title=constants.SCREEN_TITLE)
#         start = GameView()
#         window.show_view(start)


