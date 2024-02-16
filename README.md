A game I made in python to test the waters of pygame.
If you already have pygame installed, you will get an error of type "FileNotFoundError".
The source code contains my personal file paths. You need to change the file paths that access the sound files.
To do that, go to the sound file in your files in the directory where you extracted
the game,for example, click.mp3, right click it and copy its **absolute** path (relative paths likely may not work).
Then, replace that with the path that is in the source code.

For example, instead of

click_sound = pygame.mixer.Sound(
    '/home/sadeem/Python/Shooter/shooter_game-main/test_shooter_game-main/click.mp3')

it will be

click_sound = pygame.mixer.Sound(
    '/path/to/click.mp3')

where '/path/to' is your own copied path.

Do the same with the two other sound variables, shoot_sound and bang_sound, and your game will be ready to play.
